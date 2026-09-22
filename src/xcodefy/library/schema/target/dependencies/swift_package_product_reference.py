from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Self

from xcodefy.library.schema.values.object_id import ObjectID
from xcodefy.library.schema.values.swift_package_name import SwiftPackageName
from xcodefy.library.schema.values.swift_package_product_type import SwiftPackageProductType
from xcodefy.library.serialization.decoders import Decoders
from xcodefy.library.serialization.inline_keyed_codable import InlineKeyedCodable
from xcodefy.library.utilities.lexicographical_order import LexicographicalOrder


@dataclass(slots=True)
class SwiftPackageProductReference(InlineKeyedCodable):
    product_name: str = ""
    product_type: SwiftPackageProductType = SwiftPackageProductType.OTHER
    package: SwiftPackageName | None = None
    object_id: ObjectID | None = None

    @property
    def encoding_order(self) -> LexicographicalOrder:
        package_name = self.package.raw_value if self.package is not None else ""
        return LexicographicalOrder((package_name, self.product_name, self.product_type.value))

    def encode_inline(self, container: Any) -> None:
        container.put("package", self.package, None)
        container.put("id", self.object_id, None)
        container.put_unconditionally("product-name", self.product_name)
        container.put("product-type", self.product_type, SwiftPackageProductType.OTHER)

    @classmethod
    def decode_inline(cls, container: Any) -> Self:
        package = container.get_optional("package", SwiftPackageName)
        object_id = container.get_optional("id", ObjectID)
        product_name = container.get("product-name", Decoders.string)
        product_type = container.get_or_default("product-type", SwiftPackageProductType, SwiftPackageProductType.OTHER)
        return cls(product_name, product_type, package, object_id)
