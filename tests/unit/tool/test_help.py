from xcodefy.tool.help import Help


def test_the_help_text_names_the_tool_and_the_format():
    text = Help.text()
    assert "xcodefy" in text
    assert "project.xcproj" in text


def test_every_option_is_documented():
    text = Help.text()
    assert all(option in text for option in ["--input", "--output", "--update", "--help"])


def test_the_help_text_shows_the_argument_and_example_sections():
    text = Help.text()
    assert "Arguments:" in text
    assert "Example invocations:" in text
    assert text.endswith("\n")
