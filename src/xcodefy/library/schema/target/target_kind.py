from xcodefy.library.serialization.codable_str_enum import CodableStrEnum


class TargetKind(CodableStrEnum):
    NATIVE = "native"
    AGGREGATE = "aggregate"
    EXTERNAL_BUILD_SYSTEM = "external-build-system"
