from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Self

from xcodefy.library.schema.build_files.code_generation import CodeGeneration
from xcodefy.library.schema.build_files.code_generation_visibility import CodeGenerationVisibility
from xcodefy.library.schema.build_files.header_preservation import HeaderPreservation
from xcodefy.library.schema.build_files.header_role import HeaderRole
from xcodefy.library.schema.build_files.mach_interface_generation import MachInterfaceGeneration
from xcodefy.library.serialization.decoders import Decoders
from xcodefy.library.serialization.inline_keyed_codable import InlineKeyedCodable


@dataclass(frozen=True, slots=True)
class BuildFileAttributes(InlineKeyedCodable):
    header_role: HeaderRole | None = None
    mach_interface_generation: MachInterfaceGeneration | None = None
    is_weak: bool = False
    code_sign_on_copy: bool = False
    code_generation: CodeGeneration = CodeGeneration.DEFAULT
    header_preservation: HeaderPreservation = HeaderPreservation.KEEP
    decompress: bool = False
    code_generation_visibility: CodeGenerationVisibility | None = None

    @property
    def everything_is_default(self) -> bool:
        return self == BuildFileAttributes()

    def encode_inline(self, container: Any) -> None:
        container.put("header-role", self.header_role, None)
        container.put("mach-interface-generation", self.mach_interface_generation, None)
        container.put("is-weak", self.is_weak, False)
        container.put("code-sign-on-copy", self.code_sign_on_copy, False)
        container.put("code-generation", self.code_generation, CodeGeneration.DEFAULT)
        container.put("header-preservation", self.header_preservation, HeaderPreservation.KEEP)
        container.put("decompress", self.decompress, False)
        container.put("code-generation-visibility", self.code_generation_visibility, None)

    @classmethod
    def decode_inline(cls, container: Any) -> Self:
        header_role = container.get_optional("header-role", HeaderRole)
        mach_interface_generation = container.get_optional("mach-interface-generation", MachInterfaceGeneration)
        is_weak = container.get_or_default("is-weak", Decoders.boolean, False)
        code_sign_on_copy = container.get_or_default("code-sign-on-copy", Decoders.boolean, False)
        code_generation = container.get_or_default("code-generation", CodeGeneration, CodeGeneration.DEFAULT)
        header_preservation = container.get_or_default("header-preservation", HeaderPreservation, HeaderPreservation.KEEP)
        decompress = container.get_or_default("decompress", Decoders.boolean, False)
        visibility = container.get_optional("code-generation-visibility", CodeGenerationVisibility)
        return cls(header_role, mach_interface_generation, is_weak, code_sign_on_copy, code_generation, header_preservation, decompress, visibility)
