import pytest

from tests.support.instances import Instances
from tests.support.round_trip import RoundTrip
from xcodefy.errors.validation_error import ValidationError
from xcodefy.library.schema.target.common_target_properties import CommonTargetProperties
from xcodefy.library.schema.target.target import Target
from xcodefy.library.schema.target.target_kind import TargetKind
from xcodefy.library.schema.values.object_id import ObjectID


def test_a_native_target_omits_its_kind():
    assert "kind" not in RoundTrip.text(Target.native(CommonTargetProperties("App", ObjectID("T1"))))


def test_an_aggregate_target_writes_its_kind():
    assert '"kind": "aggregate"' in RoundTrip.text(Target.aggregate(CommonTargetProperties("App", ObjectID("T1"))))


def test_the_common_properties_are_reachable_for_every_kind():
    native = Target.native(CommonTargetProperties("App", ObjectID("T1")))
    external = Target.external_build_system(Instances.populated_external_target_properties())
    assert native.common_properties.name == "App"
    assert external.common_properties.name == "App"


def test_the_name_and_build_settings_are_delegated():
    target = Target.native(Instances.populated_common_target_properties())
    assert target.name == "App"
    assert "SWIFT_VERSION" in target.build_settings


def test_mismatched_content_is_rejected():
    with pytest.raises(ValidationError, match="requires ExternalBuildSystemTargetProperties"):
        Target(TargetKind.EXTERNAL_BUILD_SYSTEM, CommonTargetProperties("App", ObjectID("T1")))


def test_a_target_can_be_copied():
    target = Target.native(CommonTargetProperties("App", ObjectID("T1")))
    assert target.copy(kind=TargetKind.AGGREGATE).kind is TargetKind.AGGREGATE


@pytest.mark.parametrize("target", [Target.native(Instances.populated_common_target_properties()), Target.aggregate(Instances.empty_common_target_properties()), Target.external_build_system(Instances.populated_external_target_properties())])
def test_every_kind_round_trips(target):
    RoundTrip.expect_equal(target, Target)
