from tests.support.instances import Instances
from tests.support.round_trip import RoundTrip
from xcodefy.library.schema.target.dependencies.remote_target import RemoteTarget


def test_every_field_is_written_unconditionally():
    assert RoundTrip.text(Instances.populated_remote_target()) == '{\n  "project": "../Sources/Foo.swift",\n  "target": "OtherTarget",\n  "target-id": "0123456789ABCDEF",\n}\n'


def test_a_remote_target_round_trips():
    RoundTrip.expect_equal(Instances.populated_remote_target(), RemoteTarget)
