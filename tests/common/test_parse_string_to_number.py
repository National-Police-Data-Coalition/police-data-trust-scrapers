import pytest

from scrapers.common.parse import parse_string_to_number


class TestParseStringToNumber:
    def test_handles_type_error(self):
        assert parse_string_to_number(None) is None

    def test_raises_not_implemented_error(self):
        with pytest.raises(NotImplementedError):
            parse_string_to_number("11.234")

    @pytest.mark.parametrize(
        "value, expected",
        [
            ("1", 1),
            ("99", 99),
        ],
    )
    def test_parses_as_expected(self, value, expected):
        assert parse_string_to_number(value) == expected
