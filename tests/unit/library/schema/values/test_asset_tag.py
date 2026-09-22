from xcodefy.library.schema.values.asset_tag import AssetTag
from xcodefy.library.schema.values.typed_string_wrapper import TypedStringWrapper
from xcodefy.library.serialization.decoder import Decoder
from xcodefy.library.serialization.encoder import Encoder
from xcodefy.library.serialization.values.value import Value


def test_the_wrapper_carries_a_raw_string():
    assert AssetTag("value").raw_value == "value"
    assert str(AssetTag("value")) == "value"
    assert isinstance(AssetTag("value"), TypedStringWrapper)


def test_the_wrapper_encodes_and_decodes_as_a_bare_string():
    assert Encoder.json_for(AssetTag("value")) == Value.string("value")
    assert Decoder.decode_value(Value.string("value"), AssetTag) == AssetTag("value")


def test_wrappers_of_different_types_never_compare_equal():
    assert AssetTag("value") != TypedStringWrapper("value")
    assert AssetTag("value") == AssetTag("value")


def test_the_wrapper_is_hashable_so_it_can_live_in_a_set():
    assert len({AssetTag("a"), AssetTag("a"), AssetTag("b")}) == 2
