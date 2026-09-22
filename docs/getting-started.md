# Getting started

## Install

```bash
pip install xcodefy
```

```bash
uv add xcodefy
```

Xcodefy requires Python 3.11 or newer and has no runtime dependencies.

## Read a project

`XcodeProject.load` accepts either the outer `.xcodeproj` bundle or the inner `project.xcproj` file.

```python
from xcodefy.xcode_project import XcodeProject

project = XcodeProject.load("MyApp.xcodeproj")
print(project.project.default_configuration_name.raw_value)
```

## Write a project

`dumps` renders the canonical text, and `save` writes it back. Saving to the path the project was
loaded from needs no argument.

```python
project.set_build_setting("SWIFT_VERSION", "6.0")
project.save()
```

## Work in memory

```python
from xcodefy.xcode_project import XcodeProject

text = '{ "default-configuration": "Debug", "localizations": { "development": "en" }, "files": [] }'
project = XcodeProject.loads(text)
print(project.dumps())
```

## Import style

Every package `__init__.py` is empty on purpose, so every import names the concrete module that
defines the type.

```python
from xcodefy.library.schema.target.target import Target
from xcodefy.library.schema.values.object_id import ObjectID
```
