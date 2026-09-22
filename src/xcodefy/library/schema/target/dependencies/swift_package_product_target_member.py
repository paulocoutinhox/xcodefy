from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Self

from xcodefy.library.schema.build_files.target_build_file import TargetBuildFile
from xcodefy.library.schema.target.dependencies.swift_package_product_reference import SwiftPackageProductReference
from xcodefy.library.utilities.lexicographical_order import LexicographicalOrder


@dataclass(slots=True)
class SwiftPackageProductTargetMember:
    package_product: SwiftPackageProductReference
    build_file: TargetBuildFile

    @property
    def encoding_order(self) -> LexicographicalOrder:
        phase = self.build_file.build_phase
        named = phase.kind is not None
        components = (phase.kind.value, phase.name or "", "") if named else ("", "", phase.object_id.raw_value)
        return LexicographicalOrder((self.package_product.encoding_order.content, components))

    def encode(self, coder: Any) -> None:
        container = coder.keyed()
        container.put_inline(self.package_product)
        container.put_unconditionally("build-phase", self.build_file)

    @classmethod
    def decode(cls, coder: Any) -> Self:
        container = coder.keyed()
        package_product = container.get_inline(SwiftPackageProductReference)
        return cls(package_product, container.get("build-phase", TargetBuildFile))
