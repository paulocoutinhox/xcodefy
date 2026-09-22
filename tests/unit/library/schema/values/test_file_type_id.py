from xcodefy.library.schema.values.file_type_id import FileTypeID
from xcodefy.library.schema.values.typed_string_wrapper import TypedStringWrapper
from xcodefy.library.serialization.decoder import Decoder
from xcodefy.library.serialization.encoder import Encoder
from xcodefy.library.serialization.values.value import Value


def test_the_wrapper_carries_a_raw_string():
    assert FileTypeID("value").raw_value == "value"
    assert str(FileTypeID("value")) == "value"
    assert isinstance(FileTypeID("value"), TypedStringWrapper)


def test_the_wrapper_encodes_and_decodes_as_a_bare_string():
    assert Encoder.json_for(FileTypeID("value")) == Value.string("value")
    assert Decoder.decode_value(Value.string("value"), FileTypeID) == FileTypeID("value")


def test_wrappers_of_different_types_never_compare_equal():
    assert FileTypeID("value") != TypedStringWrapper("value")
    assert FileTypeID("value") == FileTypeID("value")


def test_the_wrapper_is_hashable_so_it_can_live_in_a_set():
    assert len({FileTypeID("a"), FileTypeID("a"), FileTypeID("b")}) == 2
