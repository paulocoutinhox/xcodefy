import re
import tomllib
from pathlib import Path

from xcodefy.version import Version

PYPROJECT = Path(__file__).resolve().parents[2] / "pyproject.toml"


def test_the_version_is_reported_from_the_installed_metadata():
    assert re.fullmatch(r"\d+\.\d+\.\d+.*", Version.current())


def test_the_reported_version_is_the_one_declared_in_pyproject():
    declared = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))["project"]["version"]
    assert Version.current() == declared


def test_pyproject_is_the_only_place_the_version_is_written():
    root = PYPROJECT.parent
    declared = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))["project"]["version"]
    tracked = [path for path in [*root.glob("*.md"), *(root / "docs").glob("*.md"), *(root / ".github" / "workflows").glob("*.yml"), *(root / "src").rglob("*.py")]]
    carrying = [str(path.relative_to(root)) for path in tracked if declared in path.read_text(encoding="utf-8")]
    assert carrying == []
