import pytest

from xcodefy.library.schema.values.string_encoding import ENCODING_VALUES, StringEncoding


def test_every_member_maps_to_an_integer_value():
    assert all(encoding in ENCODING_VALUES for encoding in StringEncoding)


def test_the_foundation_values_are_used():
    assert StringEncoding.UTF8.encoding_value == 4
    assert StringEncoding.UTF32_LITTLE_ENDIAN.encoding_value == 0x9C000100


def test_unicode_and_utf16_share_the_same_value_and_canonical_name():
    assert StringEncoding.UNICODE.encoding_value == StringEncoding.UTF16.encoding_value
    assert StringEncoding.from_encoding_value(10) is StringEncoding.UNICODE


@pytest.mark.parametrize("encoding", list(StringEncoding))
def test_every_named_encoding_is_recoverable_from_its_value(encoding):
    assert StringEncoding.from_encoding_value(encoding.encoding_value) is not None


def test_an_unknown_value_has_no_name():
    assert StringEncoding.from_encoding_value(23418341) is None
