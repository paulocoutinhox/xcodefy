import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src" / "xcodefy"
TESTS = ROOT / "tests"

REQUIRED_PATHS = [
    ROOT / ".editorconfig",
    ROOT / ".github" / "FUNDING.yml",
    ROOT / ".github" / "workflows" / "test.yml",
    ROOT / ".github" / "workflows" / "release.yml",
    ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md",
    ROOT / ".github" / "ISSUE_TEMPLATE" / "bug_report.yml",
    ROOT / ".github" / "ISSUE_TEMPLATE" / "feature_request.yml",
    ROOT / ".github" / "ISSUE_TEMPLATE" / "question.yml",
    ROOT / "extras" / "images" / "logo.png",
    ROOT / "extras" / "images" / "social-preview.png",
    ROOT / "README.md",
    ROOT / "CLAUDE.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / "SECURITY.md",
    ROOT / "docs" / "index.md",
    ROOT / "docs" / "reference-coverage.md",
    SOURCE / "tool" / "main.py",
    SOURCE / "tool" / "arguments.py",
    SOURCE / "tool" / "help.py",
    SOURCE / "library" / "schema",
    SOURCE / "library" / "serialization",
    SOURCE / "library" / "utilities",
]


def source_files() -> list[Path]:
    return sorted(SOURCE.rglob("*.py"))


def mirrored_test_path(path: Path) -> Path:
    relative = path.relative_to(SOURCE)
    return TESTS / "unit" / relative.parent / f"test_{relative.stem}.py"


def test_every_init_file_is_empty():
    for path in [*SOURCE.rglob("__init__.py"), *TESTS.rglob("__init__.py")]:
        assert path.read_bytes() == b"", str(path)


def test_the_source_avoids_conditional_typing_imports_and_combined_statements():
    for path in source_files():
        text = path.read_text(encoding="utf-8")
        assert "TYPE_CHECKING" not in text, str(path)
        assert ";" not in text, str(path)


def test_every_source_module_declares_at_most_one_top_level_class():
    for path in source_files():
        tree = ast.parse(path.read_text(encoding="utf-8"))
        classes = [node for node in tree.body if isinstance(node, ast.ClassDef)]
        assert len(classes) <= 1, f"{path} declares {len(classes)} top level classes"


def test_every_source_module_has_a_mirrored_unit_test_module():
    for path in source_files():
        if path.name == "__init__.py":
            continue
        assert mirrored_test_path(path).exists(), f"Missing unit test {mirrored_test_path(path)}"


def test_every_unit_test_module_mirrors_a_source_module():
    for path in sorted((TESTS / "unit").rglob("test_*.py")):
        relative = path.relative_to(TESTS / "unit")
        expected = SOURCE / relative.parent / f"{relative.stem.removeprefix('test_')}.py"
        assert expected.exists(), f"Orphan unit test {path}"


def test_function_signatures_and_calls_stay_on_one_physical_line():
    for path in source_files():
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                assert node.lineno == node.end_lineno, f"Multiline call in {path}:{node.lineno}"
            if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.body:
                assert node.body[0].lineno <= node.lineno + 1, f"Multiline signature in {path}:{node.lineno}"


def test_the_source_carries_no_legacy_project_format_compatibility():
    for path in source_files():
        assert "project.pbxproj" not in path.read_text(encoding="utf-8"), str(path)


def test_the_repository_carries_the_required_infrastructure():
    for path in REQUIRED_PATHS:
        assert path.exists(), str(path)


def test_the_reference_coverage_map_mentions_every_source_module():
    document = (ROOT / "docs" / "reference-coverage.md").read_text(encoding="utf-8")
    for path in source_files():
        if path.name == "__init__.py":
            continue
        relative = path.relative_to(SOURCE).as_posix()
        assert relative in document, f"Missing from docs/reference-coverage.md: {relative}"
