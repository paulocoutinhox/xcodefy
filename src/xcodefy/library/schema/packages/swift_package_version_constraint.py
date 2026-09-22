from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Self

from xcodefy.errors.decode_error import DecodeError
from xcodefy.library.schema.packages.swift_package_version_kind import SwiftPackageVersionKind
from xcodefy.library.serialization.decoders import Decoders
from xcodefy.library.serialization.inline_keyed_codable import InlineKeyedCodable
from xcodefy.library.utilities.text import Text

RANGE_SEPARATOR = "..<"
SIMPLE_KINDS = (SwiftPackageVersionKind.REVISION, SwiftPackageVersionKind.BRANCH, SwiftPackageVersionKind.VERSION, SwiftPackageVersionKind.UP_TO_NEXT_MINOR_VERSION, SwiftPackageVersionKind.UP_TO_NEXT_MAJOR_VERSION)
BASIC_VERSION_CHARACTERS = frozenset("0123456789.")


@dataclass(slots=True)
class SwiftPackageVersionConstraint(InlineKeyedCodable):
    kind: SwiftPackageVersionKind
    value: str = ""
    maximum: str = ""

    @classmethod
    def revision(cls, value: str) -> Self:
        return cls(SwiftPackageVersionKind.REVISION, value)

    @classmethod
    def branch(cls, value: str) -> Self:
        return cls(SwiftPackageVersionKind.BRANCH, value)

    @classmethod
    def version(cls, value: str) -> Self:
        return cls(SwiftPackageVersionKind.VERSION, value)

    @classmethod
    def up_to_next_minor_version(cls, value: str) -> Self:
        return cls(SwiftPackageVersionKind.UP_TO_NEXT_MINOR_VERSION, value)

    @classmethod
    def up_to_next_major_version(cls, value: str) -> Self:
        return cls(SwiftPackageVersionKind.UP_TO_NEXT_MAJOR_VERSION, value)

    @classmethod
    def version_range(cls, minimum: str, maximum: str) -> Self:
        return cls(SwiftPackageVersionKind.VERSION_RANGE, minimum, maximum)

    @staticmethod
    def is_basic_version_number(value: str) -> bool:
        return all(character in BASIC_VERSION_CHARACTERS for character in value)

    def encode_inline(self, container: Any) -> None:
        if self.kind is not SwiftPackageVersionKind.VERSION_RANGE:
            container.put_unconditionally(self.kind.value, self.value)
            return
        if self.is_basic_version_number(self.value) and self.is_basic_version_number(self.maximum):
            container.put_unconditionally("version-range", self.value + RANGE_SEPARATOR + self.maximum)
            return
        container.put_unconditionally("version-range-min", self.value)
        container.put_unconditionally("version-range-max", self.maximum)

    @classmethod
    def decode_inline(cls, container: Any) -> Self:
        for kind in SIMPLE_KINDS:
            value = container.get_if_present(kind.value, Decoders.string)
            if value is not None:
                return cls(kind, value)
        combined = container.get_if_present("version-range", Decoders.string)
        if combined is not None:
            return cls._decode_combined_range(combined)
        minimum = container.get("version-range-min", Decoders.string)
        return cls.version_range(minimum, container.get("version-range-max", Decoders.string))

    @classmethod
    def _decode_combined_range(cls, value: str) -> Self:
        bounds = Text.partition_at_only(value, RANGE_SEPARATOR)
        if bounds is None:
            raise DecodeError(f"Unexpected version range value {Text.smart_quoted(value)}.")
        return cls.version_range(bounds[0], bounds[1])
