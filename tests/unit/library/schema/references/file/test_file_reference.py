import pytest

from tests.support.instances import Instances
from tests.support.round_trip import RoundTrip
from xcodefy.library.schema.references.file.file_reference import FileReference
from xcodefy.library.schema.references.reference import Reference
from xcodefy.library.schema.values.file_path import FilePath
from xcodefy.library.serialization.decoder import Decoder
from xcodefy.library.serialization.printing_density import PrintingDensity
from xcodefy.library.serialization.values.value import Value


def test_a_file_reference_is_only_printed_compactly_through_its_reference():
    assert RoundTrip.text(FileReference()) == "{\n}\n"
    assert RoundTrip.text(Reference.of_file(FileReference())) == "{}\n"


def test_a_reference_with_at_most_one_build_file_prints_compactly():
    reference = Instances.populated_file_reference()
    assert reference.printing_density is PrintingDensity.COMPACT
    reference.build_files.append(Instances.populated_project_build_file())
    assert reference.printing_density is None


def test_the_path_is_written_inline():
    assert RoundTrip.text(Reference.of_file(FileReference(Instances.populated_file_path()))) == '{ "path": "/Sources/Foo.swift" }\n'


def test_a_populated_reference_round_trips():
    RoundTrip.expect_equal(Instances.populated_file_reference(), FileReference)


@pytest.mark.parametrize("key", ["id", "type", "signature", "encoding", "line-ending", "index"])
def test_every_optional_field_accepts_an_explicit_null(key):
    payload = Value.from_python({"path": "a.swift", key: None})
    assert Decoder.decode_value(payload, Reference).content == FileReference(FilePath.from_string_representation("a.swift"))
