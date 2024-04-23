from scrapy.http import HtmlResponse

from scrapers.fifty_a.fifty_a.spiders.command import CommandSpider
from tests.fifty_a.fifty_a.spiders.commands_page import page_1

mock_response = HtmlResponse(url="dummy-commands", body=page_1)


class TestCommand:
    def test_parse(self):
        spider = CommandSpider()
        results = [i for i in spider.parse(mock_response)]

        assert len(results) == 489

        first_result = results[0]
        assert first_result.url == "/command/1pct"
        assert first_result.name == "1st Precinct"
