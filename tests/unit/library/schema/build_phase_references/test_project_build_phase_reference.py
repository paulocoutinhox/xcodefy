import pytest

from tests.support.round_trip import RoundTrip
from xcodefy.errors.decode_error import DecodeError
from xcodefy.errors.validation_error import ValidationError
from xcodefy.library.schema.build_phase_references.project_build_phase_reference import ProjectBuildPhaseReference
from xcodefy.library.schema.build_phases.build_phase_kind import BuildPhaseKind
from xcodefy.library.schema.values.local_target_reference import LocalTargetReference
from xcodefy.library.schema.values.name_path import NamePath
from xcodefy.library.schema.values.name_path_component import NamePathComponent
from xcodefy.library.schema.values.object_id import ObjectID
from xcodefy.library.schema.values.relative_reference import RelativeReference


def test_a_kind_only_reference_encodes_as_target_and_kind():
    reference = ProjectBuildPhaseReference.named(LocalTargetReference("App"), BuildPhaseKind.SOURCES)
    assert RoundTrip.text(reference) == '"App/compile-sources"\n'


def test_a_named_reference_encodes_as_target_kind_and_name():
    reference = ProjectBuildPhaseReference.named(LocalTargetReference("App"), BuildPhaseKind.COPY, "Install")
    assert RoundTrip.text(reference) == '"App/copy/Install"\n'


def test_an_object_id_reference_encodes_with_the_signalling_prefix():
    assert RoundTrip.text(ProjectBuildPhaseReference.of_object_id(ObjectID("A1"))) == '"id:A1"\n'


@pytest.mark.parametrize("arguments", [{}, {"target": LocalTargetReference("App"), "kind": BuildPhaseKind.COPY, "object_id": ObjectID("A1")}])
def test_a_reference_rejects_carrying_neither_or_both_forms(arguments):
    with pytest.raises(ValidationError, match="either a named phase or an object id"):
        ProjectBuildPhaseReference(**arguments)


def test_a_named_reference_requires_a_target():
    with pytest.raises(ValidationError, match="requires a target"):
        ProjectBuildPhaseReference(kind=BuildPhaseKind.COPY)


def test_an_empty_name_path_is_rejected():
    with pytest.raises(DecodeError, match="Invalid project relative build phase reference"):
        ProjectBuildPhaseReference.from_name_path(NamePath())


def test_a_relative_first_component_is_rejected():
    path = NamePath((NamePathComponent.of_relative(RelativeReference.PARENT), NamePathComponent.child("copy")))
    with pytest.raises(DecodeError, match="Invalid project relative build phase reference"):
        ProjectBuildPhaseReference.from_name_path(path)


def test_a_reference_renders_for_diagnostics():
    reference = ProjectBuildPhaseReference.named(LocalTargetReference("App"), BuildPhaseKind.COPY)
    assert str(reference) == "App/copy"
