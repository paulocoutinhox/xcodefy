from xcodefy.library.schema.values.swift_package_name import SwiftPackageName
from xcodefy.library.schema.values.typed_string_wrapper import TypedStringWrapper
from xcodefy.library.serialization.decoder import Decoder
from xcodefy.library.serialization.encoder import Encoder
from xcodefy.library.serialization.values.value import Value


def test_the_wrapper_carries_a_raw_string():
    assert SwiftPackageName("value").raw_value == "value"
    assert str(SwiftPackageName("value")) == "value"
    assert isinstance(SwiftPackageName("value"), TypedStringWrapper)


def test_the_wrapper_encodes_and_decodes_as_a_bare_string():
    assert Encoder.json_for(SwiftPackageName("value")) == Value.string("value")
    assert Decoder.decode_value(Value.string("value"), SwiftPackageName) == SwiftPackageName("value")


def test_wrappers_of_different_types_never_compare_equal():
    assert SwiftPackageName("value") != TypedStringWrapper("value")
    assert SwiftPackageName("value") == SwiftPackageName("value")


def test_the_wrapper_is_hashable_so_it_can_live_in_a_set():
    assert len({SwiftPackageName("a"), SwiftPackageName("a"), SwiftPackageName("b")}) == 2
