import os
import threading
from pathlib import Path

import pytest

from xcodefy.errors.decode_error import DecodeError
from xcodefy.project_file import ProjectFile


def test_a_bundle_path_resolves_to_the_inner_project_file():
    assert ProjectFile.resolve("Demo.xcodeproj") == Path("Demo.xcodeproj/project.xcproj")


def test_an_inner_project_file_is_returned_unchanged():
    assert ProjectFile.resolve("Demo.xcodeproj/project.xcproj") == Path("Demo.xcodeproj/project.xcproj")


def test_an_unrelated_path_is_returned_unchanged():
    assert ProjectFile.resolve("somewhere/else.json") == Path("somewhere/else.json")


def test_a_path_object_is_accepted():
    assert ProjectFile.resolve(Path("Demo.xcodeproj")) == Path("Demo.xcodeproj/project.xcproj")


def test_reading_and_writing_round_trips(tmp_path):
    target = tmp_path / "project.xcproj"
    ProjectFile.write(target, "{}\n")
    assert ProjectFile.read(target) == "{}\n"


def test_writing_creates_a_missing_parent_directory(tmp_path):
    target = tmp_path / "Demo.xcodeproj" / "project.xcproj"
    ProjectFile.write(target, "{}\n")
    assert target.read_text(encoding="utf-8") == "{}\n"


def test_writing_leaves_no_staging_file_behind(tmp_path):
    target = tmp_path / "project.xcproj"
    ProjectFile.write(target, "{}\n")
    assert [path.name for path in tmp_path.iterdir()] == ["project.xcproj"]


def test_a_failed_write_leaves_the_original_untouched(tmp_path):
    target = tmp_path / "project.xcproj"
    ProjectFile.write(target, "original\n")
    with pytest.raises(UnicodeEncodeError):
        ProjectFile.write(target, "\ud800")
    assert target.read_text(encoding="utf-8") == "original\n"
    assert [path.name for path in tmp_path.iterdir()] == ["project.xcproj"]


def test_writing_replaces_an_existing_file(tmp_path):
    target = tmp_path / "project.xcproj"
    ProjectFile.write(target, "first\n")
    ProjectFile.write(target, "second\n")
    assert ProjectFile.read(target) == "second\n"


def test_a_file_that_is_not_utf8_reports_a_decode_error(tmp_path):
    target = tmp_path / "project.xcproj"
    target.write_bytes(b'{ "path": "caf\xe9.swift" }')
    with pytest.raises(DecodeError, match="not valid UTF-8"):
        ProjectFile.read(target)


def test_a_byte_order_mark_is_an_encoding_signature_and_not_content(tmp_path):
    target = tmp_path / "project.xcproj"
    target.write_bytes(b"\xef\xbb\xbf{}\n")
    assert ProjectFile.read(target) == "{}\n"


def test_writing_never_emits_a_byte_order_mark(tmp_path):
    target = tmp_path / "project.xcproj"
    ProjectFile.write(target, "{}\n")
    assert target.read_bytes() == b"{}\n"


def test_concurrent_writers_all_succeed_and_leave_one_complete_document(tmp_path):
    target = tmp_path / "project.xcproj"
    ProjectFile.write(target, "original\n")
    documents = [f"writer {index}\n" for index in range(6)]
    failures: list[BaseException] = []

    def write(document):
        for _ in range(40):
            try:
                ProjectFile.write(target, document)
            except BaseException as error:
                failures.append(error)

    threads = [threading.Thread(target=write, args=(document,)) for document in documents]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert failures == []
    assert [path.name for path in tmp_path.iterdir()] == ["project.xcproj"]
    assert target.read_text(encoding="utf-8") in documents


def test_an_interrupt_during_a_write_removes_the_staging_file(tmp_path, monkeypatch):
    target = tmp_path / "project.xcproj"
    ProjectFile.write(target, "original\n")

    def interrupt(self, text, **arguments):
        raise KeyboardInterrupt

    monkeypatch.setattr(Path, "write_text", interrupt)
    with pytest.raises(KeyboardInterrupt):
        ProjectFile.write(target, "replacement\n")
    monkeypatch.undo()
    assert target.read_text(encoding="utf-8") == "original\n"
    assert [path.name for path in tmp_path.iterdir()] == ["project.xcproj"]


@pytest.mark.skipif(os.name != "posix", reason="file mode bits are a POSIX concept")
def test_an_existing_project_keeps_its_permissions(tmp_path):
    target = tmp_path / "project.xcproj"
    ProjectFile.write(target, "original\n")
    target.chmod(0o640)
    ProjectFile.write(target, "replacement\n")
    assert target.stat().st_mode & 0o777 == 0o640


@pytest.mark.skipif(os.name != "posix", reason="file mode bits are a POSIX concept")
def test_a_new_project_is_not_created_private_to_its_owner(tmp_path):
    target = tmp_path / "project.xcproj"
    ProjectFile.write(target, "x\n")
    assert target.stat().st_mode & 0o777 == 0o644


def test_the_document_is_written_with_the_newline_the_format_uses(tmp_path):
    target = tmp_path / "project.xcproj"
    ProjectFile.write(target, "{\n}\n")
    assert target.read_bytes() == b"{\n}\n"
