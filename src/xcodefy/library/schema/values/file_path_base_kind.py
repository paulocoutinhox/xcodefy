from xcodefy.library.serialization.codable_str_enum import CodableStrEnum


class FilePathBaseKind(CodableStrEnum):
    ABSOLUTE = "absolute"
    GROUP = "group"
    PROJECT = "PROJECT"
    DEVELOPER = "DEVELOPER"
    BUILD_PRODUCTS = "PRODUCTS"
    SDK = "SDK"
    SOURCE_ROOT = "source-root"
