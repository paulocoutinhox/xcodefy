import pytest

from xcodefy.errors.decode_error import DecodeError
from xcodefy.library.schema.build_files.code_generation import CodeGeneration

VALUES = ["default", "skip"]


def test_every_case_from_the_reference_schema_is_represented():
    assert [member.value for member in CodeGeneration] == VALUES


@pytest.mark.parametrize("value", VALUES)
def test_every_case_decodes_from_its_encoded_value(value):
    assert CodeGeneration.from_encodable_string(value).encodable_string_representation == value


def test_an_unknown_value_is_rejected():
    with pytest.raises(DecodeError, match="Unexpected value"):
        CodeGeneration.from_encodable_string("not-a-case")
