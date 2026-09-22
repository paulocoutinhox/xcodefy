HELP_TEXT = """The xcodefy tool pretty prints "project.xcproj" Xcode project files in their canonical format.

Usage:

    xcodefy [[--input] input-project] [--output output-project]
    xcodefy --update project
    xcodefy --help
    xcodefy --version

Arguments:
    --input     The path to an Xcode project. It can refer to the outer ".xcodeproj" directory, or the inner "project.xcproj" file.
    --output    The path to an Xcode project. It can refer to the outer ".xcodeproj" directory, or the inner "project.xcproj" file.
    --update    A short hand for passing --input and --output with the same value.
    --version   Print the installed version.

Example invocations:

    # Updates "Project.xcodeproj/project.xcproj" in place.
    xcodefy --update Project.xcodeproj

    # Reads a project file on standard input, pretty prints it, and writes it to standard output.
    xcodefy

    # Reads "Project.xcodeproj/project.xcproj", pretty prints it, and writes it to standard output.
    xcodefy Project.xcodeproj

    # Reads "Project.xcodeproj/project.xcproj", pretty prints it, and writes it to standard output.
    xcodefy --input Project.xcodeproj

    # Reads "Input.xcodeproj/project.xcproj", pretty prints it, and writes it to "Output.xcodeproj/project.xcproj".
    xcodefy --input Input.xcodeproj --output Output.xcodeproj
"""


class Help:
    @staticmethod
    def text() -> str:
        return HELP_TEXT
