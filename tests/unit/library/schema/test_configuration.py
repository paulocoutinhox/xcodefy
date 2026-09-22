from tests.support.instances import Instances
from tests.support.round_trip import RoundTrip
from xcodefy.library.schema.configuration import Configuration
from xcodefy.library.schema.values.configuration_name import ConfigurationName
from xcodefy.library.schema.values.object_id import ObjectID


def test_a_plain_configuration_collapses_to_its_name():
    configuration = Configuration(ConfigurationName("Debug"))
    assert configuration.is_specialized is False
    assert RoundTrip.text(configuration) == '"Debug"\n'


def test_an_xcconfig_file_specialises_the_configuration():
    configuration = Configuration(ConfigurationName("Debug"), Instances.populated_anchored_reference())
    assert configuration.is_specialized is True
    assert '"name": "Debug"' in RoundTrip.text(configuration)


def test_an_object_id_specialises_the_configuration():
    configuration = Configuration(ConfigurationName("Debug"), object_id=ObjectID("A1"))
    assert configuration.is_specialized is True
    assert RoundTrip.text(configuration) == '{\n  "id": "A1",\n  "name": "Debug",\n}\n'


def test_both_forms_round_trip():
    RoundTrip.expect_equal(Configuration(ConfigurationName("Release")), Configuration)
    RoundTrip.expect_equal(Configuration(ConfigurationName("Debug"), Instances.populated_anchored_reference(), ObjectID("A1")), Configuration)
