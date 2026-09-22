from tests.support.instances import Instances
from tests.support.round_trip import RoundTrip
from xcodefy.library.schema.packages.local_swift_package import LocalSwiftPackage
from xcodefy.library.schema.packages.swift_package import SwiftPackage
from xcodefy.library.schema.packages.swift_package_location import SwiftPackageLocation


def test_the_location_is_written_inline_and_empty_traits_are_omitted():
    package = SwiftPackage(SwiftPackageLocation.of_local(LocalSwiftPackage("./Local")))
    assert RoundTrip.text(package) == '{\n  "kind": "local",\n  "path": "./Local",\n}\n'


def test_traits_are_written_when_present():
    package = SwiftPackage(SwiftPackageLocation.of_local(LocalSwiftPackage()), ["Trait"])
    assert '"traits": [\n    "Trait",\n  ],' in RoundTrip.text(package)
    RoundTrip.expect_equal(package, SwiftPackage)


def test_a_populated_package_round_trips():
    RoundTrip.expect_equal(Instances.populated_swift_package(), SwiftPackage)
