from tests.support.instances import Instances
from tests.support.round_trip import RoundTrip
from xcodefy.library.schema.build_files.project_build_file import ProjectBuildFile
from xcodefy.library.schema.build_phase_references.project_build_phase_reference import ProjectBuildPhaseReference
from xcodefy.library.schema.build_phases.build_phase_kind import BuildPhaseKind
from xcodefy.library.schema.values.local_target_reference import LocalTargetReference
from xcodefy.library.schema.values.object_id import ObjectID

PHASE = ProjectBuildPhaseReference.named(LocalTargetReference("App"), BuildPhaseKind.SOURCES)


def test_a_plain_membership_collapses_to_a_bare_string():
    build_file = ProjectBuildFile(PHASE)
    assert build_file.encodes_to_string is True
    assert RoundTrip.text(build_file) == '"App/compile-sources"\n'


def test_an_object_id_forces_the_object_form():
    build_file = ProjectBuildFile(PHASE, object_id=ObjectID("A1"))
    assert build_file.encodes_to_string is False
    assert RoundTrip.text(build_file) == '{ "id": "A1", "build-phase": "App/compile-sources" }\n'


def test_non_default_properties_force_the_object_form():
    build_file = ProjectBuildFile(PHASE, Instances.populated_build_file_properties())
    assert build_file.encodes_to_string is False


def test_a_phase_that_cannot_encode_to_a_string_forces_the_object_form():
    phase = ProjectBuildPhaseReference.named(LocalTargetReference("id:App"), BuildPhaseKind.SOURCES)
    assert ProjectBuildFile(phase).encodes_to_string is False


def test_both_forms_round_trip():
    RoundTrip.expect_equal(ProjectBuildFile(PHASE), ProjectBuildFile)
    RoundTrip.expect_equal(Instances.populated_project_build_file(), ProjectBuildFile)
