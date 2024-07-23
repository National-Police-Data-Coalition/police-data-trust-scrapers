import pytest
from scrapy.http import HtmlResponse

from scrapers.fifty_a.fifty_a.spiders.officer import OfficerSpider
from tests.fifty_a.fifty_a.spiders.officer_page import officer_1

mock_response = HtmlResponse(url="dummy", body=officer_1, encoding='utf-8')


class TestOfficer:
    def test_parse_complaints(self):
        expected = [202400461, 202002491, 201810646, 201401749]
        results = OfficerSpider.parse_complaints(mock_response)

        assert set(results) == set(expected)

    def test_parse_officer(self):
        spider = OfficerSpider()
        officer = next(spider.parse_officer(mock_response))

        assert officer.url == mock_response.url
        assert officer.gender == "Male"
        assert officer.age == 37
        assert officer.taxnum == 948283

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
    def test_parse_gender(self, body, race, gender):
        mock_response = HtmlResponse(url="dummy", body=body, encoding='utf-8')

        spider = OfficerSpider()
        results = [i for i in spider.parse_officer(mock_response)]
        assert len(results) == 1

        officer = results[0]

        assert officer.gender == gender
