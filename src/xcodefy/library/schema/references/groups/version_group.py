from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Self

from xcodefy.library.schema.build_files.project_build_file import ProjectBuildFile
from xcodefy.library.schema.references.common_reference_properties import CommonReferenceProperties
from xcodefy.library.schema.references.file.file_reference import FileReference
from xcodefy.library.schema.values.file_path import FilePath
from xcodefy.library.schema.values.file_type_id import FileTypeID
from xcodefy.library.schema.values.group_tree_reference import GroupTreeReference
from xcodefy.library.schema.values.object_id import ObjectID
from xcodefy.library.serialization.decoders import Decoders
from xcodefy.library.serialization.inline_keyed_codable import InlineKeyedCodable
from xcodefy.library.serialization.printing_density import PrintingDensity


@dataclass(slots=True)
class VersionGroup(InlineKeyedCodable):
    path: FilePath = field(default_factory=FilePath)
    name: str = ""
    object_id: ObjectID | None = None
    current_version: GroupTreeReference | None = None
    versioned_file_type: FileTypeID | None = None
    common_properties: CommonReferenceProperties = field(default_factory=CommonReferenceProperties)
    build_files: list[ProjectBuildFile] = field(default_factory=list)
    children: list[FileReference] = field(default_factory=list)

    @property
    def printing_density(self) -> PrintingDensity | None:
        return PrintingDensity.COMPACT if not self.children and len(self.build_files) <= 1 else None

    def encode_inline(self, container: Any) -> None:
        container.put("id", self.object_id, None)
        container.put_inline(self.path)
        container.put("name", self.name, self.path.name)
        container.put("current-version", self.current_version, None)
        container.put("type", self.versioned_file_type, None)
        container.put_inline(self.common_properties)
        container.put("target-membership", self.build_files, [])
        container.put("children", self.children, [])

    @classmethod
    def decode_inline(cls, container: Any) -> Self:
        object_id = container.get_optional("id", ObjectID)
        path = container.get_inline(FilePath)
        name = container.get_or_default("name", Decoders.string, path.name)
        current_version = container.get_optional("current-version", GroupTreeReference)
        versioned_file_type = container.get_optional("type", FileTypeID)
        common_properties = container.get_inline(CommonReferenceProperties)
        build_files = container.get_or_default("target-membership", Decoders.array_of(ProjectBuildFile), [])
        children = container.get_or_default("children", Decoders.array_of(FileReference), [])
        return cls(path, name, object_id, current_version, versioned_file_type, common_properties, build_files, children)
