from tests.support.round_trip import RoundTrip
from xcodefy.library.schema.build_phases.build_phase_properties import BuildPhaseProperties
from xcodefy.library.schema.values.object_id import ObjectID
from xcodefy.library.serialization.printing_density import PrintingDensity


def test_the_default_properties_encode_to_nothing():
    assert BuildPhaseProperties().everything_is_default is True
    assert RoundTrip.text(BuildPhaseProperties()) == "{\n}\n"


def test_the_identifier_and_name_are_written_when_present():
    properties = BuildPhaseProperties(ObjectID("A1"), "Compile Sources")
    assert RoundTrip.text(properties) == '{\n  "id": "A1",\n  "name": "Compile Sources",\n}\n'


def test_plain_phase_properties_print_compactly():
    assert BuildPhaseProperties().printing_density is PrintingDensity.COMPACT


def test_populated_properties_round_trip():
    RoundTrip.expect_equal(BuildPhaseProperties(ObjectID("A1"), "Name"), BuildPhaseProperties)
