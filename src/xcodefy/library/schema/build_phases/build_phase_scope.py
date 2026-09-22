from xcodefy.library.serialization.codable_str_enum import CodableStrEnum


class BuildPhaseScope(CodableStrEnum):
    ALWAYS = "always"
    INSTALL = "install"
