from xcodefy.library.serialization.values.comment_style import CommentStyle


def test_both_comment_styles_are_represented():
    assert [member.value for member in CommentStyle] == ["line", "block"]
