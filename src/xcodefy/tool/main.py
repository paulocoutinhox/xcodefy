from __future__ import annotations

import sys
from collections.abc import Sequence
from pathlib import Path

from xcodefy.errors.xcodefy_error import XcodefyError
from xcodefy.project_file import ProjectFile
from xcodefy.tool.arguments import Arguments
from xcodefy.tool.help import Help
from xcodefy.version import Version
from xcodefy.xcode_project import XcodeProject

ERROR_SEPARATOR = "\n\n----------------------------\n\n"
STREAM_ENCODING = "utf-8"


class Main:
    @staticmethod
    def run(argv: Sequence[str] | None = None) -> int:
        try:
            return Main._run(Arguments.parse(argv if argv is not None else sys.argv[1:]))
        except (OSError, XcodefyError) as error:
            Main.write_error(f"{error}{ERROR_SEPARATOR}{Help.text()}")
            return 1

    @staticmethod
    def _run(arguments: Arguments) -> int:
        if arguments.help:
            Main.write_standard_output(Help.text())
            return 0
        if arguments.version:
            Main.write_standard_output(f"{Version.current()}\n")
            return 0
        source = Main.read_input(arguments.input_path)
        Main.write_output(XcodeProject.loads(source).dumps(), arguments.output_path)
        return 0

    @staticmethod
    def read_input(path: Path | None) -> str | bytes:
        if path is None:
            return sys.stdin.buffer.read()
        return ProjectFile.read(ProjectFile.resolve(path))

    @staticmethod
    def write_output(text: str, path: Path | None) -> None:
        if path is None:
            Main.write_standard_output(text)
            return
        ProjectFile.write(ProjectFile.resolve(path), text)

    @staticmethod
    def write_standard_output(text: str) -> None:
        sys.stdout.buffer.write(text.encode(STREAM_ENCODING))
        sys.stdout.buffer.flush()

    @staticmethod
    def write_error(text: str) -> None:
        sys.stderr.buffer.write(text.encode(STREAM_ENCODING))
        sys.stderr.buffer.flush()


def main(argv: Sequence[str] | None = None) -> int:
    return Main.run(argv)
