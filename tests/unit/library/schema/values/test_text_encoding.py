from tests.support.round_trip import RoundTrip
from xcodefy.library.schema.values.string_encoding import StringEncoding
from xcodefy.library.schema.values.text_encoding import TextEncoding


def test_a_named_encoding_prints_its_name():
    assert RoundTrip.text(TextEncoding.of(StringEncoding.UTF8)) == '"utf8"\n'


def test_an_unknown_encoding_prints_its_integer_value():
    assert RoundTrip.text(TextEncoding(23418341)) == "23418341\n"


def test_the_named_encoding_is_exposed():
    assert TextEncoding.of(StringEncoding.UTF8).string_encoding is StringEncoding.UTF8
    assert TextEncoding(23418341).string_encoding is None


def test_utf16_normalises_onto_the_unicode_name():
    assert RoundTrip.text(TextEncoding.of(StringEncoding.UTF16)) == '"unicode"\n'
    RoundTrip.expect_equal(TextEncoding.of(StringEncoding.UTF16), TextEncoding)
