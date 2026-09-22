from dataclasses import dataclass

from xcodefy.library.utilities.unescape_status import UnescapeStatus


@dataclass(frozen=True, slots=True)
class UnescapeResult:
    status: UnescapeStatus
    unescaped: str = ""
    remaining: str = ""
    character: str = ""
