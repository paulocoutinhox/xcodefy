from xcodefy.library.schema.values.folder_member_id import FolderMemberID
from xcodefy.library.schema.values.typed_string_wrapper import TypedStringWrapper
from xcodefy.library.serialization.decoder import Decoder
from xcodefy.library.serialization.encoder import Encoder
from xcodefy.library.serialization.values.value import Value


def test_the_wrapper_carries_a_raw_string():
    assert FolderMemberID("value").raw_value == "value"
    assert str(FolderMemberID("value")) == "value"
    assert isinstance(FolderMemberID("value"), TypedStringWrapper)


def test_the_wrapper_encodes_and_decodes_as_a_bare_string():
    assert Encoder.json_for(FolderMemberID("value")) == Value.string("value")
    assert Decoder.decode_value(Value.string("value"), FolderMemberID) == FolderMemberID("value")


def test_wrappers_of_different_types_never_compare_equal():
    assert FolderMemberID("value") != TypedStringWrapper("value")
    assert FolderMemberID("value") == FolderMemberID("value")


def test_the_wrapper_is_hashable_so_it_can_live_in_a_set():
    assert len({FolderMemberID("a"), FolderMemberID("a"), FolderMemberID("b")}) == 2
