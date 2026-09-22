from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Self

from xcodefy.errors.validation_error import ValidationError
from xcodefy.library.schema.target.dependencies.remote_target import RemoteTarget
from xcodefy.library.schema.target.dependencies.swift_package_product_reference import SwiftPackageProductReference
from xcodefy.library.schema.target.dependencies.target_dependency_kind import TargetDependencyKind
from xcodefy.library.schema.values.local_target_reference import LocalTargetReference
from xcodefy.library.schema.values.platform_filter import PlatformFilter
from xcodefy.library.serialization.decoders import Decoders
from xcodefy.library.serialization.printing_density import PrintingDensity
from xcodefy.library.serialization.values.value_type import ValueType

CONTENT_TYPES = {TargetDependencyKind.LOCAL_TARGET: LocalTargetReference, TargetDependencyKind.REMOTE_TARGET: RemoteTarget, TargetDependencyKind.PACKAGE: SwiftPackageProductReference}


@dataclass(slots=True)
class TargetDependency:
    kind: TargetDependencyKind
    content: Any
    platform_filters: frozenset[PlatformFilter] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not isinstance(self.content, CONTENT_TYPES[self.kind]):
            raise ValidationError(f"A {self.kind.value} dependency requires {CONTENT_TYPES[self.kind].__name__}.")

    @classmethod
    def of_local_target(cls, content: LocalTargetReference, platform_filters: Any = frozenset()) -> Self:
        return cls(TargetDependencyKind.LOCAL_TARGET, content, frozenset(platform_filters))

    @classmethod
    def of_remote_target(cls, content: RemoteTarget, platform_filters: Any = frozenset()) -> Self:
        return cls(TargetDependencyKind.REMOTE_TARGET, content, frozenset(platform_filters))

    @classmethod
    def of_package(cls, content: SwiftPackageProductReference, platform_filters: Any = frozenset()) -> Self:
        return cls(TargetDependencyKind.PACKAGE, content, frozenset(platform_filters))

    @property
    def encodes_to_string(self) -> bool:
        return self.kind is TargetDependencyKind.LOCAL_TARGET and not self.platform_filters

    def encode(self, coder: Any) -> None:
        if self.encodes_to_string:
            coder.encode_string(self.content.raw_value)
            return
        container = coder.keyed(PrintingDensity.COMPACT)
        container.put("kind", self.kind, TargetDependencyKind.LOCAL_TARGET)
        if self.kind is TargetDependencyKind.LOCAL_TARGET:
            container.put_unconditionally("target", self.content)
        else:
            container.put_inline(self.content)
        container.put("platforms", self.platform_filters, frozenset(), PrintingDensity.COMPACT)

    @classmethod
    def decode(cls, coder: Any) -> Self:
        if coder.current_node_type is ValueType.STRING:
            return cls.of_local_target(LocalTargetReference(coder.decode_string()))
        container = coder.keyed()
        filters = container.get_or_default("platforms", Decoders.set_of(PlatformFilter), frozenset())
        kind = container.get_or_default("kind", TargetDependencyKind, TargetDependencyKind.LOCAL_TARGET)
        if kind is TargetDependencyKind.LOCAL_TARGET:
            return cls(kind, container.get("target", LocalTargetReference), filters)
        return cls(kind, CONTENT_TYPES[kind].decode_inline(container), filters)
