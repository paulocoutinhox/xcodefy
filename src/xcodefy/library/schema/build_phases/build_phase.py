from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Self

from xcodefy.errors.decode_error import DecodeError
from xcodefy.errors.validation_error import ValidationError
from xcodefy.library.schema.build_phases.apple_script_build_phase_properties import AppleScriptBuildPhaseProperties
from xcodefy.library.schema.build_phases.build_phase_kind import BuildPhaseKind
from xcodefy.library.schema.build_phases.build_phase_properties import BuildPhaseProperties
from xcodefy.library.schema.build_phases.copy_files_build_phase_properties import CopyFilesBuildPhaseProperties
from xcodefy.library.schema.build_phases.script_build_phase_properties import ScriptBuildPhaseProperties
from xcodefy.library.serialization.printing_density import PrintingDensity
from xcodefy.library.serialization.values.value_type import ValueType
from xcodefy.library.utilities.text import Text

PLAIN_KINDS = frozenset({BuildPhaseKind.FRAMEWORKS, BuildPhaseKind.HEADERS, BuildPhaseKind.JAVA_ARCHIVE, BuildPhaseKind.RESOURCES, BuildPhaseKind.REZ, BuildPhaseKind.SOURCES})
PROPERTY_TYPES = {BuildPhaseKind.APPLE_SCRIPT: AppleScriptBuildPhaseProperties, BuildPhaseKind.COPY: CopyFilesBuildPhaseProperties, BuildPhaseKind.SCRIPT: ScriptBuildPhaseProperties}


@dataclass(slots=True)
class BuildPhase:
    kind: BuildPhaseKind
    properties: Any = field(default_factory=BuildPhaseProperties)

    def __post_init__(self) -> None:
        expected = PROPERTY_TYPES.get(self.kind, BuildPhaseProperties)
        if not isinstance(self.properties, expected):
            raise ValidationError(f"A {self.kind.value} build phase requires {expected.__name__}.")

    @classmethod
    def of_kind(cls, kind: BuildPhaseKind, properties: Any = None) -> Self:
        return cls(kind, properties if properties is not None else BuildPhaseProperties())

    @property
    def name(self) -> str | None:
        return self.properties.name

    @property
    def printing_density(self) -> PrintingDensity | None:
        return self.properties.printing_density

    @property
    def encode_as_kind_only(self) -> bool:
        return self.kind in PLAIN_KINDS and self.properties.everything_is_default

    def encode(self, coder: Any) -> None:
        if self.encode_as_kind_only:
            coder.encode_string(self.kind.value)
            return
        container = coder.keyed(self.printing_density)
        container.put_unconditionally("kind", self.kind)
        container.put_inline(self.properties)

    @classmethod
    def decode(cls, coder: Any) -> Self:
        if coder.current_node_type is ValueType.STRING:
            return cls._decode_kind_only(BuildPhaseKind.decode(coder))
        container = coder.keyed()
        kind = container.get("kind", BuildPhaseKind)
        return cls(kind, container.get_inline(PROPERTY_TYPES.get(kind, BuildPhaseProperties)))

    @classmethod
    def _decode_kind_only(cls, kind: BuildPhaseKind) -> Self:
        if kind not in PLAIN_KINDS:
            quoted = Text.smart_quoted(kind.value)
            raise DecodeError(f"Invalid build phase encoding {quoted}. The accompanying build phase properties are missing.")
        return cls(kind, BuildPhaseProperties())
