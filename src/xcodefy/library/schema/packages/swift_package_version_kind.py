from xcodefy.library.serialization.codable_str_enum import CodableStrEnum


class SwiftPackageVersionKind(CodableStrEnum):
    REVISION = "revision"
    BRANCH = "branch"
    VERSION = "version"
    VERSION_RANGE = "version-range"
    UP_TO_NEXT_MINOR_VERSION = "up-to-next-minor-version"
    UP_TO_NEXT_MAJOR_VERSION = "up-to-next-major-version"
