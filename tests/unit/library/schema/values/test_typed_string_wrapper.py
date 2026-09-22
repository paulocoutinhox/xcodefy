from xcodefy.library.schema.values.typed_string_wrapper import TypedStringWrapper
from xcodefy.library.serialization.decoder import Decoder
from xcodefy.library.serialization.encoder import Encoder
from xcodefy.library.serialization.values.value import Value


def test_the_encodable_representation_is_the_raw_value():
    assert TypedStringWrapper("a").encodable_string_representation == "a"


def test_a_wrapper_is_built_from_its_encodable_representation():
    assert TypedStringWrapper.from_encodable_string("a") == TypedStringWrapper("a")


def test_a_wrapper_round_trips_as_a_bare_string():
    assert Encoder.json_for(TypedStringWrapper("a")) == Value.string("a")
    assert Decoder.decode_value(Value.string("a"), TypedStringWrapper) == TypedStringWrapper("a")


def test_a_wrapper_renders_as_its_raw_value():
    assert str(TypedStringWrapper("a")) == "a"
