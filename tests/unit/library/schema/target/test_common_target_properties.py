import pytest

from tests.support.instances import Instances
from tests.support.round_trip import RoundTrip
from xcodefy.errors.encode_error import EncodeError
from xcodefy.library.schema.configuration import Configuration
from xcodefy.library.schema.target.common_target_properties import CommonTargetProperties
from xcodefy.library.schema.target.target import Target
from xcodefy.library.schema.values.configuration_name import ConfigurationName
from xcodefy.library.schema.values.object_id import ObjectID
from xcodefy.library.schema.values.product_type_id import ProductTypeID


def properties(**changes):
    return CommonTargetProperties("App", ObjectID("T1")).copy(**changes)


def test_the_name_and_identifier_are_always_written():
    assert RoundTrip.text(Target.native(properties())) == '{\n  "name": "App",\n  "id": "T1",\n}\n'


def test_an_apple_product_type_is_abbreviated():
    target = Target.native(properties(product_type_id=ProductTypeID("com.apple.product-type.application")))
    assert '"product-type": "application"' in RoundTrip.text(target)
    RoundTrip.expect_equal(target, Target)


def test_a_foreign_product_type_is_written_in_full():
    target = Target.native(properties(product_type_id=ProductTypeID("unusual.prefix")))
    assert '"full-product-type": "unusual.prefix"' in RoundTrip.text(target)
    RoundTrip.expect_equal(target, Target)


def test_an_absent_product_type_is_omitted():
    assert "product-type" not in RoundTrip.text(Target.native(properties()))


def test_a_redundant_specialized_configuration_is_rejected():
    target = Target.native(properties(specialized_configurations=[Configuration(ConfigurationName("Debug"))]))
    with pytest.raises(EncodeError, match="Redundant configuration specialization"):
        RoundTrip.text(target)


def test_package_product_members_are_sorted_before_encoding():
    target = Target.native(Instances.populated_common_target_properties())
    RoundTrip.expect_equal(target, Target)


def test_fully_populated_properties_round_trip():
    RoundTrip.expect_equal(Target.native(Instances.populated_common_target_properties()), Target)
