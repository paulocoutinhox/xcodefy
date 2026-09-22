from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Self

from xcodefy.errors.decode_error import DecodeError
from xcodefy.library.schema.build_files.build_file_attributes import BuildFileAttributes
from xcodefy.library.schema.references.folder.exception_sets.exception_set_sense import ExceptionSetSense
from xcodefy.library.schema.values.asset_tag import AssetTag
from xcodefy.library.schema.values.folder_member_id import FolderMemberID
from xcodefy.library.schema.values.platform_filter import PlatformFilter
from xcodefy.library.serialization.compact_dictionary import CompactDictionary
from xcodefy.library.serialization.decoders import Decoders
from xcodefy.library.serialization.inline_keyed_codable import InlineKeyedCodable
from xcodefy.library.utilities.text import Text

EMPTY_COMPACT_DICTIONARY = CompactDictionary.of({})


@dataclass(slots=True)
class CommonExceptionSetProperties(InlineKeyedCodable):
    sense: ExceptionSetSense = ExceptionSetSense.INCLUSIONS
    membership_exceptions: frozenset[FolderMemberID] = field(default_factory=frozenset)
    platform_filters_by_member: dict[FolderMemberID, frozenset[PlatformFilter]] = field(default_factory=dict)
    attributes_by_member: dict[FolderMemberID, BuildFileAttributes] = field(default_factory=dict)
    asset_tags_by_member: dict[FolderMemberID, frozenset[AssetTag]] = field(default_factory=dict)

    def encode_inline(self, container: Any) -> None:
        if self.membership_exceptions:
            container.put_unverified(self.sense.value, self.membership_exceptions)
        container.put("platforms", CompactDictionary.of(self.platform_filters_by_member), EMPTY_COMPACT_DICTIONARY)
        container.put("attributes", CompactDictionary.of(self.attributes_by_member), EMPTY_COMPACT_DICTIONARY)
        container.put("asset-tags", CompactDictionary.of(self.asset_tags_by_member), EMPTY_COMPACT_DICTIONARY)

    @classmethod
    def decode_inline(cls, container: Any) -> Self:
        sense, membership_exceptions = cls._decode_sense(container)
        platforms = container.get_or_default("platforms", Decoders.keyed_dictionary_of(FolderMemberID, Decoders.set_of(PlatformFilter)), {})
        attributes = container.get_or_default("attributes", Decoders.keyed_dictionary_of(FolderMemberID, BuildFileAttributes), {})
        asset_tags = container.get_or_default("asset-tags", Decoders.keyed_dictionary_of(FolderMemberID, Decoders.set_of(AssetTag)), {})
        return cls(sense, membership_exceptions, platforms, attributes, asset_tags)

    @classmethod
    def _decode_sense(cls, container: Any) -> tuple[ExceptionSetSense, frozenset[FolderMemberID]]:
        present = [sense for sense in ExceptionSetSense if container.contains(sense.value)]
        if len(present) == 1:
            return present[0], container.get_or_default(present[0].value, Decoders.set_of(FolderMemberID), frozenset())
        if not present:
            return ExceptionSetSense.INCLUSIONS, frozenset()
        expected = Text.joined_with_final_separator([Text.smart_quoted(sense.value) for sense in ExceptionSetSense], ", ", " or ")
        raise DecodeError(f"Multiple exception set senses. Expected one of {expected}.")
