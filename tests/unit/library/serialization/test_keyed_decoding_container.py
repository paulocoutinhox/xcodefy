import pytest

from xcodefy.errors.decode_error import DecodeError
from xcodefy.library.serialization.decoder import Decoder
from xcodefy.library.serialization.decoders import Decoders
from xcodefy.library.serialization.inline_keyed_codable import InlineKeyedCodable
from xcodefy.library.serialization.values.comment import Comment
from xcodefy.library.serialization.values.comment_style import CommentStyle
from xcodefy.library.serialization.values.field import Field
from xcodefy.library.serialization.values.field_or_comment import FieldOrComment
from xcodefy.library.serialization.values.value import Value


class Sample(InlineKeyedCodable):
    @classmethod
    def decode_inline(cls, container):
        return container.get("a", Decoders.integer)


def container(payload):
    return Decoder(Value.from_python(payload)).keyed()


def test_keys_are_listed_counted_and_probed():
    opened = container({"a": 1, "b": 2})
    assert opened.count == 2
    assert opened.keys == ["a", "b"]
    assert opened.contains("a") is True
    assert opened.contains("c") is False


def test_a_present_key_is_decoded():
    assert container({"a": 1}).get("a", Decoders.integer) == 1


def test_a_missing_required_key_is_reported_with_its_path():
    with pytest.raises(DecodeError, match="Missing required value for key"):
        container({}).get("a", Decoders.integer)


def test_a_missing_key_falls_back_to_the_default():
    assert container({}).get_or_default("a", Decoders.integer, 7) == 7
    assert container({"a": 1}).get_or_default("a", Decoders.integer, 7) == 1


def test_a_missing_optional_key_returns_nothing():
    assert container({}).get_if_present("a", Decoders.integer) is None
    assert container({"a": 1}).get_if_present("a", Decoders.integer) == 1


def test_an_inline_value_reuses_the_same_container():
    assert container({"a": 1}).get_inline(Sample) == 1


def test_a_later_duplicate_key_wins():
    entries = [FieldOrComment(field=Field("a", Value.integer(1))), FieldOrComment(field=Field("a", Value.integer(2)))]
    assert Decoder(Value.object(entries)).keyed().get("a", Decoders.integer) == 2


def test_comments_are_skipped():
    entries = [FieldOrComment(comment=Comment(CommentStyle.LINE, "note")), FieldOrComment(field=Field("a", Value.integer(1)))]
    assert Decoder(Value.object(entries)).keyed().count == 1


def test_a_non_object_is_rejected():
    with pytest.raises(DecodeError, match="Expected an instance of dictionary"):
        Decoder(Value.integer(1)).keyed()


def test_an_optional_field_treats_a_missing_key_and_an_explicit_null_alike():
    assert container({}).get_optional("a", Decoders.integer) is None
    assert container({"a": None}).get_optional("a", Decoders.integer) is None
    assert container({"a": 1}).get_optional("a", Decoders.integer) == 1


def test_an_optional_field_with_a_default_tells_absent_from_null():
    assert container({}).get_optional_with_default("a", Decoders.integer, 7) == 7
    assert container({"a": None}).get_optional_with_default("a", Decoders.integer, 7) is None
    assert container({"a": 1}).get_optional_with_default("a", Decoders.integer, 7) == 1


def test_a_present_only_field_rejects_an_explicit_null():
    with pytest.raises(DecodeError, match="Expected an instance of integer"):
        container({"a": None}).get_if_present("a", Decoders.integer)
