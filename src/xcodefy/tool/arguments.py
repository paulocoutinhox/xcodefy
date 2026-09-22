from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Self

from xcodefy.errors.argument_error import ArgumentError
from xcodefy.library.utilities.path_names import PathNames
from xcodefy.library.utilities.text import Text


@dataclass(slots=True)
class Arguments:
    input_path: Path | None = None
    output_path: Path | None = None
    help: bool = False
    version: bool = False

    @classmethod
    def parse(cls, command_line: Sequence[str]) -> Self:
        arguments = cls()
        remaining = list(command_line)
        while remaining:
            arguments._consume(remaining.pop(0), remaining)
        return arguments

    def _consume(self, current: str, remaining: list[str]) -> None:
        if current == "--help":
            self.help = True
        elif current == "--version":
            self.version = True
        elif current == "--input":
            self._set_input(Arguments._value(remaining, "--input"))
        elif current == "--output":
            self._set_output(Arguments._value(remaining, "--output"))
        elif current == "--update":
            self._set_update(Arguments._value(remaining, "--update"))
        elif self.input_path is None and not current.startswith("--"):
            self.input_path = Arguments._path(current)
        else:
            raise ArgumentError(f"Unexpected argument: {Text.quoted(current)}.")

    def _set_input(self, value: str) -> None:
        if self.input_path is not None:
            raise ArgumentError("Two values passed for '--input'.")
        self.input_path = Arguments._path(value)

    def _set_output(self, value: str) -> None:
        if self.output_path is not None:
            raise ArgumentError("Two values passed for '--output'.")
        self.output_path = Arguments._path(value)

    def _set_update(self, value: str) -> None:
        if self.output_path is not None:
            raise ArgumentError("Two values passed for output.")
        if self.input_path is not None:
            raise ArgumentError("Two values passed for input.")
        self.input_path = Arguments._path(value)
        self.output_path = self.input_path

    @staticmethod
    def _value(remaining: list[str], option: str) -> str:
        if not remaining:
            raise ArgumentError(f"Missing argument for '{option}'.")
        return remaining.pop(0)

    @staticmethod
    def _path(value: str) -> Path:
        return Path(PathNames.expanding_tilde(value))
