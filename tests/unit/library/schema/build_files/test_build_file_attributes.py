from tests.support.instances import Instances
from tests.support.round_trip import RoundTrip
from xcodefy.library.schema.build_files.build_file_attributes import BuildFileAttributes
from xcodefy.library.schema.build_files.code_generation import CodeGeneration
from xcodefy.library.schema.build_files.header_role import HeaderRole


def test_the_default_attributes_encode_to_nothing():
    assert BuildFileAttributes().everything_is_default is True
    assert RoundTrip.text(BuildFileAttributes()) == "{\n}\n"


def test_a_non_default_attribute_is_written():
    assert RoundTrip.text(BuildFileAttributes(header_role=HeaderRole.PUBLIC)) == '{\n  "header-role": "public",\n}\n'


def test_the_default_code_generation_and_header_preservation_are_omitted():
    attributes = BuildFileAttributes(code_generation=CodeGeneration.DEFAULT)
    assert "code-generation" not in RoundTrip.text(attributes)


def test_every_attribute_round_trips():
    RoundTrip.expect_equal(Instances.populated_build_file_attributes(), BuildFileAttributes)
    assert Instances.populated_build_file_attributes().everything_is_default is False
