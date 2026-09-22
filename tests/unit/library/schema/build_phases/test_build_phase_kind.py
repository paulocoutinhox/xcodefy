import pytest

from xcodefy.errors.decode_error import DecodeError
from xcodefy.library.schema.build_phases.build_phase_kind import BuildPhaseKind

VALUES = ["apple-script", "frameworks", "headers", "java-archive", "resources", "rez", "compile-sources", "copy", "script"]


def test_every_build_phase_kind_from_the_reference_schema_is_represented():
    assert [member.value for member in BuildPhaseKind] == VALUES


def test_the_sources_phase_keeps_its_distinct_encoded_name():
    assert BuildPhaseKind.SOURCES.value == "compile-sources"


@pytest.mark.parametrize("kind", list(BuildPhaseKind))
def test_every_kind_carries_a_human_readable_name(kind):
    assert isinstance(kind.error_message_name, str)
    assert kind.error_message_name != ""


def test_the_human_readable_names_match_the_reference():
    assert BuildPhaseKind.FRAMEWORKS.error_message_name == "Link Libraries & Frameworks"
    assert BuildPhaseKind.SOURCES.error_message_name == "Compile Sources"


def test_an_unknown_value_is_rejected():
    with pytest.raises(DecodeError, match="Unexpected value"):
        BuildPhaseKind.from_encodable_string("not-a-phase")
