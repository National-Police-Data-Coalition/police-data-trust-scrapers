import scrapy

from scrapers.fifty_a.fifty_a.items import CommandItem


class CommandSpider(scrapy.Spider):
    name = "command"
    allowed_domains = ["www.50-a.org"]
    start_urls = ["https://www.50-a.org/commands"]

    def parse(self, response):
        for c in response.css("a.command"):
            url = c.css("::attr(href)").extract_first()
            command = CommandItem(
                name=c.css("::text").extract_first(), url=response.urljoin(url)
            )

            yield command
