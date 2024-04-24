from typing import List, Optional, Dict, Any, Tuple

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from scrapers.common.parse import parse_string_to_number
from scrapers.fifty_a.fifty_a.items import OfficerItem


class OfficerSpider(CrawlSpider):
    name = "officer"
    allowed_domains = ["www.50-a.org"]
    start_urls = ["https://www.50-a.org/commands"]

    rules = (
        Rule(LinkExtractor(allow="command"), follow=True),
        Rule(LinkExtractor(allow="officer"), callback="parse_officer"),
    )

    def parse_officer(self, response):
        race, gender = self.parse_race_and_gender(response)
        officer = OfficerItem(
            url=response.url,
            name=response.css("h1::text").get(),
            badge=response.css(".badge::text").get(),
            race=race,
            gender=gender,
            complaints=self.parse_complaints(response),
            age=response.css(".age::text").get(),
        )

        yield officer

    @staticmethod
    def parse_race_and_gender(response) -> Tuple[Optional[str], Optional[str]]:
        race = None
        gender = None

        description_text = response.xpath(
            "//span[contains(@class, 'desc')]/text()"
        ).get("")
        race_and_gender = description_text.split(",")[0]

        splits = [i.strip() for i in race_and_gender.split()]
        if len(splits) == 0:
            return race, gender
        elif len(splits) == 1:
            race = splits[0]
        else:
            race = " ".join(splits[:-1])
            gender = splits[-1]

        return race, gender

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
