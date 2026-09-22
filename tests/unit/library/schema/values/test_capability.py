from xcodefy.library.schema.values.capability import Capability


def test_the_testing_capability_is_known_and_satisfied():
    assert Capability.known_capability_for_testing().is_satisfied is True


def test_an_unknown_capability_is_not_satisfied():
    assert Capability("glow in the dark").is_satisfied is False


def test_the_capability_description_is_the_raw_value():
    assert Capability.known_capability_for_testing().raw_value == "known capability for testing"
