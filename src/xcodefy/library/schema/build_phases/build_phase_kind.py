from xcodefy.library.serialization.codable_str_enum import CodableStrEnum


class BuildPhaseKind(CodableStrEnum):
    APPLE_SCRIPT = "apple-script"
    FRAMEWORKS = "frameworks"
    HEADERS = "headers"
    JAVA_ARCHIVE = "java-archive"
    RESOURCES = "resources"
    REZ = "rez"
    SOURCES = "compile-sources"
    COPY = "copy"
    SCRIPT = "script"

    @property
    def error_message_name(self) -> str:
        return ERROR_MESSAGE_NAMES[self]


ERROR_MESSAGE_NAMES = {
    BuildPhaseKind.APPLE_SCRIPT: "Apple Script",
    BuildPhaseKind.FRAMEWORKS: "Link Libraries & Frameworks",
    BuildPhaseKind.HEADERS: "Copy Headers",
    BuildPhaseKind.JAVA_ARCHIVE: "Java Archive",
    BuildPhaseKind.RESOURCES: "Copy Resources",
    BuildPhaseKind.REZ: "Rez",
    BuildPhaseKind.SOURCES: "Compile Sources",
    BuildPhaseKind.COPY: "Copy Files",
    BuildPhaseKind.SCRIPT: "Shell Script",
}
