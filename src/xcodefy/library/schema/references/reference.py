from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Self

from xcodefy.errors.validation_error import ValidationError
from xcodefy.library.schema.references.file.file_reference import FileReference
from xcodefy.library.schema.references.folder.folder import Folder
from xcodefy.library.schema.references.groups.group import Group
from xcodefy.library.schema.references.groups.variant_group import VariantGroup
from xcodefy.library.schema.references.groups.version_group import VersionGroup
from xcodefy.library.schema.references.reference_kind import ReferenceKind
from xcodefy.library.serialization.printing_density import PrintingDensity

CONTENT_TYPES = {ReferenceKind.FILE_REFERENCE: FileReference, ReferenceKind.GROUP: Group, ReferenceKind.FOLDER: Folder, ReferenceKind.VARIANT_GROUP: VariantGroup, ReferenceKind.VERSION_GROUP: VersionGroup}


@dataclass(slots=True)
class Reference:
    kind: ReferenceKind
    content: Any

    def __post_init__(self) -> None:
        if not isinstance(self.content, CONTENT_TYPES[self.kind]):
            raise ValidationError(f"A {self.kind.value} reference requires {CONTENT_TYPES[self.kind].__name__}.")

    @classmethod
    def of_file(cls, content: FileReference) -> Self:
        return cls(ReferenceKind.FILE_REFERENCE, content)

    @classmethod
    def of_group(cls, content: Group) -> Self:
        return cls(ReferenceKind.GROUP, content)

    @classmethod
    def of_folder(cls, content: Folder) -> Self:
        return cls(ReferenceKind.FOLDER, content)

    @classmethod
    def of_variant_group(cls, content: VariantGroup) -> Self:
        return cls(ReferenceKind.VARIANT_GROUP, content)

    @classmethod
    def of_version_group(cls, content: VersionGroup) -> Self:
        return cls(ReferenceKind.VERSION_GROUP, content)

    @property
    def printing_density(self) -> PrintingDensity | None:
        return self.content.printing_density

    def encode(self, coder: Any) -> None:
        container = coder.keyed(self.printing_density)
        container.put("kind", self.kind, ReferenceKind.FILE_REFERENCE)
        self.content.encode_inline(container)

    @classmethod
    def decode(cls, coder: Any) -> Self:
        container = coder.keyed()
        kind = container.get_or_default("kind", ReferenceKind, ReferenceKind.FILE_REFERENCE)
        if kind is ReferenceKind.GROUP:
            return cls(kind, Group.decode_inline(container, cls))
        return cls(kind, CONTENT_TYPES[kind].decode_inline(container))
