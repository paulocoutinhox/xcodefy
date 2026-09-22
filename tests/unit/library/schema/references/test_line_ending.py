import pytest

from xcodefy.errors.decode_error import DecodeError
from xcodefy.library.schema.references.line_ending import LineEnding

VALUES = ["line-feed", "carriage-return", "carriage-return-line-feed", "preserve"]


def test_every_case_from_the_reference_schema_is_represented():
    assert [member.value for member in LineEnding] == VALUES


@pytest.mark.parametrize("value", VALUES)
def test_every_case_decodes_from_its_encoded_value(value):
    assert LineEnding.from_encodable_string(value).encodable_string_representation == value


def test_an_unknown_value_is_rejected():
    with pytest.raises(DecodeError, match="Unexpected value"):
        LineEnding.from_encodable_string("not-a-case")
