from xcodefy.library.serialization.codable_str_enum import CodableStrEnum


class SwiftPackageLocationKind(CodableStrEnum):
    LOCAL = "local"
    REMOTE = "remote"
