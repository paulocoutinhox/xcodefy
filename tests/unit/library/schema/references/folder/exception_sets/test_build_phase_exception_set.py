from tests.support.instances import Instances
from tests.support.round_trip import RoundTrip
from xcodefy.library.schema.references.folder.exception_sets.build_phase_exception_set import BuildPhaseExceptionSet


def test_the_build_phase_is_always_written():
    exception_set = BuildPhaseExceptionSet(Instances.populated_project_build_phase_reference())
    assert RoundTrip.text(exception_set) == '{\n  "build-phase": "App/script/Install man pages",\n}\n'


def test_a_populated_set_round_trips():
    RoundTrip.expect_equal(Instances.populated_build_phase_exception_set(), BuildPhaseExceptionSet)
