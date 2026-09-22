from tests.support.round_trip import RoundTrip
from xcodefy.library.schema.references.common_reference_properties import CommonReferenceProperties


def test_an_unset_index_flag_is_omitted():
    assert RoundTrip.text(CommonReferenceProperties()) == "{\n}\n"


def test_both_index_values_are_written_when_set():
    assert RoundTrip.text(CommonReferenceProperties(True)) == '{\n  "index": true,\n}\n'
    assert RoundTrip.text(CommonReferenceProperties(False)) == '{\n  "index": false,\n}\n'


def test_the_properties_round_trip():
    RoundTrip.expect_equal(CommonReferenceProperties(False), CommonReferenceProperties)
