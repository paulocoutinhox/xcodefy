import pytest

from tests.support.documentation import Documentation

FIXTURE = '{ "default-configuration": "Debug", "localizations": { "development": "en" }, "files": [], "targets": [ { "name": "MyApp", "id": "APP1", "product-type": "application", "build-phases": [ "compile-sources", "resources" ] } ] }'


def bundle_at(directory):
    bundle = directory / "MyApp.xcodeproj"
    bundle.mkdir()
    (bundle / "project.xcproj").write_text(FIXTURE, encoding="utf-8")
    return bundle


@pytest.mark.parametrize("document", Documentation.documents(), ids=lambda path: path.name)
def test_every_documented_example_runs(document, tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    bundle_at(tmp_path)
    namespace = {"__name__": "documentation"}
    for index, block in enumerate(Documentation.blocks(document)):
        try:
            exec(compile(block, f"{document.name}#{index}", "exec"), namespace)
        except Exception as error:
            pytest.fail(f"{document.name} block {index} failed with {type(error).__name__}: {error}\n\n{block}")
    capsys.readouterr()


@pytest.mark.parametrize("document", Documentation.documents(), ids=lambda path: path.name)
def test_every_documented_file_carries_examples(document):
    assert Documentation.blocks(document), f"{document.name} carries no python example"


def test_the_expected_documents_are_the_ones_that_exist():
    assert all(document.exists() for document in Documentation.documents())
    assert len(Documentation.documents()) == 4
