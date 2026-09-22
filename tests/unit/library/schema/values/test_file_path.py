import pytest

from tests.support.round_trip import RoundTrip
from xcodefy.errors.decode_error import DecodeError
from xcodefy.errors.validation_error import ValidationError
from xcodefy.library.schema.values.file_path import FilePath
from xcodefy.library.schema.values.file_path_base import FilePathBase


@pytest.mark.parametrize(
    ("base", "path", "representation"),
    [
        (FilePathBase.group(), "File.swift", "File.swift"),
        (FilePathBase.absolute(), "/File.swift", "/File.swift"),
        (FilePathBase.project(), "File.swift", "<PROJECT>/File.swift"),
        (FilePathBase.sdk(), "File.swift", "<SDK>/File.swift"),
        (FilePathBase.developer(), "File.swift", "<DEVELOPER>/File.swift"),
        (FilePathBase.build_products(), "File.swift", "<PRODUCTS>/File.swift"),
        (FilePathBase.source_root("SHARED"), "File.swift", "<USER:SHARED>/File.swift"),
    ],
)
def test_each_base_renders_its_canonical_prefix(base, path, representation):
    file_path = FilePath(base, path)
    assert file_path.string_representation == representation
    assert FilePath.from_string_representation(representation) == file_path


@pytest.mark.parametrize(("path", "representation"), [("<", "\\<"), ("\\", "\\\\"), ("<Readme.md", "\\<Readme.md"), ("\\Readme.md", "\\\\Readme.md"), ("./Readme.md", "./Readme.md")])
def test_angle_brackets_and_backslashes_are_escaped_in_plain_paths(path, representation):
    assert FilePath(FilePathBase.group(), path).string_representation == representation


@pytest.mark.parametrize("build_setting", ["<", ">", "$()", "custom"])
def test_the_source_root_build_setting_is_escaped(build_setting):
    RoundTrip.expect_equal(FilePath(FilePathBase.source_root(build_setting), "Readme.md"), FilePath)


def test_the_base_must_agree_with_the_absoluteness_of_the_path():
    with pytest.raises(ValidationError, match="Base disagrees"):
        FilePath(FilePathBase.group(), "/absolute")
    with pytest.raises(ValidationError, match="Base disagrees"):
        FilePath(FilePathBase.absolute(), "relative")


def test_a_tilde_prefixed_path_counts_as_absolute():
    assert FilePath(FilePathBase.absolute(), "~/Demo").string_representation == "~/Demo"


def test_an_unterminated_expansion_base_is_rejected():
    with pytest.raises(DecodeError, match="Unterminated path base"):
        FilePath.from_string_representation("<PROJECT")


def test_an_unknown_expansion_base_is_rejected():
    with pytest.raises(DecodeError, match="Invalid path base"):
        FilePath.from_string_representation("<UNKNOWN>/File.swift")


@pytest.mark.parametrize("value", ["<USER:VAR", "<USER:VAR>", "<USER:VAR\\"])
def test_a_malformed_source_root_encoding_is_rejected(value):
    with pytest.raises(DecodeError, match="Invalid file path encoding"):
        FilePath.from_string_representation(value)


def test_a_source_root_encoding_with_a_bad_escape_is_rejected():
    with pytest.raises(DecodeError, match="Invalid escape sequence"):
        FilePath.from_string_representation("<USER:\\q>/File.swift")


def test_the_file_name_is_the_last_path_component():
    assert FilePath(FilePathBase.group(), "a/b.swift").name == "b.swift"


def test_a_file_path_renders_as_its_string_representation():
    assert str(FilePath(FilePathBase.project(), "a")) == "<PROJECT>/a"


def test_a_file_path_encodes_as_an_inline_path_field():
    assert RoundTrip.text(FilePath(FilePathBase.group(), "a")) == '{\n  "path": "a",\n}\n'


def test_an_empty_group_path_is_omitted_from_the_encoding():
    assert RoundTrip.text(FilePath()) == "{\n}\n"
