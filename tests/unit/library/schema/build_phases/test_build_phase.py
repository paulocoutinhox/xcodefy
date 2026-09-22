import pytest

from tests.support.instances import Instances
from tests.support.round_trip import RoundTrip
from xcodefy.errors.decode_error import DecodeError
from xcodefy.errors.validation_error import ValidationError
from xcodefy.library.schema.build_phases.build_phase import BuildPhase
from xcodefy.library.schema.build_phases.build_phase_kind import BuildPhaseKind
from xcodefy.library.schema.build_phases.build_phase_properties import BuildPhaseProperties
from xcodefy.library.serialization.decoder import Decoder
from xcodefy.library.serialization.printing_density import PrintingDensity
from xcodefy.library.serialization.values.value import Value

PLAIN_KINDS = [BuildPhaseKind.FRAMEWORKS, BuildPhaseKind.HEADERS, BuildPhaseKind.JAVA_ARCHIVE, BuildPhaseKind.RESOURCES, BuildPhaseKind.REZ, BuildPhaseKind.SOURCES]
SPECIALISED_KINDS = [BuildPhaseKind.APPLE_SCRIPT, BuildPhaseKind.COPY, BuildPhaseKind.SCRIPT]


@pytest.mark.parametrize("kind", PLAIN_KINDS)
def test_a_plain_phase_with_default_properties_encodes_as_a_bare_kind(kind):
    phase = BuildPhase.of_kind(kind)
    assert phase.encode_as_kind_only is True
    assert RoundTrip.text(phase) == f'"{kind.value}"\n'
    RoundTrip.expect_equal(phase, BuildPhase)


@pytest.mark.parametrize("kind", PLAIN_KINDS)
def test_a_plain_phase_with_a_name_encodes_as_an_object(kind):
    phase = BuildPhase(kind, BuildPhaseProperties(name="Custom"))
    assert phase.encode_as_kind_only is False
    assert RoundTrip.text(phase) == f'{{ "kind": "{kind.value}", "name": "Custom" }}\n'


@pytest.mark.parametrize("kind", SPECIALISED_KINDS)
def test_a_specialised_phase_never_encodes_as_a_bare_kind(kind):
    properties = {BuildPhaseKind.APPLE_SCRIPT: Instances.populated_apple_script_properties(), BuildPhaseKind.COPY: Instances.populated_copy_properties(), BuildPhaseKind.SCRIPT: Instances.populated_script_properties()}
    phase = BuildPhase(kind, properties[kind])
    assert phase.encode_as_kind_only is False
    RoundTrip.expect_equal(phase, BuildPhase)


@pytest.mark.parametrize("kind", SPECIALISED_KINDS)
def test_a_specialised_phase_cannot_be_decoded_from_a_bare_kind(kind):
    with pytest.raises(DecodeError, match="accompanying build phase properties are missing"):
        Decoder.decode_value(Value.string(kind.value), BuildPhase)


def test_mismatched_properties_are_rejected():
    with pytest.raises(ValidationError, match="requires ScriptBuildPhaseProperties"):
        BuildPhase(BuildPhaseKind.SCRIPT, BuildPhaseProperties())


def test_the_phase_name_is_delegated_to_its_properties():
    assert BuildPhase(BuildPhaseKind.SOURCES, BuildPhaseProperties(name="Custom")).name == "Custom"
    assert BuildPhase.of_kind(BuildPhaseKind.SOURCES).name is None


def test_the_printing_density_is_delegated_to_its_properties():
    assert BuildPhase.of_kind(BuildPhaseKind.SOURCES).printing_density is PrintingDensity.COMPACT
    assert BuildPhase(BuildPhaseKind.SCRIPT, Instances.populated_script_properties()).printing_density is None
