from enum import StrEnum


class UnescapeStatus(StrEnum):
    COMPLETE = "complete"
    UNESCAPED_SEQUENCE = "unescaped-sequence"
    INVALID_ESCAPE_SEQUENCE = "invalid-escape-sequence"
    UNRESOLVED_ESCAPE = "unresolved-escape"
