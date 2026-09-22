import pytest

from xcodefy.errors.decode_error import DecodeError
from xcodefy.library.utilities.text import Text


@pytest.mark.parametrize(("original", "escaped"), [("", ""), ("a", "a"), ("<", "\\<"), ("\\", "\\\\"), ("<<", "\\<\\<")])
def test_escaping_round_trips(original, escaped):
    assert Text.escaping(original, "<") == escaped
    assert Text.unescaping(escaped, "<") == original


@pytest.mark.parametrize("value", ["\\<", "\\"])
def test_unescaping_rejects_broken_escape_sequences(value):
    with pytest.raises(DecodeError):
        Text.unescaping(value, "j")


def test_unescaping_rejects_an_unescaped_occurrence_of_the_escaped_character():
    with pytest.raises(DecodeError, match="Missing escape sequence"):
        Text.unescaping("a<b", "<")
