from tests.support.instances import Instances
from tests.support.round_trip import RoundTrip
from xcodefy.library.schema.references.folder.exception_sets.target_exception_set import TargetExceptionSet
from xcodefy.library.schema.values.local_target_reference import LocalTargetReference


def test_the_target_is_always_written():
    assert RoundTrip.text(TargetExceptionSet(LocalTargetReference("App"))) == '{\n  "target": "App",\n}\n'


def test_the_header_overrides_are_written_when_present():
    text = RoundTrip.text(Instances.populated_target_exception_set())
    assert '"public-headers"' in text
    assert '"private-headers"' in text
    assert '"compiler-flags"' in text


def test_a_populated_set_round_trips():
    RoundTrip.expect_equal(Instances.populated_target_exception_set(), TargetExceptionSet)
