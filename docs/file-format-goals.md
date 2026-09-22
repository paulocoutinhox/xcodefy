# File format goals

The new `project.xcproj` format replaces the legacy `project.pbxproj` plist. The design goals
Xcodefy commits to are the ones Apple states for the reference implementation.

## Legible

The document is JSON5, so it accepts comments, trailing commas and unquoted keys. Names are spelled
out, and references are written by name wherever a name is unambiguous. Object identifiers appear
only where names cannot resolve a reference.

## Canonical

A project has exactly one correct rendering. Field order is fixed, defaults are omitted, collections
are written in a deterministic order, and each node is printed compactly or spread across lines
according to fixed rules. Reading a document and writing it back is idempotent.

## Merge friendly

The canonical rendering keeps unrelated edits on separate lines, and folder references synchronise
their content from disk instead of listing every file, so adding a file does not touch the project
document at all.

## Explicit

Malformed data is rejected rather than repaired. A document that declares a capability the reader
does not implement is rejected with a message naming the capability, so an older reader never
silently drops something it did not understand.

## What is out of scope

The legacy `project.pbxproj` format. Xcodefy contains no compatibility code for it, and
`tests/test_quality.py` enforces that.
