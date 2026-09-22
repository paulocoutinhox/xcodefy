from xcodefy.library.serialization.codable_str_enum import CodableStrEnum


class BundleBasePath(CodableStrEnum):
    ROOT = "root"
    PRODUCT_DIR = "build-products-directory"
    SHARED_FRAMEWORKS_DIR = "shared-frameworks-directory"
    SHARED_SUPPORT_DIR = "shared-support-directory"
    JAVA_DIR = "java-directory"
    FRAMEWORKS_DIR = "frameworks-directory"
    RESOURCES_DIR = "resources-directory"
    PKG_INFO = "package-info-file"
    APPLE_SCRIPTS_DIR = "apple-scripts-directory"
    PLUG_INS_DIR = "plugins-directory"
    PRIVATE_HEADERS_DIR = "private-headers-directory"
    HEADERS_DIR = "headers-directory"
    CONTENTS_DIR = "contents-directory"
    EXECUTABLES_DIR = "executables-directory"
    INFO_PLIST = "info-plist-file"
    MAIN_EXECUTABLE = "main-executable-file"
    MAIN_EXECUTABLE_SHALLOW = "shallow-main-executable-file"
