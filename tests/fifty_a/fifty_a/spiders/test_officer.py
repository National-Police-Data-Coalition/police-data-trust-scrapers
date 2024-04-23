import pytest
from scrapy.http import HtmlResponse

from scrapers.fifty_a.fifty_a.spiders.officer import OfficerSpider

from tests.fifty_a.fifty_a.spiders.officer_page import officer_1

mock_response = HtmlResponse(url="dummy", body=officer_1)


class TestOfficer:
    def test_parse_complaints(self):
        expected = {
            "complaints": 4,
            "allegations": 9,
            "substantiated": 1,
            "Substantiated (Formalized Training)": 1,
            "Closed - Pending Litigation": 1,
            "Complainant Uncooperative": 5,
            "Complaint Withdrawn": 1,
            "Exonerated": 1,
        }
        results = OfficerSpider.parse_complaints(mock_response)

        for res in results:
            name = res["name"]
            count = res["count"]

            assert count == expected[name]

    def test_parse_officer(self):
        spider = OfficerSpider()
        results = [i for i in spider.parse_officer(mock_response)]
        assert len(results) == 1

        officer = results[0]
        assert officer.url == mock_response.url
        assert officer.name == "Lawrence Wang"
        assert officer.badge is None
        assert officer.race == "Asian"
        assert officer.gender == "Male"
        assert len(officer.complaints) == 8
        assert officer.age == 37

    @pytest.mark.parametrize(
        "body, race, gender",
        [
            (
                b"""<span class="desc">Asian Male, <span class="age">37</span></span>""",
                "Asian",
                "Male",
            ),
            (b"""<span class="desc"><span class="age">37</span></span>""", None, None),
            (
                b"""<span class="desc">Native american Female, <span class="age">37</span></span>""",
                "Native american",
                "Female",
            ),
            (
                b"""<span class="desc">Black, <span class="age">37</span></span>""",
                "Black",
                None,
            ),
        ],
    )
    def test_parse_race_and_gender(self, body, race, gender):
        mock_response = HtmlResponse(url="dummy", body=body)

        spider = OfficerSpider()
        results = [i for i in spider.parse_officer(mock_response)]
        assert len(results) == 1

        officer = results[0]

        assert officer.race == race
        assert officer.gender == gender
