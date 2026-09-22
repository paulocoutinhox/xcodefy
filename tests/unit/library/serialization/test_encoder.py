import pytest

from xcodefy.errors.encode_error import EncodeError
from xcodefy.library.schema.values.object_id import ObjectID
from xcodefy.library.serialization.compact_array import CompactArray
from xcodefy.library.serialization.compact_dictionary import CompactDictionary
from xcodefy.library.serialization.encoder import Encoder
from xcodefy.library.serialization.encoding_options import EncodingOptions
from xcodefy.library.serialization.printing_density import PrintingDensity
from xcodefy.library.serialization.values.value import Value


class Silent:
    def encode(self, coder):
        return None


class Greedy:
    def encode(self, coder):
        coder.keyed()
        coder.keyed()


@pytest.mark.parametrize(("method", "argument", "expected"), [("encode_string", "a", Value.string("a")), ("encode_boolean", False, Value.boolean(False)), ("encode_integer", 3, Value.integer(3)), ("encode_double", 0.5, Value.double(0.5))])
def test_every_typed_primitive_helper_opens_a_primitive_container(method, argument, expected):
    encoder = Encoder()
    getattr(encoder, method)(argument)
    assert encoder.current.finish() == expected


def test_a_value_that_writes_nothing_encodes_as_an_empty_object():
    assert Encoder.json_for(Silent()) == Value.object([])


def test_a_value_that_opens_two_containers_is_rejected():
    with pytest.raises(EncodeError, match="more than one container"):
        Encoder.json_for(Greedy())


def test_sets_encode_in_coding_order():
    assert Encoder.json_for({ObjectID("b"), ObjectID("a")}).to_python() == ["a", "b"]


def test_mappings_encode_with_sorted_keys():
    assert [entry.field.key for entry in Encoder.json_for({"b": 1, "a": 2}).content.fields_or_comments] == ["a", "b"]


def test_a_compact_array_marks_each_element_compact():
    encoder = Encoder()
    encoder.encode_child(CompactArray.of([[1]]))
    assert PrintingDensity.COMPACT in encoder.densities.values()


def test_a_compact_dictionary_marks_each_value_compact():
    encoder = Encoder()
    encoder.encode_child(CompactDictionary.of({"a": [1]}))
    assert PrintingDensity.COMPACT in encoder.densities.values()


def test_tuples_encode_like_lists():
    assert Encoder.json_for((1, 2)).to_python() == [1, 2]


def test_text_and_data_share_the_same_rendering():
    assert Encoder.data_for([1], EncodingOptions.default()) == Encoder.text_for([1], EncodingOptions.default()).encode("utf-8")


@pytest.mark.parametrize("value", [object(), Encoder(), ("nested", object())])
def test_a_value_that_cannot_be_encoded_reports_its_type(value):
    with pytest.raises(EncodeError, match="cannot be encoded"):
        Encoder.text_for(value, EncodingOptions.default())


def test_the_reported_type_names_the_offending_value():
    with pytest.raises(EncodeError, match="A value of type Encoder cannot be encoded."):
        Encoder.json_for(Encoder())
