from xcodefy.library.serialization.codable_str_enum import CodableStrEnum


class HeaderPreservation(CodableStrEnum):
    KEEP = "keep"
    REMOVE_ON_COPY = "remove-on-copy"
