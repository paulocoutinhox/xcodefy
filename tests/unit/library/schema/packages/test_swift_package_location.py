import pytest

from tests.support.round_trip import RoundTrip
from xcodefy.errors.validation_error import ValidationError
from xcodefy.library.schema.packages.local_swift_package import LocalSwiftPackage
from xcodefy.library.schema.packages.remote_swift_package import RemoteSwiftPackage
from xcodefy.library.schema.packages.swift_package_location import SwiftPackageLocation
from xcodefy.library.schema.packages.swift_package_location_kind import SwiftPackageLocationKind


def test_the_kind_is_always_written_ahead_of_the_content():
    location = SwiftPackageLocation.of_local(LocalSwiftPackage("./Local"))
    assert RoundTrip.text(location) == '{\n  "kind": "local",\n  "path": "./Local",\n}\n'


def test_both_kinds_round_trip():
    RoundTrip.expect_equal(SwiftPackageLocation.of_local(LocalSwiftPackage()), SwiftPackageLocation)
    RoundTrip.expect_equal(SwiftPackageLocation.of_remote(RemoteSwiftPackage("url")), SwiftPackageLocation)


def test_mismatched_content_is_rejected():
    with pytest.raises(ValidationError, match="requires RemoteSwiftPackage"):
        SwiftPackageLocation(SwiftPackageLocationKind.REMOTE, LocalSwiftPackage())
