import pytest

from xcodefy.errors.decode_error import DecodeError
from xcodefy.library.utilities.text import Text
from xcodefy.library.utilities.unescape_status import UnescapeStatus


def test_quoting_helpers_wrap_the_value():
    assert Text.smart_quoted("a") == "“a”"
    assert Text.quoted("a") == '"a"'


@pytest.mark.parametrize(("value", "expected"), [("a", False), ("a\nb", True), ("a\rb", True), ("a b", True), ("a b", True)])
def test_json_line_separators_are_detected(value, expected):
    assert Text.has_json_line_separator(value) is expected


@pytest.mark.parametrize(("value", "expected"), [("", False), ("build-phase", True), ("Build", False), ("a1", False), ("-a", False)])
def test_spear_case_requires_lowercase_ascii_and_hyphens(value, expected):
    assert Text.is_spear_case(value) is expected


def test_dropping_a_required_prefix_reports_a_mismatch():
    assert Text.dropping_required_prefix("id:1", "id:") == "1"
    assert Text.dropping_required_prefix("1", "id:") is None


def test_partition_at_only_requires_exactly_one_occurrence():
    assert Text.partition_at_only("1..<2", "..<") == ("1", "2")
    assert Text.partition_at_only("1..<2..<3", "..<") is None
    assert Text.partition_at_only("12", "..<") is None


@pytest.mark.parametrize(("values", "expected"), [([], ""), (["a"], "a"), (["a", "b"], "a and b"), (["a", "b", "c"], "a, b and c")])
def test_joining_uses_a_distinct_final_separator(values, expected):
    assert Text.joined_with_final_separator(values, ", ", " and ") == expected


def test_unescaping_until_error_reports_an_unresolved_trailing_escape():
    result = Text.unescaping_until_error("a\\", "<")
    assert result.status is UnescapeStatus.UNRESOLVED_ESCAPE


def test_unescaping_until_error_reports_an_invalid_sequence():
    result = Text.unescaping_until_error("\\q", "<")
    assert (result.status, result.character) == (UnescapeStatus.INVALID_ESCAPE_SEQUENCE, "q")


def test_unescaping_until_error_splits_at_an_unescaped_occurrence():
    result = Text.unescaping_until_error("ab<cd", "<")
    assert (result.status, result.unescaped, result.remaining) == (UnescapeStatus.UNESCAPED_SEQUENCE, "ab", "cd")


def test_unescaping_a_value_without_escapes_returns_it_unchanged():
    result = Text.unescaping_until_error("plain", "<")
    assert (result.status, result.unescaped) == (UnescapeStatus.COMPLETE, "plain")


def test_unescaping_raises_for_an_unresolved_escape():
    with pytest.raises(DecodeError, match="Invalid escape sequence in"):
        Text.unescaping("a\\", "<")
