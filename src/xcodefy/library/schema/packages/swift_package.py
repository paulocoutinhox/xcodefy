from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Self

from xcodefy.library.schema.packages.swift_package_location import SwiftPackageLocation
from xcodefy.library.serialization.decoders import Decoders


@dataclass(slots=True)
class SwiftPackage:
    location: SwiftPackageLocation
    traits: list[str] = field(default_factory=list)

    def encode(self, coder: Any) -> None:
        container = coder.keyed()
        container.put_inline(self.location)
        container.put("traits", self.traits, [])

    @classmethod
    def decode(cls, coder: Any) -> Self:
        container = coder.keyed()
        location = container.get_inline(SwiftPackageLocation)
        return cls(location, container.get_or_default("traits", Decoders.array_of(Decoders.string), []))
