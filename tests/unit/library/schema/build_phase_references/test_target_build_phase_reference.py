import pytest

from tests.support.round_trip import RoundTrip
from xcodefy.errors.decode_error import DecodeError
from xcodefy.errors.validation_error import ValidationError
from xcodefy.library.schema.build_phase_references.target_build_phase_reference import TargetBuildPhaseReference
from xcodefy.library.schema.build_phases.build_phase_kind import BuildPhaseKind
from xcodefy.library.schema.values.name_path_component import NamePathComponent
from xcodefy.library.schema.values.object_id import ObjectID
from xcodefy.library.schema.values.relative_reference import RelativeReference


def test_a_kind_only_reference_encodes_as_the_kind():
    assert RoundTrip.text(TargetBuildPhaseReference.named(BuildPhaseKind.SOURCES)) == '"compile-sources"\n'


def test_a_named_reference_encodes_as_kind_and_name():
    assert RoundTrip.text(TargetBuildPhaseReference.named(BuildPhaseKind.COPY, "Install")) == '"copy/Install"\n'


def test_an_object_id_reference_encodes_with_the_signalling_prefix():
    assert RoundTrip.text(TargetBuildPhaseReference.of_object_id(ObjectID("A1"))) == '"id:A1"\n'


@pytest.mark.parametrize("arguments", [{}, {"kind": BuildPhaseKind.COPY, "object_id": ObjectID("A1")}])
def test_a_reference_rejects_carrying_neither_or_both_forms(arguments):
    with pytest.raises(ValidationError, match="either a named phase or an object id"):
        TargetBuildPhaseReference(**arguments)


def test_an_object_id_reference_cannot_carry_a_name():
    with pytest.raises(ValidationError, match="cannot carry a name"):
        TargetBuildPhaseReference(object_id=ObjectID("A1"), name="Install")


@pytest.mark.parametrize("components", [(), (NamePathComponent.child("copy"), NamePathComponent.child("a"), NamePathComponent.child("b"))])
def test_a_reference_needs_one_or_two_components(components):
    with pytest.raises(DecodeError, match="Invalid target relative build phase reference"):
        TargetBuildPhaseReference.parse_components(components)


def test_an_unknown_kind_is_rejected():
    with pytest.raises(DecodeError, match="Invalid target relative build phase reference"):
        TargetBuildPhaseReference.parse_components((NamePathComponent.child("not-a-phase"),))


def test_a_relative_component_cannot_name_a_phase():
    components = (NamePathComponent.of_relative(RelativeReference.PARENT),)
    with pytest.raises(DecodeError, match="Invalid target relative build phase reference"):
        TargetBuildPhaseReference.parse_components(components)


def test_a_relative_component_cannot_name_a_build_phase_name():
    components = (NamePathComponent.child("copy"), NamePathComponent.of_relative(RelativeReference.PARENT))
    with pytest.raises(DecodeError, match="Invalid target relative build phase reference"):
        TargetBuildPhaseReference.parse_components(components)


def test_a_reference_renders_for_diagnostics():
    assert str(TargetBuildPhaseReference.named(BuildPhaseKind.COPY, "Install")) == "copy/Install"
