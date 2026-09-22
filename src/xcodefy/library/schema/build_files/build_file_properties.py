from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Self

from xcodefy.library.schema.build_files.build_file_attributes import BuildFileAttributes
from xcodefy.library.schema.values.asset_tag import AssetTag
from xcodefy.library.schema.values.platform_filter import PlatformFilter
from xcodefy.library.serialization.decoders import Decoders
from xcodefy.library.serialization.inline_keyed_codable import InlineKeyedCodable
from xcodefy.library.serialization.printing_density import PrintingDensity


@dataclass(frozen=True, slots=True)
class BuildFileProperties(InlineKeyedCodable):
    platform_filters: frozenset[PlatformFilter] = field(default_factory=frozenset)
    attributes: BuildFileAttributes = field(default_factory=BuildFileAttributes)
    additional_build_flags: str | None = None
    asset_tags: frozenset[AssetTag] = field(default_factory=frozenset)

    @property
    def everything_is_default(self) -> bool:
        return self == BuildFileProperties()

    def encode_inline(self, container: Any) -> None:
        container.put("platforms", self.platform_filters, frozenset(), PrintingDensity.COMPACT)
        container.put_inline(self.attributes)
        container.put("arguments", self.additional_build_flags, None)
        container.put("asset-tags", self.asset_tags, frozenset(), PrintingDensity.COMPACT)

    @classmethod
    def decode_inline(cls, container: Any) -> Self:
        platform_filters = container.get_or_default("platforms", Decoders.set_of(PlatformFilter), frozenset())
        attributes = container.get_inline(BuildFileAttributes)
        additional_build_flags = container.get_optional("arguments", Decoders.string)
        asset_tags = container.get_or_default("asset-tags", Decoders.set_of(AssetTag), frozenset())
        return cls(platform_filters, attributes, additional_build_flags, asset_tags)
