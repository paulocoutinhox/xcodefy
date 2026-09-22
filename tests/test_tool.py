import io

import pytest

from xcodefy.errors.argument_error import ArgumentError
from xcodefy.tool.arguments import Arguments
from xcodefy.tool.help import Help
from xcodefy.tool.main import Main, main

MINIMAL = '{ "default-configuration": "Debug", "localizations": { "development": "en" }, "files": [] }\n'
FORMATTED = '{\n  "default-configuration": "Debug",\n  "localizations": {\n    "development": "en",\n  },\n  "files": [\n  ],\n}\n'


def write_project(directory, text=MINIMAL):
    bundle = directory / "Demo.xcodeproj"
    bundle.mkdir()
    (bundle / "project.xcproj").write_text(text, encoding="utf-8")
    return bundle


def test_arguments_accept_a_bare_input_path():
    assert Arguments.parse(["Demo.xcodeproj"]).input_path.name == "Demo.xcodeproj"


def test_arguments_accept_explicit_input_and_output():
    parsed = Arguments.parse(["--input", "In.xcodeproj", "--output", "Out.xcodeproj"])
    assert parsed.input_path.name == "In.xcodeproj"
    assert parsed.output_path.name == "Out.xcodeproj"


def test_update_sets_both_paths():
    parsed = Arguments.parse(["--update", "Demo.xcodeproj"])
    assert parsed.input_path == parsed.output_path


def test_help_is_recognised():
    assert Arguments.parse(["--help"]).help is True


def test_a_tilde_is_expanded():
    assert not str(Arguments.parse(["~/Demo.xcodeproj"]).input_path).startswith("~")


@pytest.mark.parametrize("argv", [["--input", "a", "--input", "b"], ["--output", "a", "--output", "b"], ["--update", "a", "--update", "b"], ["--input", "a", "--update", "b"], ["--input"], ["--output"], ["--update"], ["a", "b"], ["--unknown"]])
def test_invalid_argument_combinations_are_rejected(argv):
    with pytest.raises(ArgumentError):
        Arguments.parse(argv)


def test_help_text_mentions_the_tool_and_every_option():
    text = Help.text()
    assert "xcodefy" in text
    assert all(option in text for option in ["--input", "--output", "--update", "--help"])


def test_the_help_flag_prints_help(capsys):
    assert main(["--help"]) == 0
    assert "Usage" in capsys.readouterr().out


def test_standard_input_is_formatted_to_standard_output(capsysbinary, monkeypatch):
    monkeypatch.setattr("sys.stdin", io.TextIOWrapper(io.BytesIO(MINIMAL.encode("utf-8"))))
    assert main([]) == 0
    assert capsysbinary.readouterr().out == FORMATTED.encode("utf-8")


def test_a_project_bundle_is_formatted_to_standard_output(tmp_path, capsys):
    bundle = write_project(tmp_path)
    assert main([str(bundle)]) == 0
    assert capsys.readouterr().out == FORMATTED


def test_a_project_is_updated_in_place(tmp_path):
    bundle = write_project(tmp_path)
    assert main(["--update", str(bundle)]) == 0
    assert (bundle / "project.xcproj").read_text(encoding="utf-8") == FORMATTED


def test_an_output_bundle_is_created(tmp_path):
    bundle = write_project(tmp_path)
    output = tmp_path / "Out.xcodeproj"
    assert main(["--input", str(bundle), "--output", str(output)]) == 0
    assert (output / "project.xcproj").read_text(encoding="utf-8") == FORMATTED


def test_a_missing_input_reports_an_error_and_the_help(tmp_path, capsys):
    assert main([str(tmp_path / "Missing.xcodeproj")]) == 1
    captured = capsys.readouterr()
    assert "Usage" in captured.err


def test_malformed_input_reports_an_error(tmp_path, capsys):
    bundle = write_project(tmp_path, "{ not json")
    assert main([str(bundle)]) == 1
    assert capsys.readouterr().err != ""


def test_the_runner_is_reachable_through_the_class():
    assert Main.run(["--help"]) == 0
