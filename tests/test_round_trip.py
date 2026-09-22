import pytest

from tests.support.instances import ROUND_TRIP_CASES, VERSION_CONSTRAINTS
from tests.support.round_trip import RoundTrip
from xcodefy.library.schema.packages.swift_package_version_constraint import SwiftPackageVersionConstraint


@pytest.mark.parametrize(("value", "decoder"), ROUND_TRIP_CASES, ids=lambda item: type(item).__name__)
def test_schema_values_round_trip(value, decoder):
    RoundTrip.expect_equal(value, decoder)


@pytest.mark.parametrize("constraint", VERSION_CONSTRAINTS, ids=lambda item: item.kind.value)
def test_version_constraints_round_trip(constraint):
    RoundTrip.expect_equal(constraint, SwiftPackageVersionConstraint)
