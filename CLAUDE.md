# Xcodefy engineering specification

## Purpose

Xcodefy is a Python library and CLI for the new Xcode `project.xcproj` format. It implements the
public model of Apple's `xcode-project-format` package in idiomatic modern Python, and its output is
byte-for-byte identical to that reference's canonical rendering.

## Layout

| Path | Owns |
| --- | --- |
| `src/xcodefy/errors` | the exception hierarchy, rooted at `XcodefyError` |
| `src/xcodefy/library/utilities` | text escaping, path names, sequence helpers, ordering, value copying |
| `src/xcodefy/library/serialization` | the JSON5 reader, the canonical printer and the coder model, independent of the schema |
| `src/xcodefy/library/schema` | the project schema, one type per module |
| `src/xcodefy/tool` | the `xcodefy` command-line formatter |
| `src/xcodefy/project_file.py` | the project file on disk: resolving, reading and writing it |
| `src/xcodefy/target_references.py` | removing every reference to a target when that target is removed |
| `src/xcodefy/xcode_project.py` | the high-level manipulation API |
| `tests/unit` | one module mirroring each source module |
| `tests/support` | shared fixtures: schema instances, combinatorics, round trip assertions, the showcase builder, the documentation extractor |
| `tests/test_*.py` | behavioural tests for serialization, escaping, round tripping, manipulation, the CLI and repository invariants |

## Non-negotiable rules

- Support only the new `project.xcproj` format. No compatibility code for `project.pbxproj`.
- Keep every `__init__.py` completely empty.
- Keep one top-level class or enum per source file.
- Keep every function signature and call on one physical line.
- Do not use `TYPE_CHECKING` or conditional typing imports.
- Do not use semicolons to combine statements.
- Do not add generic fallbacks that hide malformed project data. Validate explicitly instead.
- Keep code and comments in English.
- Use comments only where names and structure cannot carry the intent. Each is a complete sentence.
- Delete a helper that has no caller. Nothing stays because the reference has it.

## Conventions

- A value type that lands in a set or a dictionary key is a frozen dataclass. An aggregate a caller
  manipulates is a mutable dataclass with list and dict fields.
- A model must not be constructible in an invalid state. What the format requires has no default.
- A string newtype derives from `TypedStringWrapper` and carries a single `raw_value`. Two wrappers
  of different types never compare equal.
- A string enum derives from `CodableStrEnum`. Members are plain `str`, so such a type must never
  define `encode`, which would shadow `str.encode`.
- A parameter is annotated with the type it is used as. `object` and `Any` are for values that
  genuinely have no narrower type.

## The coder model

A dictionary cannot carry the **printing density** that decides whether a node is written on one
line or across many, and that density is what makes the output canonical. Serialization therefore
goes through a coder, not through `dict`.

Encoding:

1. A type's `encode(coder)` opens exactly one container: `coder.primitive()`, `coder.ordinal()` or
   `coder.keyed(density)`.
2. The container records values and records a `PrintingDensity` for the paths that print compactly.
3. `Encoder` builds the `Value` tree and hands it, with the density map, to `Printer`.
4. `DensityValidator` walks the tree once and erases any compact request a descendant forbids, such
   as a nested line comment or a multi-line block comment.
5. `Printer` renders with two-space indentation, trailing commas, and the rule that packs runs of
   multi-line containers onto shared lines.

Decoding mirrors it: `decode(coder)` opens a container, and containers annotate every failure with
the coding path where it happened.

A type the reference marks `InlineKeyedCodable` exposes `encode_inline(container)` and
`decode_inline(container)` and inherits `InlineKeyedCodable`, which supplies the standalone
`encode` and `decode` pair. A type's `printing_density` is consumed by whichever type opens its
container: a `FileReference` prints compactly through `Reference`, not when encoded on its own.

`Group.decode_inline` takes the child decoder as an argument, because `Group` holds `Reference`
children and `Reference` holds a `Group`. Encoding needs nothing special, since the encoder
dispatches on the child object, so only decoding takes the type and `Reference.decode` passes it.

### Decode strategies

| Call | Missing key | Explicit `null` | Reference spelling |
| --- | --- | --- | --- |
| `get` | error | decoded, so usually an error | `decode(key)` |
| `get_or_default` | the default | decoded, so usually an error | `decode(key, defaultValue:)` |
| `get_optional` | `None` | `None` | `decode(key, defaultValue: nil)` |
| `get_optional_with_default` | the default | `None` | `decodeOptionalWithNonNilDefault` |
| `get_if_present` | `None` | decoded, so usually an error | `decodeIfPresent(key)` |

An optional field uses `get_optional`, so `{"id": null}` reads as an absent id. A field the
reference reads with `decodeIfPresent` rejects a null.

## Contracts

### Errors

- Reading a document raises `DecodeError` and nothing else. Nested failures carry their coding path,
  and `Decoder.decode_value` normalises anything else the schema raises onto that type.
- Writing raises `EncodeError` for a coder misuse and `ValidationError` for a schema rule the project
  breaks. A value the encoder cannot encode is a misuse and reports the type, the bar `json.dumps`
  sets. A decoder argument is a strategy rather than data, so a non-callable stays a `TypeError`.
- `ValidationError` is what a model raises when built in an invalid state, and what
  `XcodeProject.validate` raises.

Every failure Python would otherwise report as `ValueError`, `UnicodeDecodeError`,
`UnicodeEncodeError` or `RecursionError` is converted where it happens, so a caller has one
exception to catch and the CLI never shows a traceback.

### Limits

- The parser enforces `MAXIMUM_NESTING_DEPTH`, set so that **anything the parser accepts can also be
  decoded into the schema and written back out**. That property is the reason the limit exists.
- A `\uXXXX` escape in the high surrogate range must be followed by its low surrogate, and the pair
  decodes to the character it denotes. An unpaired surrogate is rejected where it enters.
- Bytes that are not valid UTF-8 are rejected at `ProjectFile.read` and `Decoder.decode_text`, the
  only two doors untrusted bytes come through.

### Encoding

- `ProjectFile` decodes bytes as `utf-8-sig`, so a byte order mark is read as the encoding signature
  it is, and writes plain `utf-8` with an explicit `\n` newline, so output never carries a signature
  and the canonical bytes are the same on every platform. Leaving the newline to the platform would
  write CRLF on Windows.
- The tool reads and writes **bytes** on the standard streams. A `project.xcproj` is UTF-8 by
  definition of the format, so its encoding is not the terminal's business and the tool behaves the
  same under `LC_ALL=C`.

### Writing a project file

A write is atomic and safe to run concurrently:

- It stages through a file whose name is unique to that write. A name derived from the target makes
  every concurrent writer collide on one path.
- It carries over the target's permissions, or uses 0644 for a new file, read with a single `stat`.
  Checking `exists` before `stat` reintroduces a race.
- It renames over the target, so a reader sees either the whole old document or the whole new one.
- Cleanup runs for `BaseException`, so an interrupt leaves no staging file in the bundle.

## The manipulation API

- A path is stored verbatim, so it is **relative to the group it is added to**, which is what a
  `group` based `FilePath` resolves against. `add_file("a.swift", group="Sources")` lands at
  `Sources/a.swift`.
- A file is only added to a build phase the target already carries, and only when exactly one phase
  matches, because a reference to a phase that does not exist or is ambiguous cannot resolve.
- Removing a target removes every reference to it. The format guarantees target names are unique, so
  a name identifies one target and the repair is unambiguous.
- Removing a file repairs nothing, because a file is referenced through a name path, which needs
  tree context the library does not resolve.

## Testing

- Every source module has a mirrored unit test module, and every unit test module mirrors a source
  module. `tests/test_quality.py` enforces the layout and style rules above.
- The suite maintains 100% statement and branch coverage with no exclusions.
- `tests/test_golden_output.py` pins the exact canonical rendering of a project covering folders,
  exception sets, variant and version groups, packages, an external build system target and imported
  products.
- `tests/test_showcase.py` builds a project from nothing covering every product type, platform,
  target kind, build phase kind and reference kind, and checks what a generator must get right:
  every referenced path exists on disk, every target membership names a phase its target has, every
  dependency names a target that exists, and the document is already canonical.
- `tests/test_documentation.py` executes every python block in `README.md` and `docs/`, in document
  order against a project fixture. An example must run as written and create whatever it uses.
- Before trusting a new test, break the code it covers and confirm the suite fails. Coverage says a
  line ran, not that a test would notice it breaking.
- A property about the environment, such as an encoding, a locale or a file mode, can only be tested
  in a subprocess that has that environment. `capsys` and `capsysbinary` capture text and byte writes
  identically and cannot tell the two apart.

## Verifying parity with the reference

Reading the Swift source is how a schema change is checked. When types are added or their fields
move, confirm all three:

- Every keyed encoder's **key sequence** matches in key, order and mode (unconditional,
  default-omitted, unverified).
- Every optional key's **default value** matches.
- Every key's **decode strategy** matches one of the five above.

## Tooling

`uv` manages the environment and builds the package.

```bash
make install
make lint
make format
make coverage
make build
make check
```

## Release

The version lives in `pyproject.toml` and nowhere else. Nothing in the source, the documentation or
the workflows repeats it, and a test enforces that. `make set-version VERSION=x.y.z` and
`make bump PART=major|minor|patch` are the only things that write it, and `xcodefy --version` reports
it from the installed package metadata.

Set the version, commit it, then push the matching `vX.Y.Z` tag. The release workflow validates that
the tag matches the declared version, runs the suite, builds the package, publishes through PyPI
Trusted Publishing, and creates the GitHub release.
