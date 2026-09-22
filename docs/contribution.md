# Contribution

## Environment

```bash
make install
```

This creates the locked development environment with `uv`.

## Checks

```bash
make lint
make coverage
```

`make lint` runs `ruff check` and `ruff format --check`. `make format` applies both fixes.
`make coverage` runs the suite behind the 100% statement and branch coverage gate.

## Rules a change must respect

`tests/test_quality.py` enforces these, so a change that breaks one fails the suite.

- Only the new `project.xcproj` format is supported. No `project.pbxproj` compatibility.
- Every `__init__.py` stays empty.
- One top-level class or enum per source file.
- Every function signature and call stays on one physical line.
- No `TYPE_CHECKING` and no conditional typing imports.
- No semicolons combining statements.
- Every source module has a mirrored unit test module, and every unit test module mirrors a source
  module.

Code and comments are in English. Comments are rare, and are used only where names and structure
cannot carry the intent. Each one is a complete sentence.

## Checking that a test would catch a break

Coverage at 100% only says every line ran. Before trusting a new test, break the code it covers on
purpose and confirm the suite fails. A test that passes either way is worse than no test, because it
reads as protection.

Be especially careful with anything that depends on the environment, such as an encoding, a locale
or a file mode. `capsys` and `capsysbinary` capture text and byte writes identically, so a test using
them cannot tell the two apart. Run the tool through `subprocess` with the environment set instead.

## Changing a documented example

Every python block in `README.md` and under `docs/` is executed by `tests/test_documentation.py`,
in document order against a project fixture. An example has to run as written and has to create
whatever it uses, so a reader can copy it and have it work. Adding a page with examples means adding
it to the list in `tests/support/documentation.py`.

## Adding a schema type

1. Add the module under `src/xcodefy/library/schema`, one class per file.
2. Give it `encode(coder)` and `decode(coder)`, or `encode_inline(container)` and
   `decode_inline(container)` plus the `InlineKeyedCodable` mixin when the reference marks the type
   inline keyed.
3. Add a fixture to `tests/support/instances.py` and register it in `ROUND_TRIP_CASES`.
4. Add the mirrored unit test module covering construction, encoding, decoding and each error
   branch.

## Building

```bash
make build
make check
```
