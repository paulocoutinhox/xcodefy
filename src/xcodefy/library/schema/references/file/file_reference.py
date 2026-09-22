from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Self

from xcodefy.library.schema.build_files.project_build_file import ProjectBuildFile
from xcodefy.library.schema.references.common_reference_properties import CommonReferenceProperties
from xcodefy.library.schema.references.line_ending import LineEnding
from xcodefy.library.schema.values.file_path import FilePath
from xcodefy.library.schema.values.file_type_id import FileTypeID
from xcodefy.library.schema.values.object_id import ObjectID
from xcodefy.library.schema.values.text_encoding import TextEncoding
from xcodefy.library.serialization.decoders import Decoders
from xcodefy.library.serialization.inline_keyed_codable import InlineKeyedCodable
from xcodefy.library.serialization.printing_density import PrintingDensity


@dataclass(slots=True)
class FileReference(InlineKeyedCodable):
    path: FilePath = field(default_factory=FilePath)
    object_id: ObjectID | None = None
    explicit_file_type: FileTypeID | None = None
    expected_signature: str | None = None
    text_encoding: TextEncoding | None = None
    line_ending: LineEnding | None = None
    common_properties: CommonReferenceProperties = field(default_factory=CommonReferenceProperties)
    build_files: list[ProjectBuildFile] = field(default_factory=list)

    @property
    def printing_density(self) -> PrintingDensity | None:
        return PrintingDensity.COMPACT if len(self.build_files) <= 1 else None

    def encode_inline(self, container: Any) -> None:
        container.put_inline(self.path)
        container.put("id", self.object_id, None)
        container.put("type", self.explicit_file_type, None)
        container.put("signature", self.expected_signature, None)
        container.put("encoding", self.text_encoding, None)
        container.put("line-ending", self.line_ending, None)
        container.put_inline(self.common_properties)
        container.put("target-membership", self.build_files, [])

    @classmethod
    def decode_inline(cls, container: Any) -> Self:
        object_id = container.get_optional("id", ObjectID)
        path = container.get_inline(FilePath)
        explicit_file_type = container.get_optional("type", FileTypeID)
        expected_signature = container.get_optional("signature", Decoders.string)
        text_encoding = container.get_optional("encoding", TextEncoding)
        line_ending = container.get_optional("line-ending", LineEnding)
        common_properties = container.get_inline(CommonReferenceProperties)
        build_files = container.get_or_default("target-membership", Decoders.array_of(ProjectBuildFile), [])
        return cls(path, object_id, explicit_file_type, expected_signature, text_encoding, line_ending, common_properties, build_files)
