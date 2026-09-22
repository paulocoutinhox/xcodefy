from xcodefy.library.schema.values.local_target_reference import LocalTargetReference
from xcodefy.library.schema.values.typed_string_wrapper import TypedStringWrapper
from xcodefy.library.serialization.decoder import Decoder
from xcodefy.library.serialization.encoder import Encoder
from xcodefy.library.serialization.values.value import Value


def test_the_wrapper_carries_a_raw_string():
    assert LocalTargetReference("value").raw_value == "value"
    assert str(LocalTargetReference("value")) == "value"
    assert isinstance(LocalTargetReference("value"), TypedStringWrapper)


def test_the_wrapper_encodes_and_decodes_as_a_bare_string():
    assert Encoder.json_for(LocalTargetReference("value")) == Value.string("value")
    assert Decoder.decode_value(Value.string("value"), LocalTargetReference) == LocalTargetReference("value")


def test_wrappers_of_different_types_never_compare_equal():
    assert LocalTargetReference("value") != TypedStringWrapper("value")
    assert LocalTargetReference("value") == LocalTargetReference("value")


def test_the_wrapper_is_hashable_so_it_can_live_in_a_set():
    assert len({LocalTargetReference("a"), LocalTargetReference("a"), LocalTargetReference("b")}) == 2
