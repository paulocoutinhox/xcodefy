import pytest

from xcodefy.errors.encode_error import EncodeError
from xcodefy.library.serialization.values.field import Field
from xcodefy.library.serialization.values.field_or_comment import FieldOrComment
from xcodefy.library.serialization.values.object import Object
from xcodefy.library.serialization.values.value import Value
from xcodefy.library.serialization.values.value_or_comment import ValueOrComment
from xcodefy.library.serialization.values.value_type import ValueType


def test_each_constructor_produces_the_matching_type():
    assert Value.null().type is ValueType.NULL
    assert Value.boolean(True).type is ValueType.BOOLEAN
    assert Value.integer(1).type is ValueType.INTEGER
    assert Value.double(1.5).type is ValueType.DOUBLE
    assert Value.string("a").type is ValueType.STRING
    assert Value.array([]).type is ValueType.ARRAY
    assert Value.object([]).type is ValueType.OBJECT


def test_an_object_accepts_both_an_object_and_an_entry_list():
    entries = [FieldOrComment(field=Field("k", Value.null()))]
    assert Value.object(entries) == Value.object(Object(entries))


def test_containers_and_scalars_are_told_apart():
    assert Value.integer(1).is_container is False
    assert Value.null().is_container is False
    assert Value.array([]).is_container is True
    assert Value.object([]).is_container is True


@pytest.mark.parametrize("value", [None, True, 1, 1.5, "a", [1, "b"], (1, "b"), {"k": 1}, {"k": [1, {"n": None}]}])
def test_python_values_convert_in_both_directions(value):
    assert Value.from_python(value).to_python() == (list(value) if isinstance(value, tuple) else value)


def test_an_unsupported_python_value_is_rejected():
    with pytest.raises(EncodeError, match="Unsupported JSON value type"):
        Value.from_python(object())


def test_a_dictionary_with_non_string_keys_is_rejected():
    with pytest.raises(EncodeError, match="Unsupported JSON value type"):
        Value.from_python({1: "a"})


def test_converting_to_python_skips_comments():
    array = Value.array([ValueOrComment(value=Value.integer(1))])
    assert array.to_python() == [1]
