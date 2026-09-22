from tests.support.instances import Instances
from tests.support.round_trip import RoundTrip
from xcodefy.library.schema.build_phases.script_build_phase_properties import ScriptBuildPhaseProperties


def test_the_shell_and_script_are_always_written():
    assert RoundTrip.text(ScriptBuildPhaseProperties()) == '{\n  "shell": "",\n  "script": "",\n}\n'


def test_a_multiline_script_encodes_as_an_array_of_lines():
    properties = ScriptBuildPhaseProperties(shell_path="/bin/sh", script="one\ntwo")
    assert RoundTrip.text(properties) == '{\n  "shell": "/bin/sh",\n  "script": [\n    "one",\n    "two",\n  ],\n}\n'


def test_the_phase_name_comes_from_the_base_properties():
    assert Instances.populated_script_properties().name == "Run Script"


def test_a_script_phase_never_prints_compactly():
    assert ScriptBuildPhaseProperties().printing_density is None


def test_populated_properties_round_trip():
    RoundTrip.expect_equal(Instances.populated_script_properties(), ScriptBuildPhaseProperties)


def test_a_script_can_be_replaced_through_copy():
    properties = Instances.populated_script_properties().copy(script="echo replaced")
    assert properties.script == "echo replaced"
    RoundTrip.expect_equal(properties, ScriptBuildPhaseProperties)
