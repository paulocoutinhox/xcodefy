import pytest

from xcodefy.errors.decode_error import DecodeError
from xcodefy.library.serialization.decoder import Decoder
from xcodefy.library.serialization.decoders import Decoders
from xcodefy.library.serialization.values.comment import Comment
from xcodefy.library.serialization.values.comment_style import CommentStyle
from xcodefy.library.serialization.values.value import Value
from xcodefy.library.serialization.values.value_or_comment import ValueOrComment


def test_elements_are_counted_and_read_by_index():
    container = Decoder(Value.from_python([1, 2])).ordinal()
    assert container.count == 2
    assert container.get(1, Decoders.integer) == 2


def test_comments_are_skipped():
    entries = [ValueOrComment(comment=Comment(CommentStyle.LINE, "note")), ValueOrComment(value=Value.integer(1))]
    container = Decoder(Value.array(entries)).ordinal()
    assert container.count == 1
    assert container.get(0, Decoders.integer) == 1


def test_a_non_array_is_rejected():
    with pytest.raises(DecodeError, match="Expected an instance of array"):
        Decoder(Value.integer(1)).ordinal()
