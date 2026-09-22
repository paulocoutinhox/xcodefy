from tests.support.instances import Instances
from tests.support.round_trip import RoundTrip
from xcodefy.library.schema.target.dependencies.swift_package_product_reference import SwiftPackageProductReference
from xcodefy.library.schema.values.swift_package_product_type import SwiftPackageProductType


def test_the_product_name_is_always_written_and_the_default_type_is_omitted():
    reference = SwiftPackageProductReference("helper")
    assert RoundTrip.text(reference) == '{\n  "product-name": "helper",\n}\n'


def test_a_non_default_product_type_is_written():
    reference = SwiftPackageProductReference("helper", SwiftPackageProductType.BUILD_TOOL_PLUGIN)
    assert '"product-type": "build-tool-plugin"' in RoundTrip.text(reference)


def test_the_encoding_order_covers_the_package_name_product_and_type():
    assert Instances.populated_package_product_reference().encoding_order.content == ("SuperUseful", "helper", "build-tool-plugin")


def test_a_reference_without_a_package_still_sorts():
    assert SwiftPackageProductReference("helper").encoding_order.content[0] == ""


def test_a_populated_reference_round_trips():
    RoundTrip.expect_equal(Instances.populated_package_product_reference(), SwiftPackageProductReference)
