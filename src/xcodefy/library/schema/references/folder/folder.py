from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Self

from xcodefy.library.schema.references.common_reference_properties import CommonReferenceProperties
from xcodefy.library.schema.references.folder.exception_sets.folder_exception_set import FolderExceptionSet
from xcodefy.library.schema.values.file_path import FilePath
from xcodefy.library.schema.values.file_type_id import FileTypeID
from xcodefy.library.schema.values.folder_member_id import FolderMemberID
from xcodefy.library.schema.values.local_target_reference import LocalTargetReference
from xcodefy.library.schema.values.object_id import ObjectID
from xcodefy.library.serialization.decoders import Decoders
from xcodefy.library.serialization.inline_keyed_codable import InlineKeyedCodable
from xcodefy.library.serialization.printing_density import PrintingDensity


@dataclass(slots=True)
class Folder(InlineKeyedCodable):
    path: FilePath = field(default_factory=FilePath)
    object_id: ObjectID | None = None
    targets: frozenset[LocalTargetReference] = field(default_factory=frozenset)
    membership_exceptions: list[FolderExceptionSet] = field(default_factory=list)
    explicit_file_types: dict[FolderMemberID, FileTypeID] = field(default_factory=dict)
    explicit_opaque_folders: frozenset[FolderMemberID] = field(default_factory=frozenset)
    common_properties: CommonReferenceProperties = field(default_factory=CommonReferenceProperties)

    @property
    def printing_density(self) -> PrintingDensity | None:
        return PrintingDensity.COMPACT if not self.membership_exceptions else None

    def encode_inline(self, container: Any) -> None:
        container.put("id", self.object_id, None)
        container.put_inline(self.path)
        container.put("file-types", self.explicit_file_types, {})
        container.put("opaque-folders", self.explicit_opaque_folders, frozenset())
        container.put("target-membership", self.targets, frozenset())
        container.put("membership-exceptions", self.membership_exceptions, [])
        container.put_inline(self.common_properties)

    @classmethod
    def decode_inline(cls, container: Any) -> Self:
        path = container.get_inline(FilePath)
        object_id = container.get_optional("id", ObjectID)
        explicit_file_types = container.get_or_default("file-types", Decoders.keyed_dictionary_of(FolderMemberID, FileTypeID), {})
        opaque_folders = container.get_or_default("opaque-folders", Decoders.set_of(FolderMemberID), frozenset())
        targets = container.get_or_default("target-membership", Decoders.set_of(LocalTargetReference), frozenset())
        exceptions = container.get_or_default("membership-exceptions", Decoders.array_of(FolderExceptionSet), [])
        common_properties = container.get_inline(CommonReferenceProperties)
        return cls(path, object_id, targets, exceptions, explicit_file_types, opaque_folders, common_properties)
