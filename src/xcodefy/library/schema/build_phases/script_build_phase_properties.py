from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Self

from xcodefy.library.schema.build_phases.build_phase_properties import BuildPhaseProperties
from xcodefy.library.schema.build_phases.build_phase_scope import BuildPhaseScope
from xcodefy.library.schema.values.multiline_text import MultilineText
from xcodefy.library.serialization.decoders import Decoders
from xcodefy.library.serialization.inline_keyed_codable import InlineKeyedCodable
from xcodefy.library.serialization.printing_density import PrintingDensity
from xcodefy.library.utilities.copy_with import CopyWith


@dataclass(slots=True)
class ScriptBuildPhaseProperties(CopyWith, InlineKeyedCodable):
    base_properties: BuildPhaseProperties = field(default_factory=BuildPhaseProperties)
    shell_path: str = ""
    script: str = ""
    log_environment_variables: bool = False
    input_paths: list[str] = field(default_factory=list)
    input_file_list_paths: list[str] = field(default_factory=list)
    output_paths: list[str] = field(default_factory=list)
    output_file_list_paths: list[str] = field(default_factory=list)
    dependency_file: str | None = None
    run_on_every_build: bool = False
    scope: BuildPhaseScope = BuildPhaseScope.ALWAYS

    @property
    def name(self) -> str | None:
        return self.base_properties.name

    @property
    def printing_density(self) -> PrintingDensity | None:
        return None

    def encode_inline(self, container: Any) -> None:
        container.put_inline(self.base_properties)
        container.put("log-environment-variables", self.log_environment_variables, False)
        container.put("input-paths", self.input_paths, [])
        container.put("input-file-list-paths", self.input_file_list_paths, [])
        container.put("output-paths", self.output_paths, [])
        container.put("output-file-list-paths", self.output_file_list_paths, [])
        container.put("dependency-file", self.dependency_file, None)
        container.put("run-on-every-build", self.run_on_every_build, False)
        container.put("scope", self.scope, BuildPhaseScope.ALWAYS)
        container.put_unconditionally("shell", self.shell_path)
        container.put_unconditionally("script", MultilineText(self.script))

    @classmethod
    def decode_inline(cls, container: Any) -> Self:
        base_properties = container.get_inline(BuildPhaseProperties)
        log_environment_variables = container.get_or_default("log-environment-variables", Decoders.boolean, False)
        input_paths = container.get_or_default("input-paths", Decoders.array_of(Decoders.string), [])
        input_file_list_paths = container.get_or_default("input-file-list-paths", Decoders.array_of(Decoders.string), [])
        output_paths = container.get_or_default("output-paths", Decoders.array_of(Decoders.string), [])
        output_file_list_paths = container.get_or_default("output-file-list-paths", Decoders.array_of(Decoders.string), [])
        dependency_file = container.get_optional("dependency-file", Decoders.string)
        run_on_every_build = container.get_or_default("run-on-every-build", Decoders.boolean, False)
        scope = container.get_or_default("scope", BuildPhaseScope, BuildPhaseScope.ALWAYS)
        shell_path = container.get("shell", Decoders.string)
        script = container.get("script", MultilineText).text
        return cls(base_properties, shell_path, script, log_environment_variables, input_paths, input_file_list_paths, output_paths, output_file_list_paths, dependency_file, run_on_every_build, scope)
