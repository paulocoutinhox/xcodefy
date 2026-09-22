from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, Self

from xcodefy.errors.decode_error import DecodeError
from xcodefy.errors.validation_error import ValidationError
from xcodefy.library.schema.build_phases.build_phase_kind import BuildPhaseKind
from xcodefy.library.schema.values.group_tree_reference import GroupTreeReference
from xcodefy.library.schema.values.name_path import NamePath
from xcodefy.library.schema.values.name_path_component import NamePathComponent
from xcodefy.library.schema.values.object_id import ObjectID
from xcodefy.library.utilities.sequences import Sequences
from xcodefy.library.utilities.text import Text

KIND_VALUES = frozenset(kind.value for kind in BuildPhaseKind)


@dataclass(frozen=True, slots=True)
class TargetBuildPhaseReference:
    kind: BuildPhaseKind | None = None
    name: str | None = None
    object_id: ObjectID | None = None

    def __post_init__(self) -> None:
        if (self.kind is None) == (self.object_id is None):
            raise ValidationError("A target build phase reference is either a named phase or an object id.")
        if self.object_id is not None and self.name is not None:
            raise ValidationError("An object id build phase reference cannot carry a name.")

    @classmethod
    def named(cls, kind: BuildPhaseKind, name: str | None = None) -> Self:
        return cls(kind=kind, name=name)

    @classmethod
    def of_object_id(cls, object_id: ObjectID) -> Self:
        return cls(object_id=object_id)

    @property
    def group_tree_reference_representation(self) -> GroupTreeReference:
        if self.object_id is not None:
            return GroupTreeReference.of_object_id(self.object_id)
        return GroupTreeReference.of_child_names(Sequences.compacted([self.kind.value, self.name]))

    @staticmethod
    def parse_components(components: Sequence[NamePathComponent]) -> tuple[BuildPhaseKind, str | None]:
        description = str(NamePath(tuple(components)))
        if len(components) not in {1, 2}:
            raise DecodeError(f"Invalid target relative build phase reference: {Text.smart_quoted(description)}.")
        kind_name = components[0].child_name
        kind = BuildPhaseKind(kind_name) if kind_name in KIND_VALUES else None
        if kind is None:
            raise DecodeError(f"Invalid target relative build phase reference: {Text.smart_quoted(description)}.")
        if len(components) == 1:
            return kind, None
        name = components[1].child_name
        if name is None:
            raise DecodeError(f"Invalid target relative build phase reference: {Text.smart_quoted(description)}.")
        return kind, name

    @classmethod
    def from_group_tree_reference(cls, reference: GroupTreeReference) -> Self:
        if reference.object_id is not None:
            return cls.of_object_id(reference.object_id)
        kind, name = cls.parse_components(reference.name_path.components)
        return cls.named(kind, name)

    def encode(self, coder: Any) -> None:
        self.group_tree_reference_representation.encode(coder)

    @classmethod
    def decode(cls, coder: Any) -> Self:
        return cls.from_group_tree_reference(GroupTreeReference.decode(coder))

    def __str__(self) -> str:
        return str(self.group_tree_reference_representation)
