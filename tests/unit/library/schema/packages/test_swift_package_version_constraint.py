import pytest

from tests.support.round_trip import RoundTrip
from xcodefy.errors.decode_error import DecodeError
from xcodefy.library.schema.packages.swift_package_version_constraint import SwiftPackageVersionConstraint
from xcodefy.library.serialization.decoder import Decoder
from xcodefy.library.serialization.values.value import Value


@pytest.mark.parametrize(
    ("constraint", "key", "value"),
    [
        (SwiftPackageVersionConstraint.revision("abc"), "revision", "abc"),
        (SwiftPackageVersionConstraint.branch("main"), "branch", "main"),
        (SwiftPackageVersionConstraint.version("1.0"), "version", "1.0"),
        (SwiftPackageVersionConstraint.up_to_next_minor_version("1.0"), "up-to-next-minor-version", "1.0"),
        (SwiftPackageVersionConstraint.up_to_next_major_version("1.0"), "up-to-next-major-version", "1.0"),
    ],
)
def test_each_simple_constraint_encodes_under_its_own_key(constraint, key, value):
    assert RoundTrip.text(constraint) == f'{{\n  "{key}": "{value}",\n}}\n'
    RoundTrip.expect_equal(constraint, SwiftPackageVersionConstraint)


def test_a_plain_version_range_uses_the_compact_spelling():
    constraint = SwiftPackageVersionConstraint.version_range("1.0", "1.5")
    assert RoundTrip.text(constraint) == '{\n  "version-range": "1.0..<1.5",\n}\n'
    RoundTrip.expect_equal(constraint, SwiftPackageVersionConstraint)


def test_a_range_with_unusual_bounds_uses_separate_keys():
    constraint = SwiftPackageVersionConstraint.version_range("a", "b")
    assert RoundTrip.text(constraint) == '{\n  "version-range-min": "a",\n  "version-range-max": "b",\n}\n'
    RoundTrip.expect_equal(constraint, SwiftPackageVersionConstraint)


@pytest.mark.parametrize(("value", "expected"), [("1", True), ("1.0", True), ("", True), ("a", False), ("1-beta", False)])
def test_only_digits_and_dots_count_as_a_basic_version_number(value, expected):
    assert SwiftPackageVersionConstraint.is_basic_version_number(value) is expected


def test_an_ambiguous_combined_range_is_rejected():
    payload = Value.from_python({"version-range": "1..<2..<3"})
    with pytest.raises(DecodeError, match="Unexpected version range value"):
        Decoder.decode_value(payload, SwiftPackageVersionConstraint)
