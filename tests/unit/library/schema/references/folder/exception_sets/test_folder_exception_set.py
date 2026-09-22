import pytest

from tests.support.instances import Instances
from tests.support.round_trip import RoundTrip
from xcodefy.errors.decode_error import DecodeError
from xcodefy.errors.validation_error import ValidationError
from xcodefy.library.schema.references.folder.exception_sets.folder_exception_set import FolderExceptionSet
from xcodefy.library.serialization.decoder import Decoder
from xcodefy.library.serialization.values.value import Value


def test_a_set_is_either_a_target_set_or_a_build_phase_set():
    assert FolderExceptionSet.of_target(Instances.populated_target_exception_set()).build_phase is None
    assert FolderExceptionSet.of_build_phase(Instances.populated_build_phase_exception_set()).target is None


def test_a_set_rejects_carrying_neither_or_both():
    with pytest.raises(ValidationError, match="either a target set or a build phase set"):
        FolderExceptionSet()
    with pytest.raises(ValidationError, match="either a target set or a build phase set"):
        FolderExceptionSet(Instances.populated_target_exception_set(), Instances.populated_build_phase_exception_set())


def test_an_unrecognised_payload_is_rejected():
    with pytest.raises(DecodeError, match="Unknown exception set"):
        Decoder.decode_value(Value.from_python({}), FolderExceptionSet)


def test_both_forms_round_trip():
    RoundTrip.expect_equal(FolderExceptionSet.of_target(Instances.populated_target_exception_set()), FolderExceptionSet)
    RoundTrip.expect_equal(FolderExceptionSet.of_build_phase(Instances.populated_build_phase_exception_set()), FolderExceptionSet)
