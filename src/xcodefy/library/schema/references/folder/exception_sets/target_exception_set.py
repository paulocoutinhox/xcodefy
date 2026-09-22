from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Self

from xcodefy.library.schema.references.folder.exception_sets.common_exception_set_properties import CommonExceptionSetProperties
from xcodefy.library.schema.values.folder_member_id import FolderMemberID
from xcodefy.library.schema.values.local_target_reference import LocalTargetReference
from xcodefy.library.serialization.decoders import Decoders
from xcodefy.library.serialization.inline_keyed_codable import InlineKeyedCodable


@dataclass(slots=True)
class TargetExceptionSet(InlineKeyedCodable):
    target: LocalTargetReference
    public_headers: frozenset[FolderMemberID] = field(default_factory=frozenset)
    private_headers: frozenset[FolderMemberID] = field(default_factory=frozenset)
    additional_compiler_flags: dict[FolderMemberID, str] = field(default_factory=dict)
    common_properties: CommonExceptionSetProperties = field(default_factory=CommonExceptionSetProperties)

    def encode_inline(self, container: Any) -> None:
        container.put_unconditionally("target", self.target)
        container.put("public-headers", self.public_headers, frozenset())
        container.put("private-headers", self.private_headers, frozenset())
        container.put("compiler-flags", self.additional_compiler_flags, {})
        self.common_properties.encode_inline(container)

    @classmethod
    def decode_inline(cls, container: Any) -> Self:
        target = container.get("target", LocalTargetReference)
        public_headers = container.get_or_default("public-headers", Decoders.set_of(FolderMemberID), frozenset())
        private_headers = container.get_or_default("private-headers", Decoders.set_of(FolderMemberID), frozenset())
        compiler_flags = container.get_or_default("compiler-flags", Decoders.keyed_dictionary_of(FolderMemberID, Decoders.string), {})
        return cls(target, public_headers, private_headers, compiler_flags, CommonExceptionSetProperties.decode_inline(container))
