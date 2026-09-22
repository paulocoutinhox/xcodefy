from pathlib import Path

from tests.support.comprehensive import Comprehensive
from xcodefy.library.schema.project import Project

GOLDEN = Path(__file__).parent / "support" / "comprehensive.xcproj"


def golden_text() -> str:
    return GOLDEN.read_text(encoding="utf-8")


def test_a_comprehensive_project_renders_exactly_as_recorded():
    assert Comprehensive.project().json_text() == golden_text()


def test_the_recorded_rendering_decodes_back_to_the_same_project():
    assert Project.from_json_text(golden_text()) == Comprehensive.project()


def test_the_recorded_rendering_is_already_canonical():
    assert Project.from_json_text(golden_text()).json_text() == golden_text()


def test_the_rendering_survives_being_reflowed():
    reflowed = golden_text().replace("\n", " ")
    assert Project.from_json_text(reflowed).json_text() == golden_text()
