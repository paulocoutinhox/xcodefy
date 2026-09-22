from __future__ import annotations

import json
from dataclasses import dataclass, field

from xcodefy.library.serialization.absolute_path import AbsolutePath
from xcodefy.library.serialization.density_validator import DensityValidator
from xcodefy.library.serialization.encoding_options import EncodingOptions
from xcodefy.library.serialization.printing_density import PrintingDensity
from xcodefy.library.serialization.values.comment import Comment
from xcodefy.library.serialization.values.comment_style import CommentStyle
from xcodefy.library.serialization.values.field import Field
from xcodefy.library.serialization.values.object import Object
from xcodefy.library.serialization.values.value import Value
from xcodefy.library.serialization.values.value_type import ValueType

INDENT = "  "
BLOCK_COMMENT_CONTINUATION = "   "


@dataclass(slots=True)
class Printer:
    options: EncodingOptions = field(default_factory=EncodingOptions.default)
    densities: dict[AbsolutePath, PrintingDensity] = field(default_factory=dict)
    _parts: list[str] = field(default_factory=list, init=False)
    _depth: int = field(default=0, init=False)
    _at_line_start: bool = field(default=True, init=False)
    _single_line: bool = field(default=False, init=False)

    def print(self, root: Value) -> str:
        self._parts = []
        self._depth = 0
        self._at_line_start = True
        self._single_line = False
        self.densities = DensityValidator(dict(self.densities)).validated(root)
        self._emit_value(root, AbsolutePath())
        text = "".join(self._parts)
        return text + "\n" if self.options.add_trailing_newline else text

    def _append(self, text: str) -> None:
        if not text:
            return
        self._parts.append(text)
        self._at_line_start = text.endswith("\n")

    def _indent_if_at_line_start(self) -> None:
        if self._at_line_start:
            self._append(INDENT * self._depth)

    def _emit_value(self, value: Value, path: AbsolutePath) -> None:
        original_single_line = self._single_line
        self._single_line = original_single_line or self.densities.get(path) is PrintingDensity.COMPACT
        self._emit_content(value, path)
        self._single_line = original_single_line

    def _emit_content(self, value: Value, path: AbsolutePath) -> None:
        if value.type is ValueType.NULL:
            self._append("null")
        elif value.type is ValueType.BOOLEAN:
            self._append("true" if value.content else "false")
        elif value.type in {ValueType.INTEGER, ValueType.DOUBLE}:
            self._append(json.dumps(value.content, allow_nan=False))
        elif value.type is ValueType.STRING:
            self._append(self._quote(value.content))
        elif value.type is ValueType.ARRAY:
            self._emit_array(value.content, path)
        else:
            self._emit_object(value.content, path)

    def _quote(self, value: str) -> str:
        return json.dumps(value, ensure_ascii=False)

    def _emit_array(self, entries: list, path: AbsolutePath) -> None:
        if self._single_line:
            self._emit_compact_array(entries, path)
            return
        self._append("[\n")
        self._depth += 1
        value_index = 0
        for entry_index, entry in enumerate(entries):
            self._indent_if_at_line_start()
            if not entry.is_value:
                self._emit_comment(entry.comment)
                self._append("\n")
                continue
            self._emit_value(entry.value, path.appending_index(value_index))
            value_index += 1
            self._append(self._array_separator(entries, entry_index, value_index, path))
        self._depth -= 1
        self._indent_if_at_line_start()
        self._append("]")

    def _emit_compact_array(self, entries: list, path: AbsolutePath) -> None:
        if not entries:
            self._append("[]")
            return
        value_count = sum(1 for entry in entries if entry.is_value)
        self._append("[ ")
        value_index = 0
        for entry in entries:
            if not entry.is_value:
                self._emit_comment(entry.comment)
                continue
            self._emit_value(entry.value, path.appending_index(value_index))
            value_index += 1
            if value_index != value_count:
                self._append(", ")
        self._append(" ]")

    def _array_separator(self, entries: list, entry_index: int, value_index: int, path: AbsolutePath) -> str:
        current = entries[entry_index].value
        following = entries[entry_index + 1].value if entry_index + 1 < len(entries) else None
        current_packs = current.is_container and not self._is_compact(path.appending_index(value_index - 1))
        following_packs = following is not None and following.is_container and not self._is_compact(path.appending_index(value_index))
        return ", " if current_packs and following_packs else ",\n"

    def _is_compact(self, path: AbsolutePath) -> bool:
        return self.densities.get(path) is PrintingDensity.COMPACT

    def _emit_object(self, content: Object, path: AbsolutePath) -> None:
        entries = content.fields_or_comments
        if self._single_line:
            self._emit_compact_object(entries, path)
            return
        self._append("{\n")
        self._depth += 1
        for entry in entries:
            self._indent_if_at_line_start()
            if entry.is_field:
                self._emit_field(entry.field, path)
                self._append(",\n")
            else:
                self._emit_comment(entry.comment)
                self._append("\n")
        self._depth -= 1
        self._indent_if_at_line_start()
        self._append("}")

    def _emit_compact_object(self, entries: list, path: AbsolutePath) -> None:
        if not entries:
            self._append("{}")
            return
        field_count = sum(1 for entry in entries if entry.is_field)
        self._append("{ ")
        field_index = 0
        for entry in entries:
            if not entry.is_field:
                self._emit_comment(entry.comment)
                continue
            self._emit_field(entry.field, path)
            field_index += 1
            if field_index != field_count:
                self._append(", ")
        self._append(" }")

    def _emit_field(self, content: Field, path: AbsolutePath) -> None:
        self._append(self._quote(content.key))
        self._append(": ")
        self._emit_value(content.value, path.appending_key(content.key))

    def _emit_comment(self, comment: Comment) -> None:
        if comment.style is CommentStyle.LINE:
            self._emit_line_comment(comment)
            return
        self._emit_block_comment(comment)

    def _emit_line_comment(self, comment: Comment) -> None:
        self._append("// ")
        for character in comment.content:
            if character in {"\n", "\r", " ", " "}:
                self._append("\n")
                self._indent_if_at_line_start()
                self._append("// ")
            else:
                self._append(character)
        self._indent_if_at_line_start()

    def _emit_block_comment(self, comment: Comment) -> None:
        outdented = comment.content.startswith("\n")
        self._append("/*")
        if not outdented:
            self._append(" ")
        for character in comment.content:
            if character in {"\n", "\r", " ", " "}:
                self._append("\n")
                self._indent_if_at_line_start()
                if not outdented:
                    self._append(BLOCK_COMMENT_CONTINUATION)
            else:
                self._append(character)
        if not outdented:
            self._append(" ")
        self._append("*/")
