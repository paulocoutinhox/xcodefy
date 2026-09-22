import pytest

from xcodefy.errors.decode_error import DecodeError
from xcodefy.library.schema.values.folder_member_id import FolderMemberID
from xcodefy.library.serialization.decoder import Decoder
from xcodefy.library.serialization.decoders import Decoders
from xcodefy.library.serialization.values.value import Value


def decoded(payload, decode):
    return Decoder.decode_value(Value.from_python(payload), decode)


def test_the_scalar_decoders_read_their_types():
    assert decoded(True, Decoders.boolean) is True
    assert decoded(1, Decoders.integer) == 1
    assert decoded(1.5, Decoders.double) == 1.5
    assert decoded("a", Decoders.string) == "a"


def test_array_of_decodes_every_element():
    assert decoded([1, 2], Decoders.array_of(Decoders.integer)) == [1, 2]


def test_set_of_collects_unique_elements():
    assert decoded(["a", "b"], Decoders.set_of(Decoders.string)) == frozenset({"a", "b"})


def test_set_of_rejects_duplicates():
    with pytest.raises(DecodeError, match="duplicate elements"):
        decoded(["a", "a"], Decoders.set_of(Decoders.string))


def test_dictionary_of_keeps_string_keys():
    assert decoded({"a": 1}, Decoders.dictionary_of(Decoders.integer)) == {"a": 1}


def test_keyed_dictionary_of_converts_the_keys():
    assert decoded({"a": 1}, Decoders.keyed_dictionary_of(FolderMemberID, Decoders.integer)) == {FolderMemberID("a"): 1}
