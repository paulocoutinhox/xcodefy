from __future__ import annotations

import re
from dataclasses import dataclass, field
from math import isfinite

from xcodefy.errors.decode_error import DecodeError
from xcodefy.library.serialization.values.comment import Comment
from xcodefy.library.serialization.values.comment_style import CommentStyle
from xcodefy.library.serialization.values.field import Field
from xcodefy.library.serialization.values.field_or_comment import FieldOrComment
from xcodefy.library.serialization.values.value import Value
from xcodefy.library.serialization.values.value_or_comment import ValueOrComment

HEXADECIMAL = re.compile(r"[0-9A-Fa-f]+")
HEXADECIMAL_LITERAL = re.compile(r"[+-]?0[xX][0-9A-Fa-f]+")
NUMBER_CHARACTERS = "+-0123456789abcdefABCDEFxX.eE"
IDENTIFIER_START = "_$"
IDENTIFIER_BODY = "_$-"
QUOTES = frozenset({'"', "'"})
MAXIMUM_NESTING_DEPTH = 128
HIGH_SURROGATES = range(0xD800, 0xDC00)
LOW_SURROGATES = range(0xDC00, 0xE000)
SURROGATE_OFFSET = 0x10000 - (0xD800 << 10) - 0xDC00
ESCAPES = {'"': '"', "'": "'", "\\": "\\", "/": "/", "b": "\b", "f": "\f", "n": "\n", "r": "\r", "t": "\t", "v": "\v", "0": "\0"}


@dataclass(slots=True)
class Parser:
    text: str
    index: int = field(default=0, init=False)
    depth: int = field(default=0, init=False)

    def parse(self) -> Value:
        self.index = 0
        self.depth = 0
        self._skip_whitespace()
        value = self._parse_value()
        self._skip_trivia()
        if self.index != len(self.text):
            raise self._error("Unexpected trailing content")
        return value

    def _parse_value(self) -> Value:
        self._skip_trivia()
        if self.index >= len(self.text):
            raise self._error("Expected a value")
        character = self.text[self.index]
        if character == "{":
            return self._parse_object()
        if character == "[":
            return self._parse_array()
        if character in QUOTES:
            return Value.string(self._parse_string())
        if character in "+-.0123456789":
            return self._parse_number()
        identifier = self._parse_identifier()
        if identifier == "true":
            return Value.boolean(True)
        if identifier == "false":
            return Value.boolean(False)
        if identifier == "null":
            return Value.null()
        raise self._error(f"Unexpected identifier {identifier!r}")

    def _parse_object(self) -> Value:
        self._enter()
        self.index += 1
        entries: list[FieldOrComment] = []
        self._skip_whitespace()
        while not self._consume("}"):
            if self._collect_comment(entries, FieldOrComment):
                continue
            key = self._parse_key()
            self._skip_trivia()
            self._expect(":")
            self._skip_trivia()
            entries.append(FieldOrComment(field=Field(key, self._parse_value())))
            self._skip_whitespace()
            if self._consume(","):
                self._skip_whitespace()
                continue
            if self._peek() != "}" and not self._at_comment():
                raise self._error("Expected ',' or '}'")
        self.depth -= 1
        return Value.object(entries)

    def _parse_array(self) -> Value:
        self._enter()
        self.index += 1
        entries: list[ValueOrComment] = []
        self._skip_whitespace()
        while not self._consume("]"):
            if self._collect_comment(entries, ValueOrComment):
                continue
            entries.append(ValueOrComment(value=self._parse_value()))
            self._skip_whitespace()
            if self._consume(","):
                self._skip_whitespace()
                continue
            if self._peek() != "]" and not self._at_comment():
                raise self._error("Expected ',' or ']'")
        self.depth -= 1
        return Value.array(entries)

    def _collect_comment(self, entries: list, entry_type: type) -> bool:
        comment = self._parse_comment_if_present()
        if comment is None:
            return False
        entries.append(entry_type(comment=comment))
        self._skip_whitespace()
        return True

    def _parse_key(self) -> str:
        self._skip_trivia()
        if self._peek() in QUOTES:
            return self._parse_string()
        identifier = self._parse_identifier()
        if not identifier:
            raise self._error("Expected an object key")
        return identifier

    def _parse_string(self) -> str:
        quote = self._peek()
        self.index += 1
        parts: list[str] = []
        while self.index < len(self.text):
            character = self.text[self.index]
            self.index += 1
            if character == quote:
                return "".join(parts)
            if character != "\\":
                parts.append(character)
                continue
            parts.append(self._parse_escape())
        raise self._error("Unterminated string")

    def _parse_escape(self) -> str:
        if self.index >= len(self.text):
            raise self._error("Unterminated string escape")
        escaped = self.text[self.index]
        self.index += 1
        if escaped in ESCAPES:
            return ESCAPES[escaped]
        if escaped == "u":
            return self._parse_unicode_escape()
        if escaped == "x":
            return chr(self._parse_hexadecimal(2))
        if escaped == "\r" and self._peek() == "\n":
            self.index += 1
            return ""
        if escaped in {"\n", "\r", " ", " "}:
            return ""
        raise self._error(f"Invalid string escape {escaped!r}")

    def _enter(self) -> None:
        self.depth += 1
        if self.depth > MAXIMUM_NESTING_DEPTH:
            raise self._error(f"Nesting is deeper than {MAXIMUM_NESTING_DEPTH} levels")

    def _parse_unicode_escape(self) -> str:
        code_point = self._parse_hexadecimal(4)
        if code_point in HIGH_SURROGATES:
            return chr((code_point << 10) + self._parse_low_surrogate() + SURROGATE_OFFSET)
        if code_point in LOW_SURROGATES:
            raise self._error("Unpaired low surrogate in string escape")
        return chr(code_point)

    def _parse_low_surrogate(self) -> int:
        if not self.text.startswith("\\u", self.index):
            raise self._error("Unpaired high surrogate in string escape")
        self.index += 2
        code_point = self._parse_hexadecimal(4)
        if code_point not in LOW_SURROGATES:
            raise self._error("Unpaired high surrogate in string escape")
        return code_point

    def _parse_hexadecimal(self, count: int) -> int:
        chunk = self.text[self.index : self.index + count]
        if len(chunk) != count or HEXADECIMAL.fullmatch(chunk) is None:
            raise self._error("Invalid hexadecimal escape")
        self.index += count
        return int(chunk, 16)

    def _parse_number(self) -> Value:
        start = self.index
        while self.index < len(self.text) and self.text[self.index] in NUMBER_CHARACTERS:
            self.index += 1
        token = self.text[start : self.index]
        return self._number_value(token)

    def _number_value(self, token: str) -> Value:
        try:
            if HEXADECIMAL_LITERAL.fullmatch(token):
                return Value.integer(int(token, 16))
            if any(character in token for character in ".eE"):
                return self._finite_double(token)
            return Value.integer(int(token, 10))
        except ValueError as error:
            raise self._error(f"Invalid number {token!r}") from error

    def _finite_double(self, token: str) -> Value:
        number = float(token)
        if not isfinite(number):
            raise self._error(f"Number out of range {token!r}")
        return Value.double(number)

    def _parse_identifier(self) -> str:
        self._skip_trivia()
        start = self.index
        if self.index < len(self.text) and (self.text[self.index].isalpha() or self.text[self.index] in IDENTIFIER_START):
            self.index += 1
            while self.index < len(self.text) and (self.text[self.index].isalnum() or self.text[self.index] in IDENTIFIER_BODY):
                self.index += 1
        return self.text[start : self.index]

    def _at_comment(self) -> bool:
        return self.text.startswith("//", self.index) or self.text.startswith("/*", self.index)

    def _parse_comment_if_present(self) -> Comment | None:
        if self.text.startswith("//", self.index):
            return self._parse_line_comment()
        if self.text.startswith("/*", self.index):
            return self._parse_block_comment()
        return None

    def _parse_line_comment(self) -> Comment:
        self.index += 2
        if self._peek() == " ":
            self.index += 1
        start = self.index
        while self.index < len(self.text) and self.text[self.index] not in "\r\n":
            self.index += 1
        return Comment(CommentStyle.LINE, self.text[start : self.index])

    def _parse_block_comment(self) -> Comment:
        self.index += 2
        start = self.index
        end = self.text.find("*/", self.index)
        if end < 0:
            raise self._error("Unterminated block comment")
        content = self.text[start:end]
        self.index = end + 2
        return Comment(CommentStyle.BLOCK, self._trimmed_block_content(content))

    def _trimmed_block_content(self, content: str) -> str:
        if content.startswith(" ") and content.endswith(" "):
            return content[1:-1]
        return content

    def _skip_trivia(self) -> None:
        self._skip_whitespace()
        while self._at_comment():
            self._parse_comment_if_present()
            self._skip_whitespace()

    def _skip_whitespace(self) -> None:
        while self.index < len(self.text) and self.text[self.index].isspace():
            self.index += 1

    def _peek(self) -> str:
        return self.text[self.index] if self.index < len(self.text) else ""

    def _consume(self, token: str) -> bool:
        if self.text.startswith(token, self.index):
            self.index += len(token)
            return True
        return False

    def _expect(self, token: str) -> None:
        if not self._consume(token):
            raise self._error(f"Expected {token!r}")

    def _error(self, message: str) -> DecodeError:
        line = self.text.count("\n", 0, self.index) + 1
        column = self.index - self.text.rfind("\n", 0, self.index)
        return DecodeError(f"{message} at line {line}, column {column}.")
