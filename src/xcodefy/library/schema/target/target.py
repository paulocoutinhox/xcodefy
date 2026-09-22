from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Self

from xcodefy.errors.validation_error import ValidationError
from xcodefy.library.schema.target.common_target_properties import CommonTargetProperties
from xcodefy.library.schema.target.external_build_system_target_properties import ExternalBuildSystemTargetProperties
from xcodefy.library.schema.target.target_kind import TargetKind
from xcodefy.library.utilities.copy_with import CopyWith

CONTENT_TYPES = {TargetKind.NATIVE: CommonTargetProperties, TargetKind.AGGREGATE: CommonTargetProperties, TargetKind.EXTERNAL_BUILD_SYSTEM: ExternalBuildSystemTargetProperties}


@dataclass(slots=True)
class Target(CopyWith):
    kind: TargetKind
    content: Any

    def __post_init__(self) -> None:
        if not isinstance(self.content, CONTENT_TYPES[self.kind]):
            raise ValidationError(f"A {self.kind.value} target requires {CONTENT_TYPES[self.kind].__name__}.")

    @classmethod
    def native(cls, content: CommonTargetProperties) -> Self:
        return cls(TargetKind.NATIVE, content)

    @classmethod
    def aggregate(cls, content: CommonTargetProperties) -> Self:
        return cls(TargetKind.AGGREGATE, content)

    @classmethod
    def external_build_system(cls, content: ExternalBuildSystemTargetProperties) -> Self:
        return cls(TargetKind.EXTERNAL_BUILD_SYSTEM, content)

    @property
    def common_properties(self) -> CommonTargetProperties:
        if self.kind is TargetKind.EXTERNAL_BUILD_SYSTEM:
            return self.content.common_properties
        return self.content

    @property
    def name(self) -> str:
        return self.common_properties.name

    @property
    def build_settings(self) -> dict:
        return self.common_properties.build_settings

    def encode(self, coder: Any) -> None:
        container = coder.keyed()
        if self.kind is TargetKind.EXTERNAL_BUILD_SYSTEM:
            self.content.encode_inline(container)
            return
        self.content.encode_with_kind(container, self.kind)

    @classmethod
    def decode(cls, coder: Any) -> Self:
        container = coder.keyed()
        kind = container.get_or_default("kind", TargetKind, TargetKind.NATIVE)
        return cls(kind, CONTENT_TYPES[kind].decode_inline(container))
