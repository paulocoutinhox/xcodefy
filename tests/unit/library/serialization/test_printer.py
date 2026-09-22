from xcodefy.library.serialization.absolute_path import AbsolutePath
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


def test_scalars_print_in_json_form():
    assert Printer().print(Value.null()) == "null\n"
    assert Printer().print(Value.boolean(False)) == "false\n"
    assert Printer().print(Value.integer(-2)) == "-2\n"
    assert Printer().print(Value.double(1.5)) == "1.5\n"
    assert Printer().print(Value.string('a"b')) == '"a\\"b"\n'


def test_non_ascii_text_is_not_escaped():
    assert Printer().print(Value.string("café")) == '"café"\n'


def test_forward_slashes_are_not_escaped():
    assert Printer().print(Value.string("a/b")) == '"a/b"\n'


def test_the_trailing_newline_can_be_disabled():
    assert Printer(options=EncodingOptions(add_trailing_newline=False)).print(Value.integer(1)) == "1"


def test_a_printer_can_render_more_than_one_document():
    printer = Printer()
    assert printer.print(Value.integer(1)) == "1\n"
    assert printer.print(Value.integer(2)) == "2\n"


def test_a_carriage_return_inside_a_comment_starts_a_new_comment_line():
    array = Value.array([ValueOrComment(comment=Comment(CommentStyle.LINE, "a\rb"))])
    assert Printer().print(array) == "[\n  // a\n  // b\n]\n"


def test_a_compact_request_on_a_nested_container_is_honoured():
    inner = Value.array([ValueOrComment(value=Value.integer(1))])
    array = Value.array([ValueOrComment(value=inner)])
    densities = {ROOT.appending_index(0): PrintingDensity.COMPACT}
    assert Printer(densities=densities).print(array) == "[\n  [ 1 ],\n]\n"


def test_a_compact_array_separates_several_values():
    entries = [ValueOrComment(value=Value.integer(1)), ValueOrComment(value=Value.integer(2))]
    assert Printer(densities={ROOT: PrintingDensity.COMPACT}).print(Value.array(entries)) == "[ 1, 2 ]\n"


def test_a_compact_object_carries_an_inline_block_comment():
    entries = [FieldOrComment(comment=Comment(CommentStyle.BLOCK, "note")), FieldOrComment(field=Field("a", Value.integer(1)))]
    assert Printer(densities={ROOT: PrintingDensity.COMPACT}).print(Value.object(entries)) == '{ /* note */"a": 1 }\n'
