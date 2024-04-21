from typing import List, Optional, Dict, Any

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
        """
        badge = response.css('.badge::text').get()
        description = response.xpath("//span[contains(@class, 'desc')]/text()").get()
        """

        complaints = self.parse_complaints(response)

        officer = OfficerItem(
            url=response.url,
            name=response.css("h1::text").get(),
            badge=response.css(".badge::text").get(),
            description=response.xpath("//span[contains(@class, 'desc')]/text()").get(),
            complaints=complaints,
        )

        yield officer

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
                complaints.append({"name": name, "count": count})
        return complaints

    def parse(self, response):
        pass
