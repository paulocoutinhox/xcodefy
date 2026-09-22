from xcodefy.library.utilities.unescape_status import UnescapeStatus


def test_every_unescape_outcome_is_represented():
    assert [status.value for status in UnescapeStatus] == ["complete", "unescaped-sequence", "invalid-escape-sequence", "unresolved-escape"]
