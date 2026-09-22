import pytest

from xcodefy.errors.validation_error import ValidationError
from xcodefy.library.serialization.values.comment import Comment
from xcodefy.library.serialization.values.comment_style import CommentStyle
from xcodefy.library.serialization.values.field import Field
from xcodefy.library.serialization.values.field_or_comment import FieldOrComment
from xcodefy.library.serialization.values.value import Value


def test_an_entry_holds_either_a_field_or_a_comment():
    assert FieldOrComment(field=Field("k", Value.null())).is_field is True
    assert FieldOrComment(comment=Comment(CommentStyle.LINE, "note")).is_field is False


@pytest.mark.parametrize("arguments", [{}, {"field": Field("k", Value.null()), "comment": Comment(CommentStyle.LINE, "note")}])
def test_an_entry_rejects_carrying_neither_or_both(arguments):
    with pytest.raises(ValidationError, match="exactly one"):
        FieldOrComment(**arguments)
