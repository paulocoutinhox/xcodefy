<p align="center">
    <a href="https://github.com/paulocoutinhox/xcodefy" target="_blank" rel="noopener noreferrer">
        <img width="420" src="extras/images/logo.png" alt="Xcodefy">
    </a>
</p>

<p align="center">
  <a href="https://pypi.org/project/xcodefy/"><img src="https://img.shields.io/pypi/v/xcodefy.svg" alt="PyPI version"></a>
  <a href="https://github.com/paulocoutinhox/xcodefy/actions/workflows/test.yml"><img src="https://github.com/paulocoutinhox/xcodefy/actions/workflows/test.yml/badge.svg" alt="Xcodefy - Test"></a>
  <a href="https://codecov.io/gh/paulocoutinhox/xcodefy"><img src="https://codecov.io/gh/paulocoutinhox/xcodefy/graph/badge.svg" alt="Coverage"></a>
  <a href="https://github.com/paulocoutinhox/xcodefy/blob/main/LICENSE.md"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT"></a>
  <a href="https://www.python.org"><img src="https://img.shields.io/badge/python-3.11%20|%203.14-blue.svg" alt="Python versions"></a>
</p>

<p align="center">
Modern Python library and command-line tool for the new Xcode <code>project.xcproj</code> project format.
</p>

<br>

## 🚀 Project

Xcodefy reads, writes, validates, formats, and manipulates the new JSON5-based Xcode project format introduced with Xcode 27.

The project follows the model published in Apple's open-source `xcode-project-format` repository while providing a Python-native API and packaging. It intentionally supports only the new `project.xcproj` format. The legacy `project.pbxproj` format is outside the scope of the library.

The internal package layout mirrors the main areas of Apple's implementation:

```text
apple/xcode-project-format                 xcodefy
Sources/Library/Schema          ->         src/xcodefy/library/schema
Sources/Library/Serialization   ->         src/xcodefy/library/serialization
Sources/Library/Utilities       ->         src/xcodefy/library/utilities
Sources/Tool                    ->         src/xcodefy/tool
```

Every model class and enum lives in its own Python file. Every class has a mirrored unit test file, and the complete suite is required to maintain 100% statement and branch coverage.

## ✨ Features

- [x] Read and write `project.xcproj`
- [x] Accept an outer `.xcodeproj` package or an inner `project.xcproj` file
- [x] JSON5 parser with comments, trailing commas, unquoted keys, single-quoted strings, hexadecimal numbers, and JSON5 escapes
- [x] Canonical pretty printer with ordered output, omitted defaults, and the reference's compact and multi-line layout rules
- [x] Complete Python model for projects, targets, references, build phases, build files, build rules, configurations, Swift packages, folder exception sets, imported products, and schema value types
- [x] High-level project manipulation API
- [x] Add and remove files and target membership
- [x] Add and remove targets
- [x] Add Swift package references
- [x] Edit project-level and target-level build settings
- [x] Validate project invariants and required capabilities
- [x] `xcodefy` command-line formatter equivalent to Apple's `xcprojformatter` workflow
- [x] Zero runtime dependencies
- [x] `uv` development workflow
- [x] Wheel and source distribution ready for PyPI
- [x] PyPI Trusted Publishing release workflow
- [x] 100% statement and branch coverage gate
- [x] Single-source version, managed through the Makefile

## 📦 Install

With pip:

```bash
pip install xcodefy
```

With uv:

```bash
uv add xcodefy
```

Xcodefy requires Python 3.11 or newer.

## 💡 Library usage

Load an Xcode project package:

```python
from xcodefy.xcode_project import XcodeProject

project = XcodeProject.load("MyApp.xcodeproj")
project.set_build_setting("SWIFT_VERSION", "6.0")
project.set_build_setting("PRODUCT_BUNDLE_IDENTIFIER", "com.example.myapp", target="MyApp")
project.save()
```

Add a Swift source file to a target. The path is relative to the group it is added to, so this one
lands at `Sources/Feature.swift`:

```python
from xcodefy.xcode_project import XcodeProject

project = XcodeProject.load("MyApp.xcodeproj")
project.add_group("Sources")
project.add_file("Feature.swift", target="MyApp", group="Sources")
project.save()
```

Add a local Swift package:

```python
from xcodefy.library.schema.packages.local_swift_package import LocalSwiftPackage
from xcodefy.library.schema.packages.swift_package import SwiftPackage
from xcodefy.library.schema.packages.swift_package_location import SwiftPackageLocation
from xcodefy.xcode_project import XcodeProject

project = XcodeProject.load("MyApp.xcodeproj")
project.add_package(SwiftPackage(SwiftPackageLocation.of_local(LocalSwiftPackage("../Shared"))))
project.save()
```

Add a target and a file to it:

```python
from xcodefy.library.schema.build_phases.build_phase import BuildPhase
from xcodefy.library.schema.build_phases.build_phase_kind import BuildPhaseKind
from xcodefy.library.schema.target.common_target_properties import CommonTargetProperties
from xcodefy.library.schema.target.target import Target
from xcodefy.library.schema.values.object_id import ObjectID
from xcodefy.xcode_project import XcodeProject

project = XcodeProject.load("MyApp.xcodeproj")
phases = [BuildPhase.of_kind(BuildPhaseKind.SOURCES)]
project.add_target(Target.native(CommonTargetProperties("Widget", ObjectID("W1"), build_phases=phases)))
project.add_group("Widget")
project.add_file("WidgetBundle.swift", target="Widget", group="Widget")
project.save()
```

The lower-level schema types are available directly from their modules. Package `__init__.py` files are deliberately empty, so imports always identify the concrete source module.

Reading a project and writing it back is idempotent: the output is the canonical rendering, so
running Xcodefy over an already-canonical document changes nothing.

## 🛠️ Command-line tool

Xcodefy includes a formatter with the same input/output workflow as the tool in Apple's reference package:

```text
xcodefy [[--input] input-project] [--output output-project]
xcodefy --update project
xcodefy --help
xcodefy --version
```

Update a project in place:

```bash
xcodefy --update MyApp.xcodeproj
```

Read from standard input and write canonical output to standard output:

```bash
cat project.xcproj | xcodefy
```

Format one project into another:

```bash
xcodefy --input Input.xcodeproj --output Output.xcodeproj
```

Both `Input.xcodeproj` and `Input.xcodeproj/project.xcproj` are valid paths.

## 🧪 Development

Install the locked development environment:

```bash
make install
```

Run the complete suite:

```bash
make test
```

Run the strict coverage gate:

```bash
make coverage
```

Run lint and formatting checks:

```bash
make lint
```

Build the wheel and source distribution:

```bash
make build
make check
```

## 📚 Documentation

- [Getting started](docs/getting-started.md)
- [Schema overview](docs/schema-overview.md)
- [Serialization](docs/serialization.md)
- [Project manipulation](docs/manipulation.md)
- [Command-line tool](docs/cli.md)
- [File format goals](docs/file-format-goals.md)
- [Package layout](docs/package-layout.md)
- [Apple reference coverage](docs/reference-coverage.md)
- [Contribution](docs/contribution.md)

## 🏷️ Releasing a new version

A release is driven by a matching Git tag. The version lives only in `pyproject.toml`, and the
Makefile is the only thing that writes it:

```bash
make version                    # show the current version
make set-version VERSION=0.0.2  # set it
make bump PART=patch            # or raise major, minor or patch
```

Commit the change, then push the matching tag:

```bash
git tag v0.0.2
git push origin v0.0.2
```

The release workflow runs lint and the full 100% coverage suite, verifies that the tag matches the declared package version, builds the wheel and source distribution with `uv`, validates both distributions with Twine, publishes to PyPI through Trusted Publishing, and creates the GitHub release.

Configure the PyPI Trusted Publisher for repository `paulocoutinhox/xcodefy`, workflow `release.yml`, and environment `pypi` before the first release.

## ☕ Buy me a coffee

Support the continuous development of this project.

<a href='https://ko-fi.com/A0A412XEV' target='_blank'><img height='36' style='border:0px;height:36px;' src='https://storage.ko-fi.com/cdn/kofi2.png?v=6' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>

## 📄 License

[MIT](http://opensource.org/licenses/MIT)

Copyright (c) 2026, Paulo Coutinho

Xcodefy is an independent project and is not affiliated with Apple Inc. Xcode, Swift, and Apple are trademarks of Apple Inc. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
