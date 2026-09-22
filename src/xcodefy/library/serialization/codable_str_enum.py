from __future__ import annotations

from enum import StrEnum
from typing import Any, Self

from xcodefy.errors.decode_error import DecodeError


# Members are plain strings, so this type must never define an "encode" method: it would shadow
# "str.encode" for every caller. The encoder writes string enums through its own string branch.
class CodableStrEnum(StrEnum):
    @property
    def encodable_string_representation(self) -> str:
        return self.value

    @classmethod
    def from_encodable_string(cls, value: str) -> Self:
        try:
            return cls(value)
        except ValueError as error:
            raise DecodeError(f"Unexpected value “{value}” for {cls.__name__}.") from error

    @classmethod
    def decode(cls, coder: Any) -> Self:
        return cls.from_encodable_string(coder.decode_string())
