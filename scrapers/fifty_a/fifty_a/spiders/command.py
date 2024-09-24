from typing import Optional, Tuple

from scrapers.common.text_utility import strip_and_replace_text

from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from scrapers.fifty_a.fifty_a.items import CommandItem, CommandOfficerItem

BASE_URL = 'https://www.50-a.org'

class CommandSpider(CrawlSpider):
    name = "command"
    allowed_domains = ["www.50-a.org"]
    start_urls = ["https://www.50-a.org/commands"]

    rules = (
        Rule(LinkExtractor(allow="/command"), callback="parse_command", follow=False),
    )

    def parse_command(self, response):
        commanding_officer_url, command_address, command_description = self.parse_intro(response)
        website_url = self.parse_website_url(response)
        command = CommandItem(
            name=strip_and_replace_text(response.css(".title.command::text").extract_first()),
            url=strip_and_replace_text(response.url),
            website_url=strip_and_replace_text(website_url),
            commanding_officer_url=strip_and_replace_text(commanding_officer_url),
            address=strip_and_replace_text(command_address),
            description=strip_and_replace_text(command_description),
            officers=self.parse_officers(response)
        )

        yield command

    @staticmethod
    def parse_intro(response) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        commanding_officer_url = None
        command_address = None

        commanding_officer_relative_url = response.css(".intro p span + a::attr(href)").extract_first()

        if commanding_officer_relative_url:
            commanding_officer_url = commanding_officer_relative_url

        address_link = response.css(".intro > a")

        if 'maps' in address_link.attrib['href']:
            command_address = address_link.css("::text").extract_first()

        command_description = response.css(".intro p:last-of-type::text").get()

        return commanding_officer_url, command_address, command_description

    @staticmethod
    def parse_website_url(response) -> Optional[str]:
        links_column_elements = response.css(".links.column a")

        for link in links_column_elements:
            link_text = link.css("::text").get()
            # There are several links, sometimes the number varies, so matching the string is important to finding the
            # right link since no other attribute differs among them
            if link_text == "Precinct Website":
                return link.css("::attr(href)").get()

        # If no elements found(sometimes there are no links, or no website links) then just return None
        return None

    @staticmethod
    def parse_officers(response) -> list[Optional[CommandOfficerItem]]:
        officer_list = []

        officer_table_elements = response.css(".officers table tbody tr:not(.header)")

        for officer_table_element in officer_table_elements:
            officer_url = None
            officer_most_recent = None
            officer_scraped_url = officer_table_element.css("td.officer a::attr(href)").extract_first()
            officer_scraped_most_recent = officer_table_element.css("td.year::text").extract_first().strip()

            if officer_scraped_url:
                officer_url = strip_and_replace_text(officer_scraped_url)

            if officer_scraped_most_recent:
                officer_most_recent = int(officer_scraped_most_recent)

            officer_list.append(CommandOfficerItem(
                url=officer_url,
                most_recent=officer_most_recent
            ))

        return officer_list

