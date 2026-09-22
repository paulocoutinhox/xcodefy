import pytest

from xcodefy.errors.decode_error import DecodeError
from xcodefy.errors.validation_error import ValidationError
from xcodefy.library.serialization.decoder import Decoder
from xcodefy.library.serialization.decoders import Decoders
from xcodefy.library.serialization.path_component import PathComponent
from xcodefy.library.serialization.values.value import Value
from xcodefy.library.serialization.values.value_type import ValueType


class Exploding:
    @classmethod
    def decode(cls, coder):
        raise ValidationError("boom")


def test_the_current_node_type_is_exposed():
    assert Decoder(Value.string("a")).current_node_type is ValueType.STRING


def test_the_typed_primitive_helpers_read_scalars():
    assert Decoder(Value.string("a")).decode_string() == "a"
    assert Decoder(Value.boolean(True)).decode_boolean() is True
    assert Decoder(Value.integer(1)).decode_integer() == 1
    assert Decoder(Value.double(1.5)).decode_double() == 1.5


def test_the_tool_name_appears_in_capability_errors():
    assert Decoder(Value.null(), "Xcodefy").tool_name == "Xcodefy"


def test_resolve_accepts_both_a_type_and_a_callable():
    assert Decoder.resolve(Decoders.integer) is Decoders.integer
    assert Decoder.resolve(Exploding) == Exploding.decode


def test_decoding_text_accepts_bytes_and_strings():
    assert Decoder.decode_text("1", Decoders.integer) == 1
    assert Decoder.decode_text(b"1", Decoders.integer) == 1


def test_an_error_is_annotated_with_the_coding_path():
    with pytest.raises(DecodeError, match="at /files"):
        Decoder.decode_text('{ "files": [1] }', lambda coder: coder.keyed().get("files", Exploding))


def test_the_innermost_coding_path_is_kept():
    with pytest.raises(DecodeError, match=r"at /files\[0\]$"):
        Decoder.decode_text('{ "files": [1] }', lambda coder: coder.keyed().get("files", Decoders.array_of(Exploding)))


def test_the_coder_state_is_restored_after_a_child_decode():
    coder = Decoder(Value.integer(1))
    coder.decode_child(Value.integer(2), PathComponent(key="a"), Decoders.integer)
    assert coder.current == Value.integer(1)
    assert str(coder.path) == ""


def test_the_coder_state_is_restored_after_a_failure():
    coder = Decoder(Value.integer(1))
    with pytest.raises(DecodeError):
        coder.decode_child(Value.integer(2), PathComponent(key="a"), Exploding)
    assert str(coder.path) == ""


def test_a_wrapped_error_is_never_its_own_cause():
    with pytest.raises(DecodeError) as caught:
        Decoder.decode_text('{ "a": { "b": 1 } }', lambda coder: coder.keyed().get("a", Exploding))
    assert caught.value.__cause__ is not caught.value
    assert isinstance(caught.value.__cause__, ValidationError)


def test_a_top_level_failure_is_normalised_onto_a_decode_error():
    with pytest.raises(DecodeError) as caught:
        Decoder.decode_text("1", Exploding)
    assert caught.value.coding_path is None
    assert isinstance(caught.value.__cause__, ValidationError)


def test_bytes_that_are_not_utf8_report_a_decode_error():
    with pytest.raises(DecodeError, match="not valid UTF-8"):
        Decoder.decode_text(b'"caf\xe9"', Decoders.string)


def test_bytes_carrying_a_byte_order_mark_are_read():
    assert Decoder.decode_text(b"\xef\xbb\xbf1", Decoders.integer) == 1


def test_a_string_source_is_taken_as_is():
    assert Decoder.decoded_source("1") == "1"
