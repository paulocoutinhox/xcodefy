from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Self

from xcodefy.library.schema.build_phases.build_phase_properties import BuildPhaseProperties
from xcodefy.library.serialization.decoders import Decoders
from xcodefy.library.serialization.inline_keyed_codable import InlineKeyedCodable
from xcodefy.library.serialization.printing_density import PrintingDensity


@dataclass(slots=True)
class AppleScriptBuildPhaseProperties(InlineKeyedCodable):
    base_properties: BuildPhaseProperties = field(default_factory=BuildPhaseProperties)
    is_shared_context: bool = False
    context_name: str = ""

    @property
    def name(self) -> str | None:
        return self.base_properties.name

    @property
    def printing_density(self) -> PrintingDensity | None:
        return None

    def encode_inline(self, container: Any) -> None:
        container.put_inline(self.base_properties)
        container.put("is-shared-context", self.is_shared_context, False)
        container.put("context-name", self.context_name, "")

    @classmethod
    def decode_inline(cls, container: Any) -> Self:
        base_properties = container.get_inline(BuildPhaseProperties)
        is_shared_context = container.get_or_default("is-shared-context", Decoders.boolean, False)
        context_name = container.get_or_default("context-name", Decoders.string, "")
        return cls(base_properties, is_shared_context, context_name)
