from xcodefy.library.serialization.absolute_path import AbsolutePath
from xcodefy.library.serialization.density_validator import DensityValidator
from xcodefy.library.serialization.printing_density import PrintingDensity
from xcodefy.library.serialization.values.comment import Comment
from xcodefy.library.serialization.values.comment_style import CommentStyle
from xcodefy.library.serialization.values.field import Field
from xcodefy.library.serialization.values.field_or_comment import FieldOrComment
from xcodefy.library.serialization.values.value import Value
from xcodefy.library.serialization.values.value_or_comment import ValueOrComment

ROOT = AbsolutePath()
COMPACT = {ROOT: PrintingDensity.COMPACT}


def validated(value, densities):
    return DensityValidator(dict(densities)).validated(value)


def test_a_scalar_keeps_a_compact_request():
    assert validated(Value.integer(1), COMPACT) == COMPACT


def test_a_container_of_scalars_keeps_a_compact_request():
    assert validated(Value.array([ValueOrComment(value=Value.string("a\nb"))]), COMPACT) == COMPACT


def test_a_line_comment_erases_a_compact_request():
    array = Value.array([ValueOrComment(comment=Comment(CommentStyle.LINE, "note"))])
    assert validated(array, COMPACT) == {}


def test_a_multiline_block_comment_erases_a_compact_request():
    array = Value.array([ValueOrComment(comment=Comment(CommentStyle.BLOCK, "a\nb"))])
    assert validated(array, COMPACT) == {}


def test_a_single_line_block_comment_keeps_a_compact_request():
    array = Value.array([ValueOrComment(comment=Comment(CommentStyle.BLOCK, "note"))])
    assert validated(array, COMPACT) == COMPACT


def test_a_comment_in_an_object_erases_a_compact_request():
    entries = [FieldOrComment(comment=Comment(CommentStyle.LINE, "note"))]
    assert validated(Value.object(entries), COMPACT) == {}


def test_a_nested_line_comment_erases_an_ancestor_request():
    inner = Value.array([ValueOrComment(comment=Comment(CommentStyle.LINE, "note"))])
    entries = [FieldOrComment(field=Field("a", inner))]
    assert validated(Value.object(entries), COMPACT) == {}


def test_a_later_good_comment_does_not_rescue_an_earlier_bad_one():
    inner = Value.array([ValueOrComment(comment=Comment(CommentStyle.LINE, "note"))])
    entries = [ValueOrComment(value=inner), ValueOrComment(comment=Comment(CommentStyle.BLOCK, "fine"))]
    assert validated(Value.array(entries), COMPACT) == {}


def test_a_request_on_a_clean_child_survives():
    child_path = ROOT.appending_index(0)
    densities = {child_path: PrintingDensity.COMPACT}
    array = Value.array([ValueOrComment(value=Value.array([]))])
    assert validated(array, densities) == densities
