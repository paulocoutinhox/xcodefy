import io
import os
import subprocess
import sys

import pytest

from xcodefy.tool.help import Help
from xcodefy.tool.main import Main, main
from xcodefy.version import Version

MINIMAL = '{ "default-configuration": "Debug", "localizations": { "development": "en" }, "files": [] }\n'
FORMATTED = '{\n  "default-configuration": "Debug",\n  "localizations": {\n    "development": "en",\n  },\n  "files": [\n  ],\n}\n'


def bundle_at(directory, text=MINIMAL):
    bundle = directory / "Demo.xcodeproj"
    bundle.mkdir()
    (bundle / "project.xcproj").write_text(text, encoding="utf-8")
    return bundle


def test_help_is_printed_to_standard_output(capsys):
    assert main(["--help"]) == 0
    assert "Usage" in capsys.readouterr().out


def test_standard_input_is_read_when_no_path_is_given(capsysbinary, monkeypatch):
    monkeypatch.setattr("sys.stdin", io.TextIOWrapper(io.BytesIO(MINIMAL.encode("utf-8"))))
    assert Main.run([]) == 0
    assert capsysbinary.readouterr().out == FORMATTED.encode("utf-8")


def test_the_default_argv_comes_from_the_process(capsys, monkeypatch):
    monkeypatch.setattr("sys.argv", ["xcodefy", "--help"])
    assert Main.run() == 0
    assert "Usage" in capsys.readouterr().out


def test_an_inner_project_file_can_be_addressed_directly(tmp_path, capsys):
    bundle = bundle_at(tmp_path)
    assert main([str(bundle / "project.xcproj")]) == 0
    assert capsys.readouterr().out == FORMATTED


def test_an_output_bundle_is_created_on_demand(tmp_path):
    bundle = bundle_at(tmp_path)
    output = tmp_path / "nested" / "Out.xcodeproj"
    assert main(["--input", str(bundle), "--output", str(output)]) == 0
    assert (output / "project.xcproj").read_text(encoding="utf-8") == FORMATTED


def test_an_argument_error_reports_the_message_and_the_help(capsys):
    assert main(["--unknown"]) == 1
    captured = capsys.readouterr()
    assert "Unexpected argument" in captured.err
    assert "Usage" in captured.err


@pytest.mark.parametrize("text", ["{ not json", "[]", '{ "files": [] }'])
def test_invalid_project_content_is_reported(tmp_path, capsys, text):
    bundle = bundle_at(tmp_path, text)
    assert main([str(bundle)]) == 1
    assert capsys.readouterr().err != ""


def test_a_missing_file_is_reported(tmp_path, capsys):
    assert main([str(tmp_path / "Missing.xcodeproj")]) == 1
    assert "Usage" in capsys.readouterr().err


def test_a_project_that_is_not_utf8_reports_a_clean_error(tmp_path, capsys):
    bundle = tmp_path / "Demo.xcodeproj"
    bundle.mkdir()
    (bundle / "project.xcproj").write_bytes(b'{ "path": "caf\xe9.swift" }')
    assert main([str(bundle)]) == 1
    captured = capsys.readouterr()
    assert "not valid UTF-8" in captured.err
    assert "Usage" in captured.err


def piped(monkeypatch, data):
    monkeypatch.setattr("sys.stdin", io.TextIOWrapper(io.BytesIO(data)))


def test_output_is_utf8_bytes_whatever_the_locale(tmp_path, capsysbinary):
    bundle = tmp_path / "Emoji.xcodeproj"
    bundle.mkdir()
    document = MINIMAL.replace('"files": []', '"files": [ { "path": "\U0001f605.swift" } ]')
    (bundle / "project.xcproj").write_text(document, encoding="utf-8")
    assert main([str(bundle)]) == 0
    written = capsysbinary.readouterr().out
    assert "\U0001f605.swift".encode() in written
    assert written.decode("utf-8").startswith("{")


def test_input_on_a_pipe_that_is_not_utf8_reports_a_decode_error(monkeypatch, capsysbinary):
    piped(monkeypatch, b'{ "path": "caf\xe9" }')
    assert main([]) == 1
    assert b"not valid UTF-8" in capsysbinary.readouterr().err


def test_input_on_a_pipe_may_carry_a_byte_order_mark(monkeypatch, capsysbinary):
    piped(monkeypatch, b"\xef\xbb\xbf" + MINIMAL.encode("utf-8"))
    assert main([]) == 0
    assert capsysbinary.readouterr().out == FORMATTED.encode("utf-8")


def test_an_error_message_reaches_standard_error_as_utf8(tmp_path, capsysbinary):
    bundle = tmp_path / "Dup.xcodeproj"
    bundle.mkdir()
    document = MINIMAL.replace('"files": []', '"files": [], "targets": [ { "name": "A", "id": "1" }, { "name": "A", "id": "2" } ]')
    (bundle / "project.xcproj").write_text(document, encoding="utf-8")
    assert main([str(bundle)]) == 1
    assert "“A”".encode() in capsysbinary.readouterr().err


def test_the_help_text_is_written_as_utf8_bytes(capsysbinary):
    assert main(["--help"]) == 0
    assert capsysbinary.readouterr().out == Help.text().encode("utf-8")


def run_under_ascii_locale(tmp_path, arguments, stdin=b""):
    runner = "import sys; from xcodefy.tool.main import main; sys.exit(main(sys.argv[1:]))"
    environment = dict(os.environ, PYTHONIOENCODING="ascii", LC_ALL="C")
    return subprocess.run([sys.executable, "-c", runner, *arguments], input=stdin, capture_output=True, env=environment, cwd=tmp_path)


def test_output_does_not_depend_on_the_locale(tmp_path):
    bundle = tmp_path / "Emoji.xcodeproj"
    bundle.mkdir()
    document = MINIMAL.replace('"files": []', '"files": [ { "path": "\U0001f605.swift" } ]')
    (bundle / "project.xcproj").write_text(document, encoding="utf-8")
    result = run_under_ascii_locale(tmp_path, ["Emoji.xcodeproj"])
    assert result.returncode == 0, result.stderr.decode("utf-8", "replace")
    assert b"Traceback" not in result.stderr
    assert "\U0001f605.swift".encode() in result.stdout


def test_an_error_message_does_not_depend_on_the_locale(tmp_path):
    bundle = tmp_path / "Dup.xcodeproj"
    bundle.mkdir()
    document = MINIMAL.replace('"files": []', '"files": [], "targets": [ { "name": "A", "id": "1" }, { "name": "A", "id": "2" } ]')
    (bundle / "project.xcproj").write_text(document, encoding="utf-8")
    result = run_under_ascii_locale(tmp_path, ["Dup.xcodeproj"])
    assert result.returncode == 1
    assert b"Traceback" not in result.stderr
    assert "“A”".encode() in result.stderr


def test_a_pipe_that_is_not_utf8_does_not_depend_on_the_locale(tmp_path):
    result = run_under_ascii_locale(tmp_path, [], b'{ "path": "caf\xe9" }')
    assert result.returncode == 1
    assert b"Traceback" not in result.stderr
    assert b"not valid UTF-8" in result.stderr


def test_the_version_flag_prints_the_installed_version(capsysbinary):
    assert main(["--version"]) == 0
    assert capsysbinary.readouterr().out == f"{Version.current()}\n".encode()
