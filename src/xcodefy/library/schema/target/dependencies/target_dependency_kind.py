from xcodefy.library.serialization.codable_str_enum import CodableStrEnum


class TargetDependencyKind(CodableStrEnum):
    LOCAL_TARGET = "localTarget"
    REMOTE_TARGET = "remoteTarget"
    PACKAGE = "package"
