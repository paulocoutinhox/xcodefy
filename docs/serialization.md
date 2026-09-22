# Serialization

`xcodefy.library.serialization` is independent of the schema. It provides the JSON5 reader, the
canonical printer, and the coder model that carries printing density.

## The value tree

`Value` is the JSON abstract syntax tree. Unlike a plain dictionary it keeps document order and
preserves comments, so a parsed document can be inspected without losing anything.

```python
from xcodefy.library.serialization.json import JSON

value = JSON.parse("{ a: 1, /* note */ b: [2,] }")
print(value.to_python())
```

## Reading

`Parser` accepts the JSON5 features Xcode writes and accepts: comments, trailing commas, unquoted
keys, single-quoted strings, hexadecimal numbers, escaped line continuations, and the JSON5 escape
set. Every failure is a `DecodeError` naming the line and column.

## Limits

Two things are rejected while reading, because both would otherwise surface much later as an error
no caller could reasonably catch.

A document may not nest more than `MAXIMUM_NESTING_DEPTH` levels. The limit is set so that any
document the parser accepts can also be decoded into the schema and written back, which is far
deeper than any real project: it allows 62 nested groups.

A `\uXXXX` escape in the high surrogate range must be followed by its low surrogate. The pair
decodes to the single character it denotes, so `"\ud83d\ude05.swift"` reads as an emoji file name.
An unpaired surrogate is a `DecodeError`, because it is not text and could not be written back out.

Bytes are decoded as `utf-8-sig`, so a document saved with a byte order mark reads as the text it
holds, and bytes that are not valid UTF-8 are a `DecodeError` rather than the `UnicodeDecodeError`
Python would raise. Output is always written as plain `utf-8` and never carries a signature.

## Printing density

The canonical format writes some nodes on a single line and spreads others across many. That choice
is not derivable from the value alone, so it travels beside it.

While encoding, a type records a `PrintingDensity` for the paths that should print compactly. Before
printing, `DensityValidator` walks the tree once and erases any compact request that a descendant
forbids, for example a nested line comment or a multi-line block comment. `Printer` then renders the
result.

```python
from xcodefy.library.serialization.encoder import Encoder
from xcodefy.library.serialization.encoding_options import EncodingOptions
from xcodefy.xcode_project import XcodeProject

loaded = XcodeProject.load("MyApp.xcodeproj")
print(Encoder.text_for(loaded.project, EncodingOptions.default()))
```

The coder encodes a schema value, which is why this passes `loaded.project` rather than the
`XcodeProject` wrapper. Handing it something it cannot encode reports an `EncodeError` naming the
type.

`EncodingOptions(add_trailing_newline=False)` suppresses the trailing newline.

## The coder model

Encoding opens exactly one container per value:

| Container | Opened with | Used for |
| --- | --- | --- |
| `PrimitiveEncodingContainer` | `coder.primitive()` | scalars |
| `OrdinalEncodingContainer` | `coder.ordinal(density)` | arrays |
| `KeyedEncodingContainer` | `coder.keyed(density)` | objects |

A keyed container omits a value that equals its default, rejects a key written twice, and rejects a
key that is not spear case unless it is written through `put_unverified`, which exists for dynamic
keys such as build setting names.

Decoding mirrors it with `coder.primitive()`, `coder.ordinal()` and `coder.keyed()`. Failures are
annotated with the coding path where they happened, for example `... at /targets[0]/build-phases`.

A keyed decoding container names how a key is read, because the format distinguishes the cases. An
optional field is read with `get_optional`, which treats a missing key and an explicit `null` alike,
so `{"id": null}` and a document with no `id` decode the same way. `get_optional_with_default` tells
the two apart, which is how `products-group` keeps its default when absent and becomes empty when
written as `null`. `get_if_present` only checks presence, so the few fields the format reads that way
reject a null.

## Extending the coder

A type joins the coder by defining `encode(self, coder)` and a `decode(cls, coder)` classmethod, or
`encode_inline(container)` and `decode_inline(container)` plus the `InlineKeyedCodable` mixin when it
writes its fields into an enclosing object. Nothing has to be inherited: the coder matches on the
methods.

`Encodable`, `Decodable` and `Codable` name that contract and are runtime checkable, so a type can be
verified against it.

```python
from xcodefy.library.schema.values.object_id import ObjectID
from xcodefy.library.serialization.codable import Codable

assert isinstance(ObjectID("A1"), Codable)
```

## Collections

`Decoders` supplies the combinators used by the schema: `array_of`, `set_of`, `dictionary_of`,
`keyed_dictionary_of` and `optional`. Sets and dictionaries encode in a deterministic order, and a
set that decodes with duplicate elements is an error.

`CompactArray` and `CompactDictionary` mark every element or value of a collection to print
compactly without making the collection itself compact.
