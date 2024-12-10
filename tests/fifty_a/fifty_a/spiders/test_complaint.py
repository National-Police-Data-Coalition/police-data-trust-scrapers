from datetime import date

import pytest
from scrapy.http import HtmlResponse

from models.complaints import CreateAllegation, CreateComplaint, CreatePenalty
from scrapers.fifty_a.fifty_a.items import SOURCE_REL, SOURCE_UID
from scrapers.fifty_a.fifty_a.spiders.complaint import ComplaintSpider
from tests.fifty_a.fifty_a.spiders.complaint_page import complaint_1

mock_response = HtmlResponse(url="dummy", body=complaint_1)


class TestComplaint:
    def test_parse_complaint(self):
        spider = ComplaintSpider()
        results = [i for i in spider.parse_complaint(mock_response)]
        assert len(results) == 1

        complaint = results[0]
        assert complaint.url == mock_response.url
        assert complaint.model == "complaint"
        assert complaint.source_uid == SOURCE_UID

        try:
            valid_data = CreateComplaint(**complaint.data)
        except ValueError as e:
            pytest.fail(f"Complaint Data is invalid: {e}")

        assert valid_data.record_id == "202201364"
        assert valid_data.incident_date == date(2022, 2, 19)
        assert valid_data.received_date == date(2022, 3, 7)
        assert valid_data.closed_date == date(2023, 4, 12)
        # assert valid_data.updated_date == date(2024, 12, 8)
        assert valid_data.reason_for_contact == "Report-domestic dispute"
        assert valid_data.outcome_of_contact == "Arrest - other violation/crime"

        # Source Details
        assert valid_data.source_details.record_type == SOURCE_REL["record_type"]
        assert (
            valid_data.source_details.reporting_agency == SOURCE_REL["reporting_agency"]
        )
        assert (
            valid_data.source_details.reporting_agency_url
            == SOURCE_REL["reporting_agency_url"]
        )

        # Location
        assert valid_data.location["location_type"] == "Street/highway"
        assert valid_data.location["location_description"] == "24th Precinct, Manhattan"

        # Allegations
        a_data = valid_data.allegations[4]
        if not isinstance(a_data, CreateAllegation):
            pytest.fail("Allegation Data is invalid.")
        assert a_data.allegation == "Physical force"
        assert a_data.type == "Force"
        assert a_data.finding == "Miscellaneous - Subject Terminated"
        assert a_data.perpetrator_uid == "/officer/EW7Z"
        assert a_data.complainant.age == 37
        assert a_data.complainant.age_range == "35-39"
        assert a_data.complainant.gender == "Male"

        # Penalties
        p_data = valid_data.penalties[1]
        if not isinstance(p_data, CreatePenalty):
            pytest.fail("Penalty Data is invalid.")
        assert p_data.officer_uid == "/officer/4S6M"
        assert p_data.crb_case_status == "Closed"
        assert p_data.date_assesed == date(2024, 11, 1)
        assert p_data.crb_plea == "Forfeit vacation 10 days"
