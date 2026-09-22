from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Self

from xcodefy.errors.decode_error import DecodeError
from xcodefy.errors.validation_error import ValidationError
from xcodefy.library.schema.build_phase_references.target_build_phase_reference import TargetBuildPhaseReference
from xcodefy.library.schema.build_phases.build_phase_kind import BuildPhaseKind
from xcodefy.library.schema.values.group_tree_reference import GroupTreeReference
from xcodefy.library.schema.values.local_target_reference import LocalTargetReference
from xcodefy.library.schema.values.name_path import NamePath
from xcodefy.library.schema.values.object_id import ObjectID
from xcodefy.library.utilities.sequences import Sequences
from xcodefy.library.utilities.text import Text


@dataclass(frozen=True, slots=True)
class ProjectBuildPhaseReference:
    target: LocalTargetReference | None = None
    kind: BuildPhaseKind | None = None
    name: str | None = None
    object_id: ObjectID | None = None

    def __post_init__(self) -> None:
        if (self.kind is None) == (self.object_id is None):
            raise ValidationError("A project build phase reference is either a named phase or an object id.")
        if (self.kind is None) != (self.target is None):
            raise ValidationError("A named project build phase reference requires a target.")

    @classmethod
    def named(cls, target: LocalTargetReference, kind: BuildPhaseKind, name: str | None = None) -> Self:
        return cls(target=target, kind=kind, name=name)

    @classmethod
    def of_object_id(cls, object_id: ObjectID) -> Self:
        return cls(object_id=object_id)

    @property
    def group_tree_reference_representation(self) -> GroupTreeReference:
        if self.object_id is not None:
            return GroupTreeReference.of_object_id(self.object_id)
        return GroupTreeReference.of_child_names(Sequences.compacted([self.target.raw_value, self.kind.value, self.name]))

    @classmethod
    def from_name_path(cls, path: NamePath) -> Self:
        target_name = path.components[0].child_name if path.components else None
        if target_name is None:
            raise DecodeError(f"Invalid project relative build phase reference {Text.smart_quoted(str(path))}.")
        kind, name = TargetBuildPhaseReference.parse_components(path.components[1:])
        return cls.named(LocalTargetReference(target_name), kind, name)

    @classmethod
    def from_group_tree_reference(cls, reference: GroupTreeReference) -> Self:
        if reference.object_id is not None:
            return cls.of_object_id(reference.object_id)
        return cls.from_name_path(reference.name_path)

    def encode(self, coder: Any) -> None:
        self.group_tree_reference_representation.encode(coder)

    @classmethod
    def decode(cls, coder: Any) -> Self:
        return cls.from_group_tree_reference(GroupTreeReference.decode(coder))

    def __str__(self) -> str:
        return str(self.group_tree_reference_representation)
