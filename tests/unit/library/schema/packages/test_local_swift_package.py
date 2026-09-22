from tests.support.round_trip import RoundTrip
from xcodefy.library.schema.packages.local_swift_package import LocalSwiftPackage


def test_the_path_is_always_written():
    assert RoundTrip.text(LocalSwiftPackage("./Local")) == '{\n  "path": "./Local",\n}\n'
    assert RoundTrip.text(LocalSwiftPackage()) == '{\n  "path": "",\n}\n'


def test_a_local_package_round_trips():
    RoundTrip.expect_equal(LocalSwiftPackage("./Local"), LocalSwiftPackage)
