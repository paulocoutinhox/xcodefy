import pytest

from xcodefy.errors.validation_error import ValidationError
from xcodefy.library.serialization.values.comment import Comment
from xcodefy.library.serialization.values.comment_style import CommentStyle


@pytest.mark.parametrize("content", ["/*", "*/"])
def test_a_block_comment_rejects_internal_terminators(content):
    with pytest.raises(ValidationError, match="internal terminators"):
        Comment(CommentStyle.BLOCK, content)


@pytest.mark.parametrize("content", ["/*", "*/"])
def test_a_line_comment_accepts_block_terminators(content):
    assert Comment(CommentStyle.LINE, content).content == content


def test_only_a_single_line_block_comment_allows_compact_printing():
    assert Comment(CommentStyle.BLOCK, "one line").allows_compact_printing is True
    assert Comment(CommentStyle.BLOCK, "two\nlines").allows_compact_printing is False
    assert Comment(CommentStyle.LINE, "one line").allows_compact_printing is False
