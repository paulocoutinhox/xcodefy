from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Self

from xcodefy.errors.decode_error import DecodeError
from xcodefy.errors.validation_error import ValidationError
from xcodefy.library.schema.values.file_path_base import FilePathBase
from xcodefy.library.schema.values.file_path_base_kind import FilePathBaseKind
from xcodefy.library.serialization.decoders import Decoders
from xcodefy.library.serialization.inline_keyed_codable import InlineKeyedCodable
from xcodefy.library.utilities.path_names import PathNames
from xcodefy.library.utilities.text import Text
from xcodefy.library.utilities.unescape_status import UnescapeStatus

SOURCE_ROOT_PREFIX = "<USER:"


@dataclass(frozen=True, slots=True)
class FilePath(InlineKeyedCodable):
    base: FilePathBase = field(default_factory=FilePathBase.group)
    path: str = ""

    def __post_init__(self) -> None:
        is_absolute_path = self.path.startswith("/") or self.path.startswith("~")
        if is_absolute_path != (self.base.kind is FilePathBaseKind.ABSOLUTE):
            raise ValidationError(f"Base disagrees with absoluteness of path: {self.path}.")

    @property
    def name(self) -> str:
        return PathNames.last_path_component(self.path)

    @property
    def string_representation(self) -> str:
        variable = self.base.built_in_expansion_variable
        if variable is not None:
            return f"<{variable}>/{self.path}"
        if self.base.build_setting is not None:
            return f"{SOURCE_ROOT_PREFIX}{Text.escaping(self.base.build_setting, '>')}>/{self.path}"
        return Text.escaping(self.path, "<")

    @classmethod
    def from_string_representation(cls, value: str) -> Self:
        source_root = cls._from_source_root_encoding(value)
        if source_root is not None:
            return source_root
        if value.startswith("<"):
            return cls._from_expansion_encoding(value)
        base = FilePathBase.absolute() if value.startswith("/") else FilePathBase.group()
        return cls(base, Text.unescaping(value, "<"))

    @classmethod
    def _from_source_root_encoding(cls, value: str) -> Self | None:
        remaining = Text.dropping_required_prefix(value, SOURCE_ROOT_PREFIX)
        if remaining is None:
            return None
        result = Text.unescaping_until_error(remaining, ">")
        if result.status is UnescapeStatus.INVALID_ESCAPE_SEQUENCE:
            quoted = Text.smart_quoted("\\" + result.character)
            raise DecodeError(f"Invalid escape sequence {quoted} in {Text.smart_quoted(value)}.")
        if result.status is not UnescapeStatus.UNESCAPED_SEQUENCE:
            raise DecodeError(f"Invalid file path encoding {Text.smart_quoted(value)}.")
        path = Text.dropping_required_prefix(result.remaining, "/")
        if path is None:
            raise DecodeError(f"Invalid file path encoding {Text.smart_quoted(value)} - missing initial path separator.")
        return cls(FilePathBase.source_root(result.unescaped), path)

    @classmethod
    def _from_expansion_encoding(cls, value: str) -> Self:
        marker = value.find(">/")
        if marker < 0:
            raise DecodeError("Unterminated path base.")
        variable = value[1:marker]
        base = FilePathBase.from_expansion_variable(variable)
        if base is None:
            raise DecodeError(f"Invalid path base: {Text.smart_quoted(variable)}.")
        return cls(base, value[marker + 2 :])

    def encode_inline(self, container: Any) -> None:
        container.put("path", self.string_representation, "")

    @classmethod
    def decode_inline(cls, container: Any) -> Self:
        return cls.from_string_representation(container.get_or_default("path", Decoders.string, ""))

    def __str__(self) -> str:
        return self.string_representation
