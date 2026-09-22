import pytest

from tests.support.round_trip import RoundTrip
from xcodefy.errors.decode_error import DecodeError
from xcodefy.library.schema.values.name_path_component import NamePathComponent
from xcodefy.library.schema.values.relative_reference import RelativeReference


def test_a_component_is_either_relative_or_a_child_name():
    assert NamePathComponent.child("a").child_name == "a"
    assert NamePathComponent.of_relative(RelativeReference.PARENT).child_name is None


@pytest.mark.parametrize("arguments", [{}, {"relative": RelativeReference.CURRENT, "name": "a"}])
def test_a_component_rejects_carrying_neither_or_both(arguments):
    with pytest.raises(DecodeError, match="relative reference or a child name"):
        NamePathComponent(**arguments)


@pytest.mark.parametrize(("name", "encodable"), [("a", True), ("a/b", False), (".", False), ("..", False), ("", True)])
def test_only_unambiguous_child_names_encode_losslessly(name, encodable):
    assert NamePathComponent.can_losslessly_encode(name) is encodable


def test_a_relative_component_always_has_a_lossless_encoding():
    assert NamePathComponent.of_relative(RelativeReference.PARENT).lossless_string_encoding == ".."


def test_an_ambiguous_child_name_has_no_lossless_encoding():
    assert NamePathComponent.child("..").lossless_string_encoding is None
    assert NamePathComponent.child("a/b").lossless_string_encoding is None


def test_a_relative_looking_string_decodes_as_a_relative_component():
    assert NamePathComponent.from_lossless_string("..") == NamePathComponent.of_relative(RelativeReference.PARENT)


def test_a_slash_bearing_component_string_is_rejected():
    with pytest.raises(DecodeError, match="not losslessly representable"):
        NamePathComponent.from_lossless_string("a/b")


def test_slash_validation_can_be_relaxed_for_pre_split_components():
    assert NamePathComponent.from_lossless_string("a/b", False) == NamePathComponent.child("a/b")


def test_an_unambiguous_child_encodes_as_a_bare_string():
    assert RoundTrip.text(NamePathComponent.child("a")) == '"a"\n'


def test_an_ambiguous_child_encodes_as_a_named_object():
    assert RoundTrip.text(NamePathComponent.child("..")) == '{\n  "name": "..",\n}\n'


def test_a_component_renders_for_diagnostics():
    assert str(NamePathComponent.child("a")) == "a"
    assert str(NamePathComponent.of_relative(RelativeReference.CURRENT)) == "."
