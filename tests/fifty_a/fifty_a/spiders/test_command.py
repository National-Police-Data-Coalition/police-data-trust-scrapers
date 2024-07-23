from scrapy import Request
from scrapy.http import HtmlResponse
import pytest

from scrapers.fifty_a.fifty_a.spiders.command import CommandSpider
from tests.fifty_a.fifty_a.spiders.command_page import command_first_precinct_html

@pytest.fixture
def mock_command_response():
    req = Request(url="https://www.50-a.org/command/1pct")
    resp = HtmlResponse(url=req.url, request=req, body=command_first_precinct_html, encoding='utf-8')
    return resp

class TestCommand:
    def test_parse(self, mock_command_response):
        spider = CommandSpider()
        result = next(spider.parse_command(mock_command_response))
        assert result.name == "1st Precinct"

        
    def test_parse_intro(self, mock_command_response):
        spider = CommandSpider()
        commanding_officer_url, command_address, command_description = spider.parse_intro(mock_command_response)

        assert commanding_officer_url == "https://www.50-a.org/officer/S753"
        assert command_address == "16 Ericsson Pl, New York, NY 10013"
        assert command_description == """The 1st Precinct serves an area that consists of a square mile 
on the southernmost tip of Manhattan. The precinct is home to the World 
Trade Center, SOHO, Tribeca, and Wall Street."""


    def test_parse_website_url(self, mock_command_response):
        spider = CommandSpider()
        website_url = spider.parse_website_url(mock_command_response)

        assert website_url == "https://www1.nyc.gov/site/nypd/bureaus/patrol/precincts/1st-precinct.page"


    def test_parse_officers(self, mock_command_response):
        spider = CommandSpider()
        officers = spider.parse_officers(mock_command_response)

        assert officers[0].most_recent == 2024
        assert officers[0].url == "https://www.50-a.org/officer/47B7"

        assert officers[len(officers)-1].most_recent is None
        assert officers[len(officers)-1].url == "https://www.50-a.org/officer/YAMX"
