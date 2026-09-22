from tests.support.instances import Instances
from tests.support.round_trip import RoundTrip
from xcodefy.library.schema.target.common_target_properties import CommonTargetProperties
from xcodefy.library.schema.target.external_build_system_target_properties import ExternalBuildSystemTargetProperties
from xcodefy.library.schema.target.target import Target
from xcodefy.library.schema.values.object_id import ObjectID


def test_the_build_tool_path_is_always_written_and_the_defaults_are_omitted():
    properties = ExternalBuildSystemTargetProperties(CommonTargetProperties("App", ObjectID("T1")))
    text = RoundTrip.text(Target.external_build_system(properties))
    assert '"kind": "external-build-system"' in text
    assert '"build-tool-path": ""' in text
    assert "build-tool-arguments" not in text
    assert "pass-build-settings-in-environment" not in text


def test_the_non_default_settings_are_written():
    properties = Instances.populated_external_target_properties()
    text = RoundTrip.text(Target.external_build_system(properties))
    assert '"build-tool-arguments": "--glow-in-the-dark true"' in text
    assert '"build-tool-working-directory": "/shared/build"' in text


def test_disabling_the_environment_pass_through_is_written():
    properties = Instances.populated_external_target_properties().copy(pass_build_settings_in_environment=False)
    assert '"pass-build-settings-in-environment": false' in RoundTrip.text(Target.external_build_system(properties))


def test_populated_properties_round_trip():
    RoundTrip.expect_equal(Target.external_build_system(Instances.populated_external_target_properties()), Target)
