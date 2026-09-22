import pytest

from xcodefy.errors.encode_error import EncodeError
from xcodefy.library.schema.values.object_id import ObjectID
from xcodefy.library.serialization.coding_order import CodingOrder


def test_a_plain_string_is_its_own_key():
    assert CodingOrder.key_string("a") == "a"


def test_a_typed_wrapper_uses_its_encodable_representation():
    assert CodingOrder.key_string(ObjectID("A1")) == "A1"


def test_a_value_without_a_string_representation_is_rejected():
    with pytest.raises(EncodeError, match="cannot be encoded as a string"):
        CodingOrder.key_string(1)
