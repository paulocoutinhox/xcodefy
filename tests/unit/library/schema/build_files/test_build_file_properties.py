from tests.support.instances import Instances
from tests.support.round_trip import RoundTrip
from xcodefy.library.schema.build_files.build_file_properties import BuildFileProperties
from xcodefy.library.schema.values.platform_filter import PlatformFilter


def test_the_default_properties_encode_to_nothing():
    assert BuildFileProperties().everything_is_default is True
    assert RoundTrip.text(BuildFileProperties()) == "{\n}\n"


def test_platform_filters_print_compactly():
    properties = BuildFileProperties(platform_filters=frozenset({PlatformFilter("ios")}))
    assert RoundTrip.text(properties) == '{\n  "platforms": [ "ios" ],\n}\n'


def test_the_nested_attributes_are_written_inline():
    properties = BuildFileProperties(attributes=Instances.populated_build_file_attributes())
    assert '"header-role"' in RoundTrip.text(properties)


def test_every_property_round_trips():
    RoundTrip.expect_equal(Instances.populated_build_file_properties(), BuildFileProperties)
    assert Instances.populated_build_file_properties().everything_is_default is False
