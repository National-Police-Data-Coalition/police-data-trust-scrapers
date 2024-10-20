import re
import random
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapers.common.parse import parse_string_to_number
from scrapers.fifty_a.fifty_a.items import OfficerItem
from models.officers import CreateOfficer, StateId
from models.enums import Ethnicity


class OfficerSpider(CrawlSpider):
    name = "officer"
    allowed_domains = ["www.50-a.org"]
    start_urls = ["https://www.50-a.org/commands"]

    def __init__(self, *args, **kwargs):
        super(OfficerSpider, self).__init__(*args, **kwargs)
        self.test_mode = 'test_mode' in kwargs
        self.max_officers = int(kwargs.get("max_officers", 10))

        if self.test_mode:
            self.rules = (
                Rule(LinkExtractor(allow="officer"), callback="parse_officer"),
            )
        else:
            self.rules = (
                Rule(LinkExtractor(allow="command"), follow=True),
                Rule(LinkExtractor(allow="officer"), callback="parse_officer"),
            )

    def parse_start_url(self, response):
        commands = response.css("a.command::attr(href)").getall()
        if self.test_mode and commands:
            selected_command = random.choice(commands)
            yield response.follow(selected_command, self.parse_command)
        elif not self.test_mode:
            for command in commands:
                yield response.follow(command, self.parse_command)

    def parse_command(self, response):
        officer_links = response.css("td.officer a.name::attr(href)").getall()
        logging.info(f"Found {len(officer_links)} officers in {response.url}")

        if self.test_mode:
            random.shuffle(officer_links)
            officer_links = officer_links[:self.max_officers]

        for officer_link in officer_links:
            logging.info(f"Yeilding request for {officer_link}")
            yield response.follow(officer_link, self.parse_officer)

    def parse_officer(self, response):
        name = response.css("h1.title.name::text").get()
        name_parts = self.parse_name(name)
        description = response.css("span.desc::text").get()
        ethnicity, gender = self.parse_description(description)

        tax_id = response.css("span.taxid::text").re_first(r"Tax #(\d+)")
        state_id = StateId(
            state="NY",
            id_name="Tax ID",
            value=tax_id
        ) if tax_id else None

        rank = response.css("span.rank::text").get()

        command_info = response.css("div.command::text").get()
        logging.info(f"Command Info: {command_info}")
        since_date = response.css("div.command::text").re(r'since\s+(.*)')
        service_info = response.css("div.service::text").get()
        service_start = re.search(r"started (\w+ \d{4})", service_info)
        service_start = service_start.group(1) if service_start else None

        officer_data = {
            "first_name": name_parts.get("first_name"),
            "middle_name": name_parts.get("middle_name"),
            "last_name": name_parts.get("last_name"),
            "suffix": name_parts.get("suffix"),
            "ethnicity": self.map_ethnicity(ethnicity),
            "gender": gender,
            "state_ids": [state_id] if state_id else None
        }

        employment_history = []

        employment_history.append({
            'earliest_date': since_date,
            'latest_date': datetime.now().strftime("%B %Y"),
            'badge_number': response.css("span.badge::text").get(),
            'highest_rank': rank,
            'unit_uid': response.css("div.command a.command::attr(href)").get()
        })

        prev_employment = response.css(
            "div.commandhistory a::attr(href)").getall()
        for emp in prev_employment:
            employment_history.append({
                'unit_uid': emp
            })

        try:
            officer = CreateOfficer(**officer_data)
        except ValueError as e:
            logging.error(f"Validation error for officer {name}: {e}")
            return None

        yield OfficerItem(
            url=response.url,
            model="officer",
            data=officer.model_dump(),
            employment=employment_history,
            service_start=service_start
        )

    @staticmethod
    def parse_name(name):
        parts = name.split()
        suffixes = ["Jr", "Sr", "II", "III", "IV"]
        result = {}

        if parts[-1] in suffixes:
            result["suffix"] = parts[-1].pop()

        result["first_name"] = parts[0]
        result["last_name"] = parts[-1]
        if len(parts) > 2:
            result["middle_name"] = " ".join(parts[1:-1])
        return result

    @staticmethod
    def parse_description(description):
        if description:
            parts = description.split()
            if len(parts) >= 2:
                ethnicity = parts[0]
                gender = parts[1]
                return ethnicity, gender
        return None, None

    @staticmethod
    def map_ethnicity(ethnicity):
        if not ethnicity:
            return Ethnicity.UNKNOWN

        ethnicity_mapping = {
            "black": Ethnicity.BLACK_AFRICAN_AMERICAN,
            "white": Ethnicity.WHITE,
            "asian": Ethnicity.ASIAN,
            "hispanic": Ethnicity.HISPANIC_LATINO,
            "american indian": Ethnicity.AMERICAN_INDIAN_ALASKA_NATIVE,
            "native hawaiian": Ethnicity.NATIVE_HAWAIIAN_PACIFIC_ISLANDER,
        }

        for key, value in ethnicity_mapping.items():
            if key in ethnicity.lower():
                return value

        return Ethnicity.UNKNOWN

    @staticmethod
    def parse_complaints(response) -> List[Optional[Dict[str, Any]]]:
        complaints = []
        for i in ["complaints", "allegations", "substantiated"]:
            count = response.css(f".column .{i} .count::text").get()
            count_parsed = parse_string_to_number(count)
            if count_parsed is not None:
                complaints.append({"name": i, "count": count_parsed})

        for disp in response.css(".dispositions").css(".disposition"):
            count = disp.css(".count::text").get()
            count_parsed = parse_string_to_number(count)
            if count_parsed is not None:
                name = disp.css(".name::text").get()
                complaints.append({"name": name, "count": count_parsed})
        return complaints
