import pytest

from tests.support.instances import Instances
from tests.support.round_trip import RoundTrip
from xcodefy.errors.decode_error import DecodeError
from xcodefy.library.schema.references.folder.exception_sets.common_exception_set_properties import CommonExceptionSetProperties
from xcodefy.library.schema.references.folder.exception_sets.exception_set_sense import ExceptionSetSense
from xcodefy.library.schema.values.folder_member_id import FolderMemberID
from xcodefy.library.serialization.decoder import Decoder
from xcodefy.library.serialization.values.value import Value


def test_empty_properties_encode_to_nothing():
    assert RoundTrip.text(CommonExceptionSetProperties()) == "{\n}\n"


@pytest.mark.parametrize("sense", list(ExceptionSetSense))
def test_the_sense_selects_the_membership_key(sense):
    properties = CommonExceptionSetProperties(sense, frozenset({FolderMemberID("a")}))
    assert f'"{sense.value}"' in RoundTrip.text(properties)
    RoundTrip.expect_equal(properties, CommonExceptionSetProperties)


def test_an_absent_membership_key_decodes_as_empty_inclusions():
    decoded = Decoder.decode_value(Value.from_python({}), CommonExceptionSetProperties)
    assert decoded.sense is ExceptionSetSense.INCLUSIONS
    assert decoded.membership_exceptions == frozenset()


def test_carrying_both_senses_is_rejected():
    payload = Value.from_python({"inclusions": ["a"], "exclusions": ["b"]})
    with pytest.raises(DecodeError, match="Multiple exception set senses"):
        Decoder.decode_value(payload, CommonExceptionSetProperties)


def test_the_per_member_maps_print_compactly():
    text = RoundTrip.text(Instances.populated_common_exception_set_properties())
    assert '"platforms": {\n    "File1.swift": [ "ios" ],\n  },' in text


def test_populated_properties_round_trip():
    RoundTrip.expect_equal(Instances.populated_common_exception_set_properties(), CommonExceptionSetProperties)
