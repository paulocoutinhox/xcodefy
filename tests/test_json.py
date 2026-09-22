import pytest

from tests.support.round_trip import RoundTrip
from xcodefy.library.serialization.absolute_path import AbsolutePath
from xcodefy.library.serialization.decoder import Decoder
from xcodefy.library.serialization.decoders import Decoders
from xcodefy.library.serialization.encoder import Encoder
from xcodefy.library.serialization.encoding_options import EncodingOptions
from xcodefy.library.serialization.printer import Printer
from xcodefy.library.serialization.printing_density import PrintingDensity
from xcodefy.library.serialization.values.comment import Comment
from xcodefy.library.serialization.values.comment_style import CommentStyle
from xcodefy.library.serialization.values.field import Field
from xcodefy.library.serialization.values.field_or_comment import FieldOrComment
from xcodefy.library.serialization.values.value import Value
from xcodefy.library.serialization.values.value_or_comment import ValueOrComment

ROOT = AbsolutePath()


def printed(value, densities=None):
    return Printer(densities=dict(densities or {})).print(value)


def lines(*values):
    return "\n".join(values) + "\n"


def array(*entries):
    return Value.array(list(entries))


def entry(value):
    return ValueOrComment(value=value)


def comment_entry(style, content):
    return ValueOrComment(comment=Comment(style, content))


def obj(**fields):
    return Value.object([FieldOrComment(field=Field(key, value)) for key, value in fields.items()])


def test_primitives_encode_to_the_expected_json_values():
    assert Encoder.json_for(None) == Value.null()
    assert Encoder.json_for(True) == Value.boolean(True)
    assert Encoder.json_for(-1) == Value.integer(-1)
    assert Encoder.json_for(1.5) == Value.double(1.5)
    assert Encoder.json_for("A") == Value.string("A")


def test_sequences_and_mappings_encode_to_the_expected_json_values():
    assert Encoder.json_for([False, True]) == array(entry(Value.boolean(False)), entry(Value.boolean(True)))
    assert Encoder.json_for({"off": False, "on": True}) == obj(off=Value.boolean(False), on=Value.boolean(True))
    assert Encoder.json_for({"b": 1, "a": 2}).content.fields_or_comments[0].field.key == "a"
    assert Encoder.json_for(frozenset({"b", "a"})) == array(entry(Value.string("a")), entry(Value.string("b")))


@pytest.mark.parametrize("value", [None, False, True, 0, 1, -1, 1.5, -1.5, "", "String"])
def test_primitive_values_round_trip(value):
    text = Encoder.text_for(value, EncodingOptions.default())
    assert Decoder.decode_text(text, lambda coder: coder.current.to_python()) == value


@pytest.mark.parametrize("code_point", range(0, 127))
def test_every_ascii_character_round_trips(code_point):
    RoundTrip.expect_equal(chr(code_point), Decoders.string)


def test_arrays_print_sprawling_by_default_and_compact_on_request():
    assert printed(array()) == lines("[", "]")
    assert printed(array(entry(Value.integer(1)))) == lines("[", "  1,", "]")
    assert printed(array(), {ROOT: PrintingDensity.COMPACT}) == lines("[]")
    assert printed(array(entry(Value.integer(1))), {ROOT: PrintingDensity.COMPACT}) == lines("[ 1 ]")


def test_objects_print_sprawling_by_default_and_compact_on_request():
    assert printed(Value.object([])) == lines("{", "}")
    assert printed(obj(key=Value.string("value"))) == lines("{", '  "key": "value",', "}")
    assert printed(Value.object([]), {ROOT: PrintingDensity.COMPACT}) == lines("{}")
    assert printed(obj(key=Value.string("value")), {ROOT: PrintingDensity.COMPACT}) == lines('{ "key": "value" }')


def test_comments_print_in_the_canonical_style():
    assert printed(array(entry(Value.integer(1)), comment_entry(CommentStyle.LINE, "Empty"))) == lines("[", "  1,", "  // Empty", "]")
    assert printed(array(comment_entry(CommentStyle.LINE, "Leading"), entry(Value.string("a string")))) == lines("[", "  // Leading", '  "a string",', "]")
    assert printed(array(comment_entry(CommentStyle.BLOCK, "Block"))) == lines("[", "  /* Block */", "]")
    assert printed(array(comment_entry(CommentStyle.BLOCK, "\nTwo Line\nOutdented Block\n"))) == lines("[", "  /*", "  Two Line", "  Outdented Block", "  */", "]")
    assert printed(array(comment_entry(CommentStyle.BLOCK, "Two Line\nBlock"))) == lines("[", "  /* Two Line", "     Block */", "]")


def test_comments_in_objects_print_on_their_own_lines():
    entries = [FieldOrComment(comment=Comment(CommentStyle.LINE, "Note")), FieldOrComment(field=Field("key", Value.string("value")))]
    assert printed(Value.object(entries)) == lines("{", "  // Note", '  "key": "value",', "}")


def test_a_compact_request_survives_escaped_newlines_but_not_line_comments():
    assert printed(array(entry(Value.string("Line1\nLine2"))), {ROOT: PrintingDensity.COMPACT}) == lines('[ "Line1\\nLine2" ]')
    assert printed(array(comment_entry(CommentStyle.LINE, "Empty")), {ROOT: PrintingDensity.COMPACT}) == lines("[", "  // Empty", "]")
    assert printed(array(comment_entry(CommentStyle.BLOCK, "Empty")), {ROOT: PrintingDensity.COMPACT}) == lines("[ /* Empty */ ]")
    assert printed(array(comment_entry(CommentStyle.BLOCK, "Line1\nLine2")), {ROOT: PrintingDensity.COMPACT}) == lines("[", "  /* Line1", "     Line2 */", "]")


def test_a_compact_request_is_erased_for_an_object_holding_a_line_comment():
    entries = [FieldOrComment(comment=Comment(CommentStyle.LINE, "Note"))]
    assert printed(Value.object(entries), {ROOT: PrintingDensity.COMPACT}) == lines("{", "  // Note", "}")


def test_runs_of_multiline_containers_pack_onto_shared_lines():
    first = obj(key=Value.string("value"))
    second = obj(key=Value.string("value2"))
    assert printed(array(entry(first))) == lines("[", "  {", '    "key": "value",', "  },", "]")
    assert printed(array(entry(first), entry(second))) == lines("[", "  {", '    "key": "value",', "  }, {", '    "key": "value2",', "  },", "]")
    assert printed(array(entry(first), entry(Value.integer(3)), entry(second))) == lines("[", "  {", '    "key": "value",', "  },", "  3,", "  {", '    "key": "value2",', "  },", "]")
    assert printed(array(entry(first), entry(Value.integer(3)))) == lines("[", "  {", '    "key": "value",', "  },", "  3,", "]")


def test_compact_children_do_not_pack_onto_shared_lines():
    first = obj(key=Value.string("value"))
    second = obj(key=Value.string("value2"))
    densities = {ROOT.appending_index(0): PrintingDensity.COMPACT, ROOT.appending_index(1): PrintingDensity.COMPACT}
    assert printed(array(entry(first)), {ROOT.appending_index(0): PrintingDensity.COMPACT}) == lines("[", '  { "key": "value" },', "]")
    assert printed(array(entry(first), entry(second)), densities) == lines("[", '  { "key": "value" },', '  { "key": "value2" },', "]")


def test_object_keys_are_escaped():
    assert printed(obj(**{"line1\nline2": Value.string("value")})) == lines("{", '  "line1\\nline2": "value",', "}")


def test_integer_and_floating_point_extremes_round_trip():
    for value in [-(2**63), 0, 2**63 - 1]:
        RoundTrip.expect_equal(value, Decoders.integer)
    for value in [1.7976931348623157e308, 3.141592653589793, 2.220446049250313e-16]:
        RoundTrip.expect_equal(value, Decoders.double)


def test_the_trailing_newline_is_optional():
    assert Encoder.text_for(1, EncodingOptions(add_trailing_newline=False)) == "1"
