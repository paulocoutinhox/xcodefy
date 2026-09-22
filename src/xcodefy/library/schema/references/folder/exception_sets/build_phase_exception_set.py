from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Self

from xcodefy.library.schema.build_phase_references.project_build_phase_reference import ProjectBuildPhaseReference
from xcodefy.library.schema.references.folder.exception_sets.common_exception_set_properties import CommonExceptionSetProperties
from xcodefy.library.serialization.inline_keyed_codable import InlineKeyedCodable


@dataclass(slots=True)
class BuildPhaseExceptionSet(InlineKeyedCodable):
    build_phase: ProjectBuildPhaseReference
    common_properties: CommonExceptionSetProperties = field(default_factory=CommonExceptionSetProperties)

    def encode_inline(self, container: Any) -> None:
        container.put_unconditionally("build-phase", self.build_phase)
        self.common_properties.encode_inline(container)

    @classmethod
    def decode_inline(cls, container: Any) -> Self:
        build_phase = container.get("build-phase", ProjectBuildPhaseReference)
        return cls(build_phase, CommonExceptionSetProperties.decode_inline(container))
