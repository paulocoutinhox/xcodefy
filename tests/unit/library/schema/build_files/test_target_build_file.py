from tests.support.instances import Instances
from tests.support.round_trip import RoundTrip
from xcodefy.library.schema.build_files.target_build_file import TargetBuildFile
from xcodefy.library.schema.build_phase_references.target_build_phase_reference import TargetBuildPhaseReference
from xcodefy.library.schema.build_phases.build_phase_kind import BuildPhaseKind


def test_a_target_build_file_always_uses_the_compact_object_form():
    build_file = TargetBuildFile(TargetBuildPhaseReference.named(BuildPhaseKind.SOURCES))
    assert RoundTrip.text(build_file) == '{ "build-phase": "compile-sources" }\n'


def test_a_populated_target_build_file_round_trips():
    RoundTrip.expect_equal(Instances.populated_target_build_file(), TargetBuildFile)
