# Schema overview

`xcodefy.library.schema` mirrors Apple's schema, one type per module. `Project` is the root: each
`project.xcproj` decodes to exactly one instance.

## The project

```text
Project
├── top_level_references : list[Reference]      the groups and files tree
├── targets              : list[Target]
├── configurations       : list[Configuration]
├── build_settings       : dict[str, BuildSetting]
├── packages             : list[SwiftPackage]
├── imported_products    : list[RemoteProduct]
├── localization_info    : ProjectLocalizationInfo
└── required_capabilities: frozenset[Capability]
```

A project verifies its own integrity when it is decoded and again before it is encoded. Duplicate
target names are rejected, and a document that declares a capability this version does not implement
is rejected before anything else is read.

## The groups and files tree

`Reference` is the tagged union for a node in the tree. Its `kind` selects the content type, and
`file-reference` is the default so it is omitted from the encoding.

| Kind | Content | Notes |
| --- | --- | --- |
| `file-reference` | `FileReference` | a file on disk, with optional type, encoding and line ending overrides |
| `group` | `Group` | a named node with `Reference` children; the name is omitted when it equals the last path component |
| `folder` | `Folder` | a directory synchronised from disk, steered by `FolderExceptionSet` entries |
| `variant-group` | `VariantGroup` | a localized resource whose children are its language variants |
| `version-group` | `VersionGroup` | a versioned source file such as a Core Data model |

## Targets

`Target` is a tagged union over `TargetKind`. `native` and `aggregate` carry
`CommonTargetProperties`; `external-build-system` carries `ExternalBuildSystemTargetProperties`,
which wraps the common properties and adds the build tool settings.

A target holds its dependencies, build phases, build rules, specialized configurations and build
settings, but not its files. Files inject themselves into a target through the `build_files` of the
reference that owns them.

## Build phases and build files

`BuildPhase` pairs a `BuildPhaseKind` with its properties. The six plain kinds collapse to a bare
kind string when their properties are all default; `apple-script`, `copy` and `script` always carry
an object because their properties are required.

`ProjectBuildFile` maps a file into a build phase when only the project is known, and collapses to a
bare string such as `"App/compile-sources"` when it carries nothing else. `TargetBuildFile` is the
same mapping when the target is already known from context.

## Paths and references

| Type | Purpose |
| --- | --- |
| `FilePath` | a path plus the virtual base it resolves against, such as `<PROJECT>/x` or `<USER:VAR>/x` |
| `NamePath` | a path through the tree by node name, which may contain `/` or look like `..` |
| `GroupTreeReference` | a node reference, either an `id:`-prefixed object id or a name path |
| `GroupTreeAnchoredReference` | a group tree node plus a relative path through the file system |
| `ObjectID` | an unambiguous identifier, used only where names cannot be unique |

## Value types

`AssetTag`, `ConfigurationName`, `FileTypeID`, `FolderMemberID`, `Language`,
`LocalTargetReference`, `ObjectID`, `PlatformFilter`, `ProductTypeID` and `SwiftPackageName` are all
string newtypes built on `TypedStringWrapper`. They carry a single `raw_value`, and two wrappers of
different types never compare equal.

`MarketingVersion`, `MultilineText`, `BuildSetting`, `TextEncoding` and `Capability` carry the
remaining value semantics that the format needs.
