import pytest
from scrapy.http import HtmlResponse

from models.agencies import CreateUnit
from scrapers.fifty_a.fifty_a.spiders.command import CommandSpider
from tests.fifty_a.fifty_a.spiders.command_page import command_1

mock_response = HtmlResponse(url="dummy-commands", body=command_1)


class TestCommand:
    def test_parse_command(self):
        spider = CommandSpider()
        results = [i for i in spider.parse_command(mock_response)]

        assert len(results) == 1

        unit = results[0]
        assert unit.url == mock_response.url
        assert unit.model == "unit"
        assert unit.source == "50-a.org"

        try:
            valid_data = CreateUnit(**unit.data)
        except ValueError as e:
            pytest.fail(f"Unit Data is invalid: {e}")

        assert valid_data.name == "9th Precinct"
        assert (
            valid_data.website_url
            == "https://www1.nyc.gov/"
            + "site/nypd/bureaus/patrol/precincts/9th-precinct.page"
        )
        assert valid_data.phone == "(212) 477-7812"
        assert (
            valid_data.description
            == "The 9th Precinct serves "
            + "the area from East Houston Street to East 14 Street from "
            + "Broadway, to the East River in Manhattan. The precinct is"
            + " home to the East Village, and features Tompkins "
            + "Square Park."
        )
        assert valid_data.address == "321 E 5th St"
        assert valid_data.city == "New York"
        assert valid_data.state == "NY"
        assert valid_data.zip == "10003"
        assert valid_data.commander_uid == "/officer/HUHH"
