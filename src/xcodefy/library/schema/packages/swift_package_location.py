from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Self

from xcodefy.errors.validation_error import ValidationError
from xcodefy.library.schema.packages.local_swift_package import LocalSwiftPackage
from xcodefy.library.schema.packages.remote_swift_package import RemoteSwiftPackage
from xcodefy.library.schema.packages.swift_package_location_kind import SwiftPackageLocationKind
from xcodefy.library.serialization.inline_keyed_codable import InlineKeyedCodable

CONTENT_TYPES = {SwiftPackageLocationKind.LOCAL: LocalSwiftPackage, SwiftPackageLocationKind.REMOTE: RemoteSwiftPackage}


@dataclass(slots=True)
class SwiftPackageLocation(InlineKeyedCodable):
    kind: SwiftPackageLocationKind
    content: Any

    def __post_init__(self) -> None:
        if not isinstance(self.content, CONTENT_TYPES[self.kind]):
            raise ValidationError(f"A {self.kind.value} package location requires {CONTENT_TYPES[self.kind].__name__}.")

    @classmethod
    def of_local(cls, content: LocalSwiftPackage) -> Self:
        return cls(SwiftPackageLocationKind.LOCAL, content)

    @classmethod
    def of_remote(cls, content: RemoteSwiftPackage) -> Self:
        return cls(SwiftPackageLocationKind.REMOTE, content)

    def encode_inline(self, container: Any) -> None:
        container.put_unconditionally("kind", self.kind)
        self.content.encode_inline(container)

    @classmethod
    def decode_inline(cls, container: Any) -> Self:
        kind = container.get("kind", SwiftPackageLocationKind)
        return cls(kind, CONTENT_TYPES[kind].decode_inline(container))
