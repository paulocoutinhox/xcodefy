from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Self


@dataclass(frozen=True, slots=True)
class TypedStringWrapper:
    raw_value: str

    @property
    def encodable_string_representation(self) -> str:
        return self.raw_value

    @classmethod
    def from_encodable_string(cls, value: str) -> Self:
        return cls(value)

    @classmethod
    def decode(cls, coder: Any) -> Self:
        return cls.from_encodable_string(coder.decode_string())

    def encode(self, coder: Any) -> None:
        coder.encode_string(self.encodable_string_representation)

    def __str__(self) -> str:
        return self.raw_value
