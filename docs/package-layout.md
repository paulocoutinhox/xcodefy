# Package layout

The package mirrors the main areas of Apple's reference implementation.

```text
apple/xcode-project-format                 xcodefy
Sources/Library/Schema          ->         src/xcodefy/library/schema
Sources/Library/Serialization   ->         src/xcodefy/library/serialization
Sources/Library/Utilities       ->         src/xcodefy/library/utilities
Sources/Tool                    ->         src/xcodefy/tool
```

```text
src/xcodefy/
├── errors/                 the exception hierarchy, rooted at XcodefyError
├── library/
│   ├── schema/             one module per schema type
│   │   ├── build_files/
│   │   ├── build_phase_references/
│   │   ├── build_phases/
│   │   ├── build_rules/
│   │   ├── packages/
│   │   ├── references/
│   │   ├── target/
│   │   └── values/
│   ├── serialization/      the JSON5 reader, the canonical printer and the coder model
│   │   └── values/         the JSON value tree
│   └── utilities/          text, path, ordering and sequence helpers
├── tool/                   the xcodefy command-line formatter
├── project_file.py         resolves a .xcodeproj bundle to its inner file, and reads and writes it
├── target_references.py    removes every reference to a target when that target is removed
├── xcode_project.py        the high-level manipulation API
└── py.typed                marks the package as shipping type information
```

## Rules the layout follows

- Each source file declares at most one top-level class or enum.
- Every `__init__.py` is empty, so every import names the module that defines the type.
- `tests/unit` mirrors `src/xcodefy` one module for one module, and the mirroring is enforced in
  both directions by `tests/test_quality.py`.
- `tests/support` holds the fixtures shared by the behavioural tests.
