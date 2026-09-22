from xcodefy.library.utilities.unescape_result import UnescapeResult
from xcodefy.library.utilities.unescape_status import UnescapeStatus


def test_a_result_defaults_to_empty_payloads():
    result = UnescapeResult(UnescapeStatus.COMPLETE)
    assert (result.unescaped, result.remaining, result.character) == ("", "", "")


def test_a_result_carries_its_payload():
    result = UnescapeResult(UnescapeStatus.UNESCAPED_SEQUENCE, unescaped="a", remaining="b")
    assert (result.status, result.unescaped, result.remaining) == (UnescapeStatus.UNESCAPED_SEQUENCE, "a", "b")
