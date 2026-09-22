import pytest

from xcodefy.errors.decode_error import DecodeError
from xcodefy.library.schema.values.marketing_version import MarketingVersion


@pytest.mark.parametrize(("major", "minor", "update", "encoding"), [(0, 0, 0, "0.0"), (0, 0, 1, "0.0.1"), (1, 0, 0, "1.0"), (1, 2, 0, "1.2"), (1, 0, 3, "1.0.3")])
def test_a_zero_update_is_dropped_from_the_encoding(major, minor, update, encoding):
    version = MarketingVersion(major, minor, update)
    assert version.encodable_string_representation == encoding
    assert str(version) == encoding


@pytest.mark.parametrize(("text", "expected"), [("1.2", MarketingVersion(1, 2, 0)), ("1.2.3", MarketingVersion(1, 2, 3))])
def test_two_and_three_component_versions_decode(text, expected):
    assert MarketingVersion.from_encodable_string(text) == expected


@pytest.mark.parametrize("text", ["", "1", "1.2.3.4", "1.x", "a.b", "1..2", "-1.2", "1.2.", "١.٢"])
def test_malformed_versions_are_rejected(text):
    with pytest.raises(DecodeError, match="Invalid version string"):
        MarketingVersion.from_encodable_string(text)


def test_only_ascii_digits_count_as_integers():
    assert MarketingVersion.is_integer("12") is True
    assert MarketingVersion.is_integer("") is False
    assert MarketingVersion.is_integer("١") is False
