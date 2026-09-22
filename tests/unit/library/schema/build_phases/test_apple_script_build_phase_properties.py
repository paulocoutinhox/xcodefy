from tests.support.instances import Instances
from tests.support.round_trip import RoundTrip
from xcodefy.library.schema.build_phases.apple_script_build_phase_properties import AppleScriptBuildPhaseProperties


def test_the_defaults_encode_to_nothing():
    assert RoundTrip.text(AppleScriptBuildPhaseProperties()) == "{\n}\n"


def test_the_context_settings_are_written_when_present():
    properties = AppleScriptBuildPhaseProperties(is_shared_context=True, context_name="MyContext")
    assert RoundTrip.text(properties) == '{\n  "is-shared-context": true,\n  "context-name": "MyContext",\n}\n'


def test_the_phase_name_comes_from_the_base_properties():
    assert Instances.populated_apple_script_properties().name == "Run AppleScript"


def test_an_apple_script_phase_never_prints_compactly():
    assert AppleScriptBuildPhaseProperties().printing_density is None


def test_populated_properties_round_trip():
    RoundTrip.expect_equal(Instances.populated_apple_script_properties(), AppleScriptBuildPhaseProperties)
