from datetime import date

import pytest
from scrapy.http import HtmlResponse

from models.litigation import CreateLitigation
from models.officers import CreateOfficer
from scrapers.fifty_a.fifty_a.items import AGENCY_UID, SOURCE_UID
from scrapers.fifty_a.fifty_a.spiders.officer import OfficerSpider
from tests.fifty_a.fifty_a.spiders.officer_page import officer_1

mock_response = HtmlResponse(url="dummy", body=officer_1)


class TestOfficer:
    def test_parse_officer(self):
        spider = OfficerSpider()
        results = [i for i in spider.parse_officer(mock_response)]
        assert len(results) == 6

        officer = results[0]
        assert officer.url == mock_response.url
        assert officer.model == "officer"
        assert officer.source_uid == SOURCE_UID
        assert officer.service_start == "July 2009"

        for e in officer.employment:
            assert e["agency_uid"] == AGENCY_UID
            assert "/command/" in e["unit_uid"]
        try:
            valid_data = CreateOfficer(**officer.data)
        except ValueError as e:
            pytest.fail(f"Officer Data is invalid: {e}")

        assert valid_data.first_name == "Lawrence"
        assert valid_data.last_name == "Wang"
        assert valid_data.ethnicity == "Asian"
        assert valid_data.gender == "Male"
        assert valid_data.state_ids[0].value == "948283"
        assert valid_data.state_ids[0].id_name == "Tax ID"
        assert (
            valid_data.attachments[0].url
            == "https://www.documentcloud.org/documents/21019814-daf-wang948283"
        )
        assert valid_data.attachments[0].title == "DA Disclosure Letter"

        litigation = results[1]

        try:
            valid_lawsuit = CreateLitigation(**litigation.data)
        except ValueError as e:
            pytest.fail(f"Litigation Data is invalid: {e}")

        assert valid_lawsuit.case_title == "Cavender, Shawn vs City of New York, et al."
        assert (
            valid_lawsuit.url
            == "https://www.courtlistener.com/docket/60324680/cavender-v-city-of-new-york/"
        )
        assert valid_lawsuit.settlement_amount == 60000
        assert valid_lawsuit.docket_number == "21CV07290"
        assert valid_lawsuit.court_level == "Federal District Court"
        assert valid_lawsuit.start_date == date(2021, 10, 28)
        assert valid_lawsuit.end_date == date(2022, 11, 2)
        assert valid_lawsuit.documents[0].title == "Complaint"
        assert (
            valid_lawsuit.documents[0].url
            == "https://storage.courtlistener.com/recap/gov.uscourts.nysd.565800/gov.uscourts.nysd.565800.17.0.pdf"
        )
        assert valid_lawsuit.defendants[0] == mock_response.url
