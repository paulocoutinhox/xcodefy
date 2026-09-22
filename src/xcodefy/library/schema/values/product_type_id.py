from __future__ import annotations

from dataclasses import dataclass

from xcodefy.library.schema.values.typed_string_wrapper import TypedStringWrapper
from xcodefy.library.utilities.text import Text

ABBREVIATABLE_PREFIX = "com.apple.product-type."


@dataclass(frozen=True, slots=True)
class ProductTypeID(TypedStringWrapper):
    @property
    def abbreviated_representation(self) -> str | None:
        return Text.dropping_required_prefix(self.raw_value, ABBREVIATABLE_PREFIX)

    @classmethod
    def from_abbreviated(cls, value: str) -> ProductTypeID:
        return cls(ABBREVIATABLE_PREFIX + value)
