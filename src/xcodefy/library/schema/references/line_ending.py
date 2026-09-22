from xcodefy.library.serialization.codable_str_enum import CodableStrEnum


class LineEnding(CodableStrEnum):
    LINE_FEED = "line-feed"
    CARRIAGE_RETURN = "carriage-return"
    CARRIAGE_RETURN_LINE_FEED = "carriage-return-line-feed"
    PRESERVE = "preserve"
