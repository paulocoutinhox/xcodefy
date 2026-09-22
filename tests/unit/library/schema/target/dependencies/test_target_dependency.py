import pytest

from tests.support.instances import Instances
from tests.support.round_trip import RoundTrip
from xcodefy.errors.validation_error import ValidationError
from xcodefy.library.schema.target.dependencies.target_dependency import TargetDependency
from xcodefy.library.schema.target.dependencies.target_dependency_kind import TargetDependencyKind
from xcodefy.library.schema.values.local_target_reference import LocalTargetReference
from xcodefy.library.schema.values.platform_filter import PlatformFilter

FILTERS = frozenset({PlatformFilter("ios")})


def test_an_unfiltered_local_target_collapses_to_a_bare_string():
    dependency = TargetDependency.of_local_target(LocalTargetReference("App"))
    assert dependency.encodes_to_string is True
    assert RoundTrip.text(dependency) == '"App"\n'


def test_a_filtered_local_target_uses_the_object_form():
    dependency = TargetDependency.of_local_target(LocalTargetReference("App"), FILTERS)
    assert dependency.encodes_to_string is False
    assert RoundTrip.text(dependency) == '{ "target": "App", "platforms": [ "ios" ] }\n'


def test_a_remote_target_writes_its_kind_and_inline_content():
    dependency = TargetDependency.of_remote_target(Instances.populated_remote_target())
    assert '"kind": "remoteTarget"' in RoundTrip.text(dependency)
    RoundTrip.expect_equal(dependency, TargetDependency)


def test_a_package_product_writes_its_kind_and_inline_content():
    dependency = TargetDependency.of_package(Instances.populated_package_product_reference())
    assert '"kind": "package"' in RoundTrip.text(dependency)
    RoundTrip.expect_equal(dependency, TargetDependency)


def test_mismatched_content_is_rejected():
    with pytest.raises(ValidationError, match="requires RemoteTarget"):
        TargetDependency(TargetDependencyKind.REMOTE_TARGET, LocalTargetReference("App"))
