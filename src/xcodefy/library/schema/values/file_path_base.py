from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from xcodefy.errors.validation_error import ValidationError
from xcodefy.library.schema.values.file_path_base_kind import FilePathBaseKind

BUILT_IN_EXPANSION_KINDS = frozenset({FilePathBaseKind.PROJECT, FilePathBaseKind.DEVELOPER, FilePathBaseKind.BUILD_PRODUCTS, FilePathBaseKind.SDK})


@dataclass(frozen=True, slots=True)
class FilePathBase:
    kind: FilePathBaseKind
    build_setting: str | None = None

    def __post_init__(self) -> None:
        if (self.kind is FilePathBaseKind.SOURCE_ROOT) != (self.build_setting is not None):
            raise ValidationError("Only a source root base carries a build setting name.")

    @classmethod
    def absolute(cls) -> Self:
        return cls(FilePathBaseKind.ABSOLUTE)

    @classmethod
    def group(cls) -> Self:
        return cls(FilePathBaseKind.GROUP)

    @classmethod
    def project(cls) -> Self:
        return cls(FilePathBaseKind.PROJECT)

    @classmethod
    def developer(cls) -> Self:
        return cls(FilePathBaseKind.DEVELOPER)

    @classmethod
    def build_products(cls) -> Self:
        return cls(FilePathBaseKind.BUILD_PRODUCTS)

    @classmethod
    def sdk(cls) -> Self:
        return cls(FilePathBaseKind.SDK)

    @classmethod
    def source_root(cls, build_setting: str) -> Self:
        return cls(FilePathBaseKind.SOURCE_ROOT, build_setting)

    @property
    def built_in_expansion_variable(self) -> str | None:
        return self.kind.value if self.kind in BUILT_IN_EXPANSION_KINDS else None

    @classmethod
    def from_expansion_variable(cls, variable: str) -> Self | None:
        for kind in BUILT_IN_EXPANSION_KINDS:
            if kind.value == variable:
                return cls(kind)
        return None
