from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Self

from xcodefy.library.schema.build_files.project_build_file import ProjectBuildFile
from xcodefy.library.schema.values.file_type_id import FileTypeID
from xcodefy.library.schema.values.group_tree_reference import GroupTreeReference
from xcodefy.library.schema.values.object_id import ObjectID
from xcodefy.library.serialization.decoders import Decoders
from xcodefy.library.serialization.inline_keyed_codable import InlineKeyedCodable
from xcodefy.library.utilities.lexicographical_order import LexicographicalOrder
from xcodefy.library.utilities.path_names import PathNames


@dataclass(slots=True)
class RemoteProduct(InlineKeyedCodable):
    project: GroupTreeReference
    target: str
    product_id: ObjectID
    path: str = ""
    file_type: FileTypeID | None = None
    build_files: list[ProjectBuildFile] = field(default_factory=list)

    @property
    def suggested_encoding_order(self) -> LexicographicalOrder:
        file_type = self.file_type.raw_value if self.file_type is not None else ""
        return LexicographicalOrder((self.path, self.target, self.product_id.raw_value, file_type))

    @property
    def path_is_name(self) -> bool:
        return len(PathNames.path_components(self.path)) == 1

    def encode_inline(self, container: Any) -> None:
        container.put_unconditionally("name" if self.path_is_name else "path", self.path)
        container.put_unconditionally("project", self.project)
        container.put_unconditionally("target", self.target)
        container.put_unconditionally("product-id", self.product_id)
        container.put("type", self.file_type, None)
        container.put_unconditionally("target-membership", self.build_files)

    @classmethod
    def decode_inline(cls, container: Any) -> Self:
        name = container.get_if_present("name", Decoders.string)
        path = name if name is not None else container.get("path", Decoders.string)
        project = container.get("project", GroupTreeReference)
        target = container.get("target", Decoders.string)
        product_id = container.get("product-id", ObjectID)
        file_type = container.get_if_present("type", FileTypeID)
        build_files = container.get("target-membership", Decoders.array_of(ProjectBuildFile))
        return cls(project, target, product_id, path, file_type, build_files)
