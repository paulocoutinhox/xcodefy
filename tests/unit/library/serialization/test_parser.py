import json

import pytest

from xcodefy.errors.decode_error import DecodeError
from xcodefy.library.serialization.parser import MAXIMUM_NESTING_DEPTH, Parser
from xcodefy.library.serialization.values.comment_style import CommentStyle
from xcodefy.library.serialization.values.value_type import ValueType


def parsed(text):
    return Parser(text).parse()


@pytest.mark.parametrize(("text", "expected"), [("null", None), ("true", True), ("false", False), ("1", 1), ("-1", 1 - 2), ("+1", 1), ("1.5", 1.5), ("1e2", 100.0), ("0x1F", 31), ('"a"', "a"), ("'a'", "a")])
def test_scalars_parse_to_python_values(text, expected):
    assert parsed(text).to_python() == expected


def test_arrays_and_objects_parse_with_trailing_commas():
    assert parsed("[1, 2,]").to_python() == [1, 2]
    assert parsed("{a: 1, b: 2,}").to_python() == {"a": 1, "b": 2}


def test_unquoted_and_quoted_keys_are_both_accepted():
    assert parsed("{ unquoted: 1, \"quoted\": 2, 'single': 3 }").to_python() == {"unquoted": 1, "quoted": 2, "single": 3}


def test_a_later_duplicate_key_is_preserved_in_the_tree():
    entries = parsed('{ "a": 1, "a": 2 }').content.fields_or_comments
    assert [entry.field.value.to_python() for entry in entries] == [1, 2]


@pytest.mark.parametrize(("text", "expected"), [(r'"\n"', "\n"), (r'"\t"', "\t"), (r'"\r"', "\r"), (r'"\b"', "\b"), (r'"\f"', "\f"), (r'"\v"', "\v"), (r'"\0"', "\0"), (r'"\/"', "/"), (r'"\\"', "\\"), (r'"A"', "A"), (r'"\x41"', "A"), (r'"\""', '"'), ("'\\''", "'")])
def test_string_escapes_are_decoded(text, expected):
    assert parsed(text).to_python() == expected


@pytest.mark.parametrize("text", ['"a\\\nb"', '"a\\\r\nb"', '"a\\ b"'])
def test_escaped_line_continuations_are_dropped(text):
    assert parsed(text).to_python() == "ab"


def test_line_and_block_comments_are_preserved():
    value = parsed("[\n  // note\n  1,\n  /* block */\n]")
    comments = [entry.comment for entry in value.content if entry.comment is not None]
    assert [(comment.style, comment.content) for comment in comments] == [(CommentStyle.LINE, "note"), (CommentStyle.BLOCK, "block")]


def test_comments_are_preserved_inside_objects():
    value = parsed("{\n  // note\n  a: 1,\n}")
    comments = [entry.comment for entry in value.content.fields_or_comments if entry.comment is not None]
    assert [comment.content for comment in comments] == ["note"]


def test_comments_are_skipped_around_values_and_keys():
    assert parsed("/* lead */ { /* k */ a /* c */ : /* v */ 1 } /* tail */").to_python() == {"a": 1}


def test_a_block_comment_keeps_asymmetric_padding():
    value = parsed("[ /*note */ ]")
    assert value.content[0].comment.content == "note "


@pytest.mark.parametrize("text", ["", "{", "[", "{a}", "[1 2]", "{a: 1 b: 2}", '"unterminated', "/* unterminated", "1 2", "unknown", '"\\u00zz"', '"\\q"', '"\\', "{,}", "0x", "{:1}"])
def test_malformed_documents_are_rejected(text):
    with pytest.raises(DecodeError):
        parsed(text)


def test_errors_report_a_line_and_column():
    with pytest.raises(DecodeError, match="line 2, column 3"):
        parsed("[\n  @\n]")


def test_an_empty_container_parses():
    assert parsed("[]").to_python() == []
    assert parsed("{}").to_python() == {}


def test_the_parser_tracks_value_types():
    assert parsed("1").type is ValueType.INTEGER
    assert parsed("1.0").type is ValueType.DOUBLE
    assert parsed("[]").type is ValueType.ARRAY
    assert parsed("{}").type is ValueType.OBJECT


def test_a_line_comment_without_a_leading_space_is_read():
    value = parsed("[\n  //note\n]")
    assert value.content[0].comment.content == "note"


@pytest.mark.parametrize("text", ["1e400", "-1e400", "[1e400]"])
def test_a_number_outside_the_double_range_is_rejected(text):
    with pytest.raises(DecodeError, match="Number out of range"):
        parsed(text)


def test_a_parser_can_be_reused():
    parser = Parser("[1]")
    assert parser.parse().to_python() == [1]
    assert parser.parse().to_python() == [1]


def test_the_read_position_is_not_a_constructor_argument():
    with pytest.raises(TypeError):
        Parser("[1]", 2)


def test_a_surrogate_pair_decodes_to_the_character_it_denotes():
    document = r'"\ud83d\ude05"'
    decoded = parsed(document).to_python()
    assert decoded == chr(0x1F605)
    assert decoded == json.loads(document)
    assert len(decoded) == 1


def test_a_basic_plane_escape_is_unaffected():
    document = r'"\u0041\u00e9"'
    assert parsed(document).to_python() == "Aé"


@pytest.mark.parametrize("text", [r'"\ud800"', r'"\udc00"', r'"\ud800x"', r'"\ud800A"', r'"\ud800\ud800"'])
def test_an_unpaired_surrogate_is_rejected(text):
    with pytest.raises(DecodeError, match="[Uu]npaired"):
        parsed(text)


def test_a_document_at_the_nesting_limit_parses():
    assert parsed("[" * MAXIMUM_NESTING_DEPTH + "]" * MAXIMUM_NESTING_DEPTH) is not None


@pytest.mark.parametrize("builder", [lambda depth: "[" * depth + "]" * depth, lambda depth: '{"a":' * depth + "1" + "}" * depth])
def test_a_document_past_the_nesting_limit_is_rejected(builder):
    with pytest.raises(DecodeError, match="Nesting is deeper"):
        parsed(builder(MAXIMUM_NESTING_DEPTH + 1))


def test_the_nesting_counter_is_reset_between_parses():
    parser = Parser("[" * MAXIMUM_NESTING_DEPTH + "]" * MAXIMUM_NESTING_DEPTH)
    parser.parse()
    assert parser.parse() is not None


HOSTILE = [
    "",
    " ",
    "{",
    "}",
    "[",
    "]",
    ",",
    ":",
    '"',
    "'",
    "//",
    "/*",
    "\\",
    "0x",
    "1e",
    "1e+",
    ".",
    "..",
    "+",
    "-",
    "{,}",
    "[,]",
    "{:}",
    "{a}",
    "[1 2]",
    '{"a"}',
    '{"a":}',
    "nul",
    "tru",
    "fals",
    '"\\u"',
    '"\\u00"',
    '"\\x"',
    '"\\',
    "﻿",
    "\x00",
    " ",
    "/**/",
    "/*/",
    "//\n",
    "{//\n}",
    "[//\n]",
    '{"a":1,,}',
    "[1,,2]",
    "{}}",
    "[]]",
    '"a',
    "'a",
    "0x",
    "1.2.3",
    "--1",
    "++1",
]


@pytest.mark.parametrize("text", HOSTILE)
def test_a_hostile_input_either_parses_or_reports_a_decode_error(text):
    try:
        value = parsed(text)
    except DecodeError as error:
        assert str(error) != ""
    else:
        assert value.to_python() is not Ellipsis
