from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Self

from xcodefy.library.schema.values.string_encoding import StringEncoding
from xcodefy.library.serialization.values.value_type import ValueType


@dataclass(frozen=True, slots=True)
class TextEncoding:
    raw_value: int

    @classmethod
    def of(cls, encoding: StringEncoding) -> Self:
        return cls(encoding.encoding_value)

    @property
    def string_encoding(self) -> StringEncoding | None:
        return StringEncoding.from_encoding_value(self.raw_value)

    def encode(self, coder: Any) -> None:
        named = self.string_encoding
        if named is None:
            coder.encode_integer(self.raw_value)
            return
        coder.encode_string(named.value)

    @classmethod
    def decode(cls, coder: Any) -> Self:
        if coder.current_node_type is ValueType.STRING:
            return cls.of(StringEncoding.decode(coder))
        return cls(coder.decode_integer())
