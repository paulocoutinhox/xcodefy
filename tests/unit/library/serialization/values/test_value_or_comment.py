import pytest

from xcodefy.errors.validation_error import ValidationError
from xcodefy.library.serialization.values.comment import Comment
from xcodefy.library.serialization.values.comment_style import CommentStyle
from xcodefy.library.serialization.values.value import Value
from xcodefy.library.serialization.values.value_or_comment import ValueOrComment


def test_an_entry_holds_either_a_value_or_a_comment():
    assert ValueOrComment(value=Value.null()).is_value is True
    assert ValueOrComment(comment=Comment(CommentStyle.LINE, "note")).is_value is False


@pytest.mark.parametrize("arguments", [{}, {"value": Value.null(), "comment": Comment(CommentStyle.LINE, "note")}])
def test_an_entry_rejects_carrying_neither_or_both(arguments):
    with pytest.raises(ValidationError, match="exactly one"):
        ValueOrComment(**arguments)
