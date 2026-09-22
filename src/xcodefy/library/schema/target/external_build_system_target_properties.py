from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Self

from xcodefy.library.schema.target.common_target_properties import CommonTargetProperties
from xcodefy.library.schema.target.target_kind import TargetKind
from xcodefy.library.serialization.decoders import Decoders
from xcodefy.library.serialization.inline_keyed_codable import InlineKeyedCodable
from xcodefy.library.utilities.copy_with import CopyWith


@dataclass(slots=True)
class ExternalBuildSystemTargetProperties(CopyWith, InlineKeyedCodable):
    common_properties: CommonTargetProperties
    build_tool_path: str = ""
    build_tool_arguments: str = ""
    build_tool_working_directory: str | None = None
    pass_build_settings_in_environment: bool = True

    def encode_inline(self, container: Any) -> None:
        self.common_properties.encode_with_kind(container, TargetKind.EXTERNAL_BUILD_SYSTEM)
        container.put_unconditionally("build-tool-path", self.build_tool_path)
        container.put("build-tool-arguments", self.build_tool_arguments, "")
        container.put("build-tool-working-directory", self.build_tool_working_directory, None)
        container.put("pass-build-settings-in-environment", self.pass_build_settings_in_environment, True)

    @classmethod
    def decode_inline(cls, container: Any) -> Self:
        common_properties = CommonTargetProperties.decode_inline(container)
        build_tool_path = container.get("build-tool-path", Decoders.string)
        build_tool_arguments = container.get_or_default("build-tool-arguments", Decoders.string, "")
        working_directory = container.get_optional("build-tool-working-directory", Decoders.string)
        pass_settings = container.get_or_default("pass-build-settings-in-environment", Decoders.boolean, True)
        return cls(common_properties, build_tool_path, build_tool_arguments, working_directory, pass_settings)
