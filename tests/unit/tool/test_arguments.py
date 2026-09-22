import pytest

from xcodefy.errors.argument_error import ArgumentError
from xcodefy.tool.arguments import Arguments


def test_an_empty_command_line_selects_standard_streams():
    parsed = Arguments.parse([])
    assert parsed.input_path is None
    assert parsed.output_path is None
    assert parsed.help is False


def test_a_bare_path_becomes_the_input():
    assert str(Arguments.parse(["Demo.xcodeproj"]).input_path) == "Demo.xcodeproj"


def test_explicit_options_set_both_paths():
    parsed = Arguments.parse(["--input", "In", "--output", "Out"])
    assert (str(parsed.input_path), str(parsed.output_path)) == ("In", "Out")


def test_update_sets_input_and_output_to_the_same_path():
    parsed = Arguments.parse(["--update", "Demo"])
    assert parsed.input_path == parsed.output_path


def test_the_help_flag_is_recognised_anywhere():
    assert Arguments.parse(["--help"]).help is True
    assert Arguments.parse(["Demo", "--help"]).help is True


def test_a_leading_tilde_is_expanded():
    assert not str(Arguments.parse(["~/Demo"]).input_path).startswith("~")


@pytest.mark.parametrize(
    ("argv", "message"),
    [
        (["--input", "a", "--input", "b"], "Two values passed for '--input'"),
        (["--output", "a", "--output", "b"], "Two values passed for '--output'"),
        (["--update", "a", "--update", "b"], "Two values passed for output"),
        (["--output", "a", "--update", "b"], "Two values passed for output"),
        (["--input", "a", "--update", "b"], "Two values passed for input"),
        (["--input"], "Missing argument for '--input'"),
        (["--output"], "Missing argument for '--output'"),
        (["--update"], "Missing argument for '--update'"),
        (["a", "b"], "Unexpected argument"),
        (["--unknown"], "Unexpected argument"),
    ],
)
def test_invalid_command_lines_are_rejected(argv, message):
    with pytest.raises(ArgumentError, match=message):
        Arguments.parse(argv)


def test_the_version_flag_is_recognised():
    assert Arguments.parse(["--version"]).version is True
    assert Arguments.parse([]).version is False
