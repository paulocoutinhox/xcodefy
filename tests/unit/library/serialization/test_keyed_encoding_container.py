import pytest

from xcodefy.errors.encode_error import EncodeError
from xcodefy.library.serialization.encoder import Encoder
from xcodefy.library.serialization.printing_density import PrintingDensity
from xcodefy.library.serialization.values.comment import Comment
from xcodefy.library.serialization.values.comment_style import CommentStyle


def test_a_value_equal_to_its_default_is_omitted():
    container = Encoder().keyed()
    container.put("name", "a", "a")
    container.put("other", "b", "a")
    assert container.finish().to_python() == {"other": "b"}


def test_an_unconditional_value_is_always_written():
    container = Encoder().keyed()
    container.put_unconditionally("name", "a")
    assert container.finish().to_python() == {"name": "a"}


def test_a_non_spear_case_key_is_rejected():
    with pytest.raises(EncodeError, match="not spear case"):
        Encoder().keyed().put_unconditionally("Name", "a")


def test_an_unverified_key_skips_the_spear_case_check():
    container = Encoder().keyed()
    container.put_unverified("SWIFT_VERSION", "6.0")
    assert container.finish().to_python() == {"SWIFT_VERSION": "6.0"}


def test_encoding_the_same_key_twice_is_rejected():
    container = Encoder().keyed()
    container.put_unverified("a", 1)
    with pytest.raises(EncodeError, match="multiple times"):
        container.put_unverified("a", 2)


def test_a_field_density_is_recorded_against_the_field_path():
    encoder = Encoder()
    container = encoder.keyed()
    container.put_unconditionally("names", ["a"], PrintingDensity.COMPACT)
    assert encoder.densities[container.path.appending_key("names")] is PrintingDensity.COMPACT


def test_an_absent_inline_value_writes_nothing():
    container = Encoder().keyed()
    container.put_inline(None)
    assert container.finish().to_python() == {}


def test_comments_are_interleaved_with_fields():
    container = Encoder().keyed()
    container.add_comment(Comment(CommentStyle.LINE, "note"))
    container.put_unconditionally("a", 1)
    assert [entry.is_field for entry in container.finish().content.fields_or_comments] == [False, True]
