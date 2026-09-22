import pytest

from tests.support.round_trip import RoundTrip
from xcodefy.library.schema.values.multiline_text import MultilineText


@pytest.mark.parametrize(("text", "compact"), [("", True), ("one line", True), ("one line\n", True), ("one\ntwo", False), ("one\ntwo\n", False), ("\n", True), ("\n\n", False)])
def test_only_a_single_logical_line_encodes_as_a_string(text, compact):
    assert MultilineText(text).encodes_to_string is compact


def test_a_single_line_encodes_as_a_string():
    assert RoundTrip.text(MultilineText("echo hello")) == '"echo hello"\n'


def test_several_lines_encode_as_an_array():
    assert RoundTrip.text(MultilineText("one\ntwo")) == '[\n  "one",\n  "two",\n]\n'


def test_the_lines_view_splits_on_newlines():
    assert MultilineText("one\ntwo").lines == ["one", "two"]


@pytest.mark.parametrize("text", ["", "\n", "\n\n", "\n\n\n", "one", "one\n", "one\ntwo", "one\ntwo\n"])
def test_multiline_text_round_trips(text):
    RoundTrip.expect_equal(MultilineText(text), MultilineText)
