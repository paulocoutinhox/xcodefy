from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Self

from xcodefy.library.schema.values.file_type_id import FileTypeID
from xcodefy.library.schema.values.multiline_text import MultilineText
from xcodefy.library.schema.values.object_id import ObjectID
from xcodefy.library.serialization.decoders import Decoders
from xcodefy.library.utilities.copy_with import CopyWith


@dataclass(slots=True)
class BuildRule(CopyWith):
    processor: str = ""
    name: str | None = None
    file_type: FileTypeID | None = None
    file_patterns: str | None = None
    script: str | None = None
    input_files: list[str] = field(default_factory=list)
    input_file_lists: list[str] = field(default_factory=list)
    output_files: list[str] = field(default_factory=list)
    output_file_lists: list[str] = field(default_factory=list)
    output_files_compiler_flags: list[str] = field(default_factory=list)
    dependency_file: str | None = None
    run_once_per_architecture: bool = True
    object_id: ObjectID | None = None

    def encode(self, coder: Any) -> None:
        container = coder.keyed()
        container.put("name", self.name, None)
        container.put("id", self.object_id, None)
        container.put_unconditionally("processor", self.processor)
        container.put("file-type", self.file_type, None)
        container.put("file-patterns", self.file_patterns, None)
        container.put("input-files", self.input_files, [])
        container.put("input-file-lists", self.input_file_lists, [])
        container.put("output-files", self.output_files, [])
        container.put("output-file-lists", self.output_file_lists, [])
        container.put("output-files-compiler-flags", self.output_files_compiler_flags, [])
        container.put("dependency-file", self.dependency_file, None)
        container.put("run-once-per-architecture", self.run_once_per_architecture, True)
        container.put("script", None if self.script is None else MultilineText(self.script), None)

    @classmethod
    def decode(cls, coder: Any) -> Self:
        container = coder.keyed()
        name = container.get_if_present("name", Decoders.string)
        object_id = container.get_optional("id", ObjectID)
        processor = container.get("processor", Decoders.string)
        file_type = container.get_optional("file-type", FileTypeID)
        file_patterns = container.get_optional("file-patterns", Decoders.string)
        input_files = container.get_or_default("input-files", Decoders.array_of(Decoders.string), [])
        input_file_lists = container.get_or_default("input-file-lists", Decoders.array_of(Decoders.string), [])
        output_files = container.get_or_default("output-files", Decoders.array_of(Decoders.string), [])
        output_file_lists = container.get_or_default("output-file-lists", Decoders.array_of(Decoders.string), [])
        compiler_flags = container.get_or_default("output-files-compiler-flags", Decoders.array_of(Decoders.string), [])
        dependency_file = container.get_optional("dependency-file", Decoders.string)
        run_once_per_architecture = container.get_or_default("run-once-per-architecture", Decoders.boolean, True)
        script = container.get_if_present("script", MultilineText)
        return cls(processor, name, file_type, file_patterns, None if script is None else script.text, input_files, input_file_lists, output_files, output_file_lists, compiler_flags, dependency_file, run_once_per_architecture, object_id)
