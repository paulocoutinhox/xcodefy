import pytest

from xcodefy.errors.decode_error import DecodeError
from xcodefy.library.schema.references.reference_kind import ReferenceKind

VALUES = ["file-reference", "group", "folder", "variant-group", "version-group"]


def test_every_case_from_the_reference_schema_is_represented():
    assert [member.value for member in ReferenceKind] == VALUES


@pytest.mark.parametrize("value", VALUES)
def test_every_case_decodes_from_its_encoded_value(value):
    assert ReferenceKind.from_encodable_string(value).encodable_string_representation == value


def test_an_unknown_value_is_rejected():
    with pytest.raises(DecodeError, match="Unexpected value"):
        ReferenceKind.from_encodable_string("not-a-case")
