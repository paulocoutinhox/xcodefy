import pytest

from xcodefy.errors.validation_error import ValidationError
from xcodefy.library.schema.values.file_path_base import FilePathBase
from xcodefy.library.schema.values.file_path_base_kind import FilePathBaseKind


def test_each_constructor_produces_the_matching_kind():
    assert FilePathBase.absolute().kind is FilePathBaseKind.ABSOLUTE
    assert FilePathBase.group().kind is FilePathBaseKind.GROUP
    assert FilePathBase.project().kind is FilePathBaseKind.PROJECT
    assert FilePathBase.developer().kind is FilePathBaseKind.DEVELOPER
    assert FilePathBase.build_products().kind is FilePathBaseKind.BUILD_PRODUCTS
    assert FilePathBase.sdk().kind is FilePathBaseKind.SDK
    assert FilePathBase.source_root("VAR").build_setting == "VAR"


def test_a_build_setting_is_required_exactly_for_a_source_root_base():
    with pytest.raises(ValidationError, match="source root base"):
        FilePathBase(FilePathBaseKind.SOURCE_ROOT)
    with pytest.raises(ValidationError, match="source root base"):
        FilePathBase(FilePathBaseKind.GROUP, "VAR")


@pytest.mark.parametrize(("base", "variable"), [(FilePathBase.project(), "PROJECT"), (FilePathBase.developer(), "DEVELOPER"), (FilePathBase.build_products(), "PRODUCTS"), (FilePathBase.sdk(), "SDK")])
def test_the_built_in_bases_expose_an_expansion_variable(base, variable):
    assert base.built_in_expansion_variable == variable
    assert FilePathBase.from_expansion_variable(variable) == base


@pytest.mark.parametrize("base", [FilePathBase.absolute(), FilePathBase.group(), FilePathBase.source_root("VAR")])
def test_the_remaining_bases_have_no_expansion_variable(base):
    assert base.built_in_expansion_variable is None


def test_an_unknown_expansion_variable_is_not_recognised():
    assert FilePathBase.from_expansion_variable("UNKNOWN") is None
