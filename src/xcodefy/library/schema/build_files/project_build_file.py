from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Self

from xcodefy.library.schema.build_files.build_file_properties import BuildFileProperties
from xcodefy.library.schema.build_phase_references.project_build_phase_reference import ProjectBuildPhaseReference
from xcodefy.library.schema.values.object_id import ObjectID
from xcodefy.library.serialization.printing_density import PrintingDensity
from xcodefy.library.serialization.values.value_type import ValueType


@dataclass(slots=True)
class ProjectBuildFile:
    build_phase: ProjectBuildPhaseReference
    properties: BuildFileProperties = field(default_factory=BuildFileProperties)
    object_id: ObjectID | None = None

    @property
    def encodes_to_string(self) -> bool:
        if self.object_id is not None or not self.properties.everything_is_default:
            return False
        return self.build_phase.group_tree_reference_representation.encodes_to_string

    def encode(self, coder: Any) -> None:
        if self.encodes_to_string:
            self.build_phase.encode(coder)
            return
        container = coder.keyed(PrintingDensity.COMPACT)
        container.put("id", self.object_id, None)
        container.put_unconditionally("build-phase", self.build_phase)
        container.put_inline(self.properties)

    @classmethod
    def decode(cls, coder: Any) -> Self:
        if coder.current_node_type is ValueType.STRING:
            return cls(ProjectBuildPhaseReference.decode(coder))
        container = coder.keyed()
        object_id = container.get_optional("id", ObjectID)
        build_phase = container.get("build-phase", ProjectBuildPhaseReference)
        return cls(build_phase, container.get_inline(BuildFileProperties), object_id)
