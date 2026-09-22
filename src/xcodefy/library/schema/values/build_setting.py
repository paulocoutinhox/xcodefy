from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any, Self

from xcodefy.errors.validation_error import ValidationError
from xcodefy.library.serialization.decoders import Decoders
from xcodefy.library.serialization.values.value_type import ValueType


@dataclass(frozen=True, slots=True)
class BuildSetting:
    string: str | None = None
    array: tuple[str, ...] | None = None

    def __post_init__(self) -> None:
        if (self.string is None) == (self.array is None):
            raise ValidationError("A build setting must be either a string or an array of strings.")
        if self.string is not None and not isinstance(self.string, str):
            raise ValidationError("A string build setting must hold a string.")
        if self.array is not None and not all(isinstance(value, str) for value in self.array):
            raise ValidationError("An array build setting must hold only strings.")

    @classmethod
    def of_string(cls, value: str) -> Self:
        return cls(string=value)

    @classmethod
    def of_array(cls, values: Iterable[str]) -> Self:
        return cls(array=tuple(values))

    def encode(self, coder: Any) -> None:
        if self.string is not None:
            coder.encode_string(self.string)
            return
        container = coder.ordinal()
        for value in self.array:
            container.put(value)

    @classmethod
    def decode(cls, coder: Any) -> Self:
        if coder.current_node_type is ValueType.STRING:
            return cls.of_string(coder.decode_string())
        return cls.of_array(Decoders.array_of(Decoders.string)(coder))
