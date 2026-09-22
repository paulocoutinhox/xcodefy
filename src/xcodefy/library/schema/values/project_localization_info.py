from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Self

from xcodefy.errors.validation_error import ValidationError
from xcodefy.library.schema.values.language import Language
from xcodefy.library.serialization.decoders import Decoders


@dataclass(frozen=True, slots=True)
class ProjectLocalizationInfo:
    development: Language
    supported: frozenset[Language] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if self.development in self.supported:
            raise ValidationError("The supported languages must not contain the development language.")

    @property
    def all_languages(self) -> frozenset[Language]:
        return self.supported | {self.development}

    def encode(self, coder: Any) -> None:
        container = coder.keyed()
        container.put_unconditionally("development", self.development)
        container.put("supported", self.supported, frozenset())

    @classmethod
    def decode(cls, coder: Any) -> Self:
        container = coder.keyed()
        development = container.get("development", Language)
        supported = container.get_or_default("supported", Decoders.set_of(Language), frozenset())
        return cls(development, supported)
