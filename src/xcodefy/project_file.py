import os
from pathlib import Path
from tempfile import mkstemp

from xcodefy.errors.decode_error import DecodeError
from xcodefy.library.utilities.text import Text

PROJECT_FILE_NAME = "project.xcproj"
PROJECT_BUNDLE_SUFFIX = ".xcodeproj"
READ_ENCODING = "utf-8-sig"
WRITE_ENCODING = "utf-8"
DOCUMENT_NEWLINE = "\n"
STAGED_SUFFIX = ".staged"
DEFAULT_MODE = 0o644


class ProjectFile:
    @staticmethod
    def resolve(path: str | Path) -> Path:
        resolved = Path(path)
        return resolved / PROJECT_FILE_NAME if resolved.suffix == PROJECT_BUNDLE_SUFFIX else resolved

    @staticmethod
    def read(path: Path) -> str:
        try:
            return path.read_bytes().decode(READ_ENCODING)
        except UnicodeDecodeError as error:
            raise DecodeError(f"{Text.quoted(str(path))} is not valid UTF-8 text.") from error

    @staticmethod
    def write(path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        staged = ProjectFile._stage(path)
        try:
            staged.write_text(text, encoding=WRITE_ENCODING, newline=DOCUMENT_NEWLINE)
            staged.chmod(ProjectFile._mode(path))
            staged.replace(path)
        except BaseException:
            staged.unlink(missing_ok=True)
            raise

    @staticmethod
    def _stage(path: Path) -> Path:
        handle, name = mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=STAGED_SUFFIX)
        os.close(handle)
        return Path(name)

    @staticmethod
    def _mode(path: Path) -> int:
        try:
            return path.stat().st_mode & 0o7777
        except FileNotFoundError:
            return DEFAULT_MODE
