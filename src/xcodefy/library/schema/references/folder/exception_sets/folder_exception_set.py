from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Self

from xcodefy.errors.decode_error import DecodeError
from xcodefy.errors.validation_error import ValidationError
from xcodefy.library.schema.references.folder.exception_sets.build_phase_exception_set import BuildPhaseExceptionSet
from xcodefy.library.schema.references.folder.exception_sets.target_exception_set import TargetExceptionSet


@dataclass(slots=True)
class FolderExceptionSet:
    target: TargetExceptionSet | None = None
    build_phase: BuildPhaseExceptionSet | None = None

    def __post_init__(self) -> None:
        if (self.target is None) == (self.build_phase is None):
            raise ValidationError("A folder exception set is either a target set or a build phase set.")

    @classmethod
    def of_target(cls, value: TargetExceptionSet) -> Self:
        return cls(target=value)

    @classmethod
    def of_build_phase(cls, value: BuildPhaseExceptionSet) -> Self:
        return cls(build_phase=value)

    def encode(self, coder: Any) -> None:
        container = coder.keyed()
        content = self.target if self.target is not None else self.build_phase
        content.encode_inline(container)

    @classmethod
    def decode(cls, coder: Any) -> Self:
        container = coder.keyed()
        if container.contains("target"):
            return cls.of_target(TargetExceptionSet.decode_inline(container))
        if container.contains("build-phase"):
            return cls.of_build_phase(BuildPhaseExceptionSet.decode_inline(container))
        raise DecodeError("Unknown exception set. Expected either a target or a build phase.")
