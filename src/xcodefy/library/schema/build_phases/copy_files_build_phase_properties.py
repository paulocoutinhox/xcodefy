from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Self

from xcodefy.library.schema.build_phases.build_phase_properties import BuildPhaseProperties
from xcodefy.library.schema.build_phases.build_phase_scope import BuildPhaseScope
from xcodefy.library.schema.values.bundle_base_path import BundleBasePath
from xcodefy.library.serialization.decoders import Decoders
from xcodefy.library.serialization.inline_keyed_codable import InlineKeyedCodable
from xcodefy.library.serialization.printing_density import PrintingDensity


@dataclass(slots=True)
class CopyFilesBuildPhaseProperties(InlineKeyedCodable):
    base_properties: BuildPhaseProperties = field(default_factory=BuildPhaseProperties)
    bundle_base_path: BundleBasePath | None = None
    relative_path: str = ""
    scope: BuildPhaseScope = BuildPhaseScope.ALWAYS

    @property
    def name(self) -> str | None:
        return self.base_properties.name

    @property
    def printing_density(self) -> PrintingDensity | None:
        return None

    def encode_inline(self, container: Any) -> None:
        container.put_inline(self.base_properties)
        container.put("bundle-base-path", self.bundle_base_path, None)
        container.put("relative-path", self.relative_path, "")
        container.put("scope", self.scope, BuildPhaseScope.ALWAYS)

    @classmethod
    def decode_inline(cls, container: Any) -> Self:
        base_properties = container.get_inline(BuildPhaseProperties)
        bundle_base_path = container.get_optional("bundle-base-path", BundleBasePath)
        relative_path = container.get_or_default("relative-path", Decoders.string, "")
        scope = container.get_or_default("scope", BuildPhaseScope, BuildPhaseScope.ALWAYS)
        return cls(base_properties, bundle_base_path, relative_path, scope)
