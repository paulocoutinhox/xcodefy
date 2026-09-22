from xcodefy.library.serialization.codable_str_enum import CodableStrEnum


class RelativeReference(CodableStrEnum):
    CURRENT = "."
    PARENT = ".."
