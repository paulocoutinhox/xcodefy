from tests.support.instances import Instances
from tests.support.round_trip import RoundTrip
from xcodefy.library.schema.build_rules.build_rule import BuildRule


def test_a_default_rule_writes_only_the_processor():
    assert RoundTrip.text(BuildRule()) == '{\n  "processor": "",\n}\n'


def test_run_once_per_architecture_is_only_written_when_disabled():
    assert '"run-once-per-architecture"' not in RoundTrip.text(BuildRule(run_once_per_architecture=True))
    assert '"run-once-per-architecture": false' in RoundTrip.text(BuildRule(run_once_per_architecture=False))


def test_an_absent_script_is_omitted():
    assert '"script"' not in RoundTrip.text(BuildRule())


def test_a_multiline_script_encodes_as_an_array_of_lines():
    assert '"script": [\n    "one",\n    "two",\n  ],' in RoundTrip.text(BuildRule(script="one\ntwo"))


def test_an_empty_script_is_distinct_from_an_absent_one():
    RoundTrip.expect_equal(BuildRule(script=""), BuildRule)
    assert '"script": ""' in RoundTrip.text(BuildRule(script=""))


def test_a_populated_rule_round_trips():
    RoundTrip.expect_equal(Instances.populated_build_rule(), BuildRule)


def test_a_rule_can_be_copied_with_a_new_script():
    assert Instances.populated_build_rule().copy(script="echo").script == "echo"
