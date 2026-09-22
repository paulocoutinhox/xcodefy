from xcodefy.library.serialization.codable_str_enum import CodableStrEnum


class ReferenceKind(CodableStrEnum):
    FILE_REFERENCE = "file-reference"
    GROUP = "group"
    FOLDER = "folder"
    VARIANT_GROUP = "variant-group"
    VERSION_GROUP = "version-group"
