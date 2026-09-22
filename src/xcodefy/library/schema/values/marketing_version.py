from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Self

from xcodefy.errors.decode_error import DecodeError
from xcodefy.library.utilities.text import Text

DIGITS = frozenset("0123456789")


@dataclass(frozen=True, slots=True)
class MarketingVersion:
    major: int
    minor: int
    update: int = 0

    @property
    def encodable_string_representation(self) -> str:
        if self.update == 0:
            return f"{self.major}.{self.minor}"
        return f"{self.major}.{self.minor}.{self.update}"

    @classmethod
    def from_encodable_string(cls, value: str) -> Self:
        components = value.split(".")
        if len(components) not in {2, 3} or not all(MarketingVersion.is_integer(component) for component in components):
            raise DecodeError(f"Invalid version string {Text.smart_quoted(value)}.")
        numbers = [int(component) for component in components]
        return cls(numbers[0], numbers[1], numbers[2] if len(numbers) == 3 else 0)

    @staticmethod
    def is_integer(value: str) -> bool:
        return bool(value) and all(character in DIGITS for character in value)

    @classmethod
    def decode(cls, coder: Any) -> Self:
        return cls.from_encodable_string(coder.decode_string())

    def encode(self, coder: Any) -> None:
        coder.encode_string(self.encodable_string_representation)

    def __str__(self) -> str:
        return self.encodable_string_representation
