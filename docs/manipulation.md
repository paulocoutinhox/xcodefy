# Project manipulation

`XcodeProject` is the high-level API. It wraps a `Project` and the path it came from.

## Load and save

```python
from xcodefy.xcode_project import XcodeProject

project = XcodeProject.load("MyApp.xcodeproj")
project.save()
```

`load` and `save` accept the outer `.xcodeproj` bundle or the inner `project.xcproj` file. `save`
with no argument writes back to the path the project was loaded from, and raises `ValidationError`
for a project that was created in memory and never given a path.

`loads` and `dumps` are the in-memory equivalents.

## Targets

```python
from xcodefy.library.schema.target.common_target_properties import CommonTargetProperties
from xcodefy.library.schema.target.target import Target
from xcodefy.library.schema.values.object_id import ObjectID

project.add_target(Target.native(CommonTargetProperties("Widget", ObjectID("W1"))))
project.target("Widget")
project.remove_target("Widget")
```

Adding a target whose name is taken raises `ValidationError`. Looking up a name that does not exist
raises `KeyError`.

**Removing a target is transitive.** A build file that maps a file into a phase of a target that is
gone has no meaning, so the removal also drops:

- the build files that mapped a file reference, a variant group, a version group or an imported
  product into that target,
- the target from every folder's target membership, and every folder exception set that named it,
- the local dependency on it held by other targets, and their `test_host_target` when it pointed at
  it.

A build phase reference written as an object id carries no target name, so nothing can be concluded
about it and it is left untouched.

Removing a **file** is not transitive in the same way. A target is referenced by name and the format
guarantees target names are unique, which is what makes the repair unambiguous. A file is referenced
through a name path, such as a build configuration's xcconfig or a version group's current version,
and resolving a name path needs the tree context that this library deliberately does not provide,
exactly as the reference states. Those references are left as they are.

## Groups and files

```python
from xcodefy.library.schema.build_phases.build_phase_kind import BuildPhaseKind

project.add_group("Sources")
project.add_group("Helpers", parent="Sources")
project.add_file("Feature.swift", target="MyApp", group="Sources")
project.add_file("Info.plist", target="MyApp", build_phase=BuildPhaseKind.RESOURCES)
project.remove_file("Feature.swift", group="Sources")
```

**A path is relative to the group it is added to**, and to the project when no group is given. That
is what a `group` based `FilePath` means: it resolves against its parent reference. So
`add_file("Feature.swift", group="Sources")` lands at `Sources/Feature.swift`, and passing
`"Sources/Feature.swift"` would land at `Sources/Sources/Feature.swift` instead.

`add_file` attaches the file to a build phase that the target already carries. `build_phase` selects
the kind and defaults to the compile sources phase, and `build_phase_name` picks one when the target
has more than one phase of that kind. A target with no phase of the requested kind, or with several
and no name to choose between them, raises `ValidationError` rather than writing a reference that
resolves to nothing.

`files()` and `groups()` walk the whole tree, including nested groups, and `group(name)` finds one
by name anywhere in it. A name that matches nothing raises `KeyError`, and one that matches more than
one group raises `ValidationError`.

## Build settings

```python
project.set_build_setting("SDKROOT", "iphoneos")
project.set_build_setting("OTHER_SWIFT_FLAGS", ["-warnings-as-errors"], target="MyApp")
project.remove_build_setting("SDKROOT")
settings = project.build_settings("MyApp")
```

A string becomes a string setting and any other sequence becomes an array setting. Omitting `target`
reads and writes the project-level settings.

## Swift packages

```python
from xcodefy.library.schema.packages.local_swift_package import LocalSwiftPackage
from xcodefy.library.schema.packages.remote_swift_package import RemoteSwiftPackage
from xcodefy.library.schema.packages.swift_package import SwiftPackage
from xcodefy.library.schema.packages.swift_package_location import SwiftPackageLocation
from xcodefy.library.schema.packages.swift_package_version_constraint import SwiftPackageVersionConstraint

project.add_package(SwiftPackage(SwiftPackageLocation.of_local(LocalSwiftPackage("../Shared"))))

constraint = SwiftPackageVersionConstraint.up_to_next_major_version("1.4.0")
remote = RemoteSwiftPackage("https://github.com/example/Package.git", constraint)
project.add_package(SwiftPackage(SwiftPackageLocation.of_remote(remote)))
```

## Building a project from nothing

`tests/support/showcase.py` builds one, and it is the most complete worked example in the tree: 21
targets covering 16 product types across iOS, macOS, watchOS, tvOS, visionOS and DriverKit, every
build phase kind, a synchronised folder with exception sets, a localized variant group, a versioned
Core Data group, local and remote Swift packages, and real Swift sources on disk.

Two things it is worth copying. A path stored in a reference is relative to its parent, so a variant
group is a logical grouping with **no directory of its own** and its children carry the
`<language>.lproj/...` path, which is why the reference gives `VariantGroup` an empty default path.
And a target has to carry a build phase before a file can be added to it.

## Validation

```python
project.validate()
```

`validate` runs the same integrity checks the format applies when a project is encoded, so a
duplicate target name is reported before the document is written.
