from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Self

from xcodefy.library.schema.packages.swift_package_version_constraint import SwiftPackageVersionConstraint
from xcodefy.library.serialization.decoders import Decoders
from xcodefy.library.serialization.inline_keyed_codable import InlineKeyedCodable


@dataclass(slots=True)
class RemoteSwiftPackage(InlineKeyedCodable):
    repository_url: str = ""
    version_constraint: SwiftPackageVersionConstraint | None = None

    def encode_inline(self, container: Any) -> None:
        container.put_unconditionally("repository", self.repository_url)
        container.put("version", self.version_constraint, None)

    @classmethod
    def decode_inline(cls, container: Any) -> Self:
        repository_url = container.get("repository", Decoders.string)
        return cls(repository_url, container.get_optional("version", SwiftPackageVersionConstraint))
