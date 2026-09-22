from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any, Self

from xcodefy.library.schema.values.name_path_component import NamePathComponent
from xcodefy.library.serialization.decoders import Decoders
from xcodefy.library.serialization.values.value_type import ValueType


@dataclass(frozen=True, slots=True)
class NamePath:
    components: tuple[NamePathComponent, ...] = ()

    @classmethod
    def of(cls, components: Iterable[NamePathComponent]) -> Self:
        return cls(tuple(components))

    @classmethod
    def of_child_names(cls, names: Iterable[str]) -> Self:
        return cls(tuple(NamePathComponent.child(name) for name in names))

    @property
    def lossless_path_representation(self) -> str | None:
        if not self.components:
            return None
        encodings = [component.lossless_string_encoding for component in self.components]
        return None if any(encoding is None for encoding in encodings) else "/".join(encodings)

    @classmethod
    def from_lossless_path(cls, value: str) -> Self:
        return cls(tuple(NamePathComponent.from_lossless_string(component, False) for component in value.split("/")))

    def encode(self, coder: Any) -> None:
        representation = self.lossless_path_representation
        if representation is not None:
            coder.encode_string(representation)
            return
        container = coder.ordinal()
        for component in self.components:
            container.put(component)

    @classmethod
    def decode(cls, coder: Any) -> Self:
        if coder.current_node_type is ValueType.STRING:
            return cls.from_lossless_path(coder.decode_string())
        return cls.of(Decoders.array_of(NamePathComponent)(coder))

    def __add__(self, other: NamePath) -> NamePath:
        return NamePath(self.components + other.components)

    def __str__(self) -> str:
        return "/".join(str(component) for component in self.components)
