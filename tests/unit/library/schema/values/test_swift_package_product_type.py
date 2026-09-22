from xcodefy.library.schema.values.swift_package_product_type import SwiftPackageProductType


def test_both_package_product_types_are_represented():
    assert [member.value for member in SwiftPackageProductType] == ["other", "build-tool-plugin"]
