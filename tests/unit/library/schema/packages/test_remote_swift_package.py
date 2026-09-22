from tests.support.round_trip import RoundTrip
from xcodefy.library.schema.packages.remote_swift_package import RemoteSwiftPackage
from xcodefy.library.schema.packages.swift_package_version_constraint import SwiftPackageVersionConstraint


def test_the_repository_is_always_written_and_an_absent_version_is_omitted():
    assert RoundTrip.text(RemoteSwiftPackage("https://example.com/p.git")) == '{\n  "repository": "https://example.com/p.git",\n}\n'


def test_the_version_constraint_is_written_when_present():
    package = RemoteSwiftPackage("https://example.com/p.git", SwiftPackageVersionConstraint.branch("main"))
    assert '"version": {\n    "branch": "main",\n  },' in RoundTrip.text(package)
    RoundTrip.expect_equal(package, RemoteSwiftPackage)
