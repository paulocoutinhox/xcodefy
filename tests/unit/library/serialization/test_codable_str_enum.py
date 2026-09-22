import pytest

from xcodefy.errors.decode_error import DecodeError
from xcodefy.library.serialization.codable_str_enum import CodableStrEnum
from xcodefy.library.serialization.decoder import Decoder
from xcodefy.library.serialization.values.value import Value


class Sample(CodableStrEnum):
    FIRST = "first"
    SECOND = "second"


def test_a_member_reports_its_encodable_representation():
    assert Sample.FIRST.encodable_string_representation == "first"


def test_a_known_value_decodes():
    assert Sample.from_encodable_string("second") is Sample.SECOND
    assert Decoder.decode_value(Value.string("first"), Sample) is Sample.FIRST


def test_an_unknown_value_is_rejected():
    with pytest.raises(DecodeError, match="Unexpected value"):
        Sample.from_encodable_string("third")


def test_a_member_is_still_a_plain_string():
    assert Sample.FIRST.encode("utf-8") == b"first"
