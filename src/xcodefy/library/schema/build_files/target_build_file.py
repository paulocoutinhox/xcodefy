from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Self

from xcodefy.library.schema.build_files.build_file_properties import BuildFileProperties
from xcodefy.library.schema.build_phase_references.target_build_phase_reference import TargetBuildPhaseReference
from xcodefy.library.schema.values.object_id import ObjectID
from xcodefy.library.serialization.printing_density import PrintingDensity


@dataclass(slots=True)
class TargetBuildFile:
    build_phase: TargetBuildPhaseReference
    properties: BuildFileProperties = field(default_factory=BuildFileProperties)
    object_id: ObjectID | None = None

    def encode(self, coder: Any) -> None:
        container = coder.keyed(PrintingDensity.COMPACT)
        container.put("id", self.object_id, None)
        container.put_unconditionally("build-phase", self.build_phase)
        container.put_inline(self.properties)

    @classmethod
    def decode(cls, coder: Any) -> Self:
        container = coder.keyed()
        object_id = container.get_optional("id", ObjectID)
        build_phase = container.get("build-phase", TargetBuildPhaseReference)
        return cls(build_phase, container.get_inline(BuildFileProperties), object_id)
