from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Self

from xcodefy.errors.decode_error import DecodeError
from xcodefy.library.schema.values.relative_reference import RelativeReference
from xcodefy.library.serialization.decoders import Decoders
from xcodefy.library.serialization.values.value_type import ValueType
from xcodefy.library.utilities.text import Text

RELATIVE_NAMES = frozenset(reference.value for reference in RelativeReference)


@dataclass(frozen=True, slots=True)
class NamePathComponent:
    relative: RelativeReference | None = None
    name: str | None = None

    def __post_init__(self) -> None:
        if (self.relative is None) == (self.name is None):
            raise DecodeError("A name path component is either a relative reference or a child name.")

    @classmethod
    def child(cls, name: str) -> Self:
        return cls(name=name)

    @classmethod
    def of_relative(cls, relative: RelativeReference) -> Self:
        return cls(relative=relative)

    @staticmethod
    def can_losslessly_encode(name: str, requires_slash_validation: bool = True, requires_relative_reference_validation: bool = True) -> bool:
        if requires_slash_validation and "/" in name:
            return False
        return not (requires_relative_reference_validation and name in RELATIVE_NAMES)

    @property
    def lossless_string_encoding(self) -> str | None:
        if self.relative is not None:
            return self.relative.value
        return self.name if NamePathComponent.can_losslessly_encode(self.name) else None

    @property
    def child_name(self) -> str | None:
        return self.name

    @classmethod
    def from_lossless_string(cls, value: str, requires_slash_validation: bool = True) -> Self:
        if value in RELATIVE_NAMES:
            return cls.of_relative(RelativeReference(value))
        if not NamePathComponent.can_losslessly_encode(value, requires_slash_validation, False):
            raise DecodeError(f"The value {Text.smart_quoted(value)} is not losslessly representable as a group path component.")
        return cls.child(value)

    def encode(self, coder: Any) -> None:
        encoding = self.lossless_string_encoding
        if encoding is not None:
            coder.encode_string(encoding)
            return
        container = coder.keyed()
        container.put_unconditionally("name", self.name)

    @classmethod
    def decode(cls, coder: Any) -> Self:
        if coder.current_node_type is ValueType.STRING:
            return cls.from_lossless_string(coder.decode_string())
        return cls.child(coder.keyed().get("name", Decoders.string))

    def __str__(self) -> str:
        return self.relative.value if self.relative is not None else self.name
