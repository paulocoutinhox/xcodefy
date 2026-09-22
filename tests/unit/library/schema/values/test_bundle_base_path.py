from xcodefy.library.schema.values.bundle_base_path import BundleBasePath


def test_every_bundle_location_from_the_reference_schema_is_represented():
    expected = [
        "root",
        "build-products-directory",
        "shared-frameworks-directory",
        "shared-support-directory",
        "java-directory",
        "frameworks-directory",
        "resources-directory",
        "package-info-file",
        "apple-scripts-directory",
        "plugins-directory",
        "private-headers-directory",
        "headers-directory",
        "contents-directory",
        "executables-directory",
        "info-plist-file",
        "main-executable-file",
        "shallow-main-executable-file",
    ]
    assert [member.value for member in BundleBasePath] == expected
