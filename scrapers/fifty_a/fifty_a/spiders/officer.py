from typing import Any, Dict, List, Optional, Tuple

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

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
        _, gender = self.parse_race_and_gender(response)
        officer = OfficerItem(
            taxnum=self.parse_taxnum(response),
            url=response.url,
            gender=gender,
            complaints=self.parse_complaints(response),
            age=self.parse_age(response),
        )

        yield officer

    def parse_age(self, response):
        age = response.css(".age::text").get()
        if age:
            age = parse_string_to_number(age)
        return age


    @staticmethod
    def parse_taxnum(response) -> Optional[int]:
        taxid_span_text = response.css(".taxid::text").get()

        if taxid_span_text:
            taxid_text_split = taxid_span_text.split("#")
            if len(taxid_text_split) <= 1 or len(taxid_text_split) >= 3:
                return None
            else:
                return int(taxid_text_split[1])



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
    def parse_complaints(response) -> Optional[List[int]]:
        complaints = []

        complaints_anchors = response.css(".complaint a::text").getall()

        for anchor_text in complaints_anchors:
            anchor_text_split = anchor_text.strip().split(",")
            if len(anchor_text_split) <= 1 or len(anchor_text_split) >= 3:
                continue
            else:
                complaint_text, _ = anchor_text_split
                complaint_text_split = complaint_text.split("#")
                if len(complaint_text_split) <= 1 or len(complaint_text_split) >= 3:
                    continue
                else:
                    complaints.append(int(complaint_text_split[1]))

        return complaints
