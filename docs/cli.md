# Command-line tool

Xcodefy installs an `xcodefy` executable that pretty prints `project.xcproj` files in their
canonical format. It mirrors the input and output workflow of the tool in Apple's reference package.

```text
xcodefy [[--input] input-project] [--output output-project]
xcodefy --update project
xcodefy --help
xcodefy --version
```

## Arguments

| Argument | Meaning |
| --- | --- |
| `--input` | The project to read. Either the outer `.xcodeproj` directory or the inner `project.xcproj` file. |
| `--output` | The project to write. Either form is accepted, and the bundle directory is created when needed. |
| `--update` | Shorthand for passing the same path as both input and output. |
| `--help` | Print the help text and exit. |
| `--version` | Print the installed version and exit. |

A bare path with no option is treated as the input. A leading `~` is expanded.

## Examples

Update a project in place:

```bash
xcodefy --update MyApp.xcodeproj
```

Read standard input and write canonical output to standard output:

```bash
cat project.xcproj | xcodefy
```

Format one project into another:

```bash
xcodefy --input Input.xcodeproj --output Output.xcodeproj
```

## Text encoding

A `project.xcproj` is UTF-8, so the tool reads and writes UTF-8 regardless of the locale it runs
under. A document read from a file or from a pipe may carry a byte order mark, which is treated as
the encoding signature it is, and output never carries one. Bytes that are not valid UTF-8 are
reported as a decode error rather than failing inside the interpreter.

## Exit codes

`0` on success. `1` when the arguments are invalid, the input cannot be read, or the document is not
a valid project. The error message and the help text are written to standard error.
