from xcodefy.library.serialization.values.comment import Comment
from xcodefy.library.serialization.values.comment_style import CommentStyle
from xcodefy.library.serialization.values.field import Field
from xcodefy.library.serialization.values.field_or_comment import FieldOrComment
from xcodefy.library.serialization.values.object import Object
from xcodefy.library.serialization.values.value import Value


def test_an_object_defaults_to_no_entries():
    assert Object().fields_or_comments == []


def test_the_fields_view_skips_comments():
    field = FieldOrComment(field=Field("k", Value.null()))
    comment = FieldOrComment(comment=Comment(CommentStyle.LINE, "note"))
    assert Object([field, comment]).fields == [field]
