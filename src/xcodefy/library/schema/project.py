from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Any, Self

from xcodefy.errors.decode_error import DecodeError
from xcodefy.errors.validation_error import ValidationError
from xcodefy.library.schema.configuration import Configuration
from xcodefy.library.schema.packages.swift_package import SwiftPackage
from xcodefy.library.schema.references.file.file_reference import FileReference
from xcodefy.library.schema.references.reference import Reference
from xcodefy.library.schema.references.reference_kind import ReferenceKind
from xcodefy.library.schema.target.dependencies.remote_product import RemoteProduct
from xcodefy.library.schema.target.target import Target
from xcodefy.library.schema.values.build_setting import BuildSetting
from xcodefy.library.schema.values.capability import Capability
from xcodefy.library.schema.values.configuration_name import ConfigurationName
from xcodefy.library.schema.values.group_tree_reference import GroupTreeReference
from xcodefy.library.schema.values.marketing_version import MarketingVersion
from xcodefy.library.schema.values.object_id import ObjectID
from xcodefy.library.schema.values.project_localization_info import ProjectLocalizationInfo
from xcodefy.library.serialization.compact_array import CompactArray
from xcodefy.library.serialization.decoder import Decoder
from xcodefy.library.serialization.decoders import Decoders
from xcodefy.library.serialization.encoder import Encoder
from xcodefy.library.serialization.encoding_options import EncodingOptions
from xcodefy.library.utilities.sequences import Sequences
from xcodefy.library.utilities.text import Text

DEFAULT_PRODUCTS_REFERENCE = GroupTreeReference.of_child_names(["Products"])
GROUPED_FILE_KINDS = frozenset({ReferenceKind.VARIANT_GROUP, ReferenceKind.VERSION_GROUP})


@dataclass(slots=True)
class Project:
    top_level_references: list[Reference]
    default_configuration_name: ConfigurationName
    localization_info: ProjectLocalizationInfo
    packages: list[SwiftPackage] = field(default_factory=list)
    configurations: list[Configuration] = field(default_factory=list)
    build_settings: dict[str, BuildSetting] = field(default_factory=dict)
    targets: list[Target] = field(default_factory=list)
    required_capabilities: frozenset[Capability] = field(default_factory=frozenset)
    build_independent_targets_in_parallel: bool = True
    last_upgrade_check: MarketingVersion | None = None
    last_swift_update_check: MarketingVersion | None = None
    last_swift_migration: MarketingVersion | None = None
    organization_name: str | None = None
    class_prefix: str | None = None
    products_group: GroupTreeReference | None = DEFAULT_PRODUCTS_REFERENCE
    object_id: ObjectID | None = None
    root_group_debug_id: ObjectID | None = None
    configuration_list_debug_id: ObjectID | None = None
    imported_products: list[RemoteProduct] = field(default_factory=list)

    def verify_reference_integrity(self) -> None:
        duplicates = Sequences.duplicate_values(self.targets, target_name)
        if not duplicates:
            return
        verb = "is" if len(duplicates) == 1 else "are"
        names = Text.joined_with_final_separator([Text.smart_quoted(name) for name in sorted(duplicates)], ", ", " and ")
        raise ValidationError(f"Target names must be unique, but {names} {verb} used multiple times.")

    def encode(self, coder: Any) -> None:
        self.verify_reference_integrity()
        container = coder.keyed()
        container.put("required-capabilities", self.required_capabilities, frozenset())
        container.put("id", self.object_id, None)
        container.put("root-group-debug-id", self.root_group_debug_id, None)
        container.put("configuration-list-debug-id", self.configuration_list_debug_id, None)
        container.put("organization", self.organization_name, None)
        container.put("class-prefix", self.class_prefix, None)
        container.put("build-independent-targets-in-parallel", self.build_independent_targets_in_parallel, True)
        container.put_unconditionally("default-configuration", self.default_configuration_name)
        container.put("configurations", CompactArray.of(self.configurations), CompactArray())
        container.put_unconditionally("localizations", self.localization_info)
        container.put("imported-products", self.imported_products, [])
        container.put("packages", self.packages, [])
        container.put_unconditionally("files", self.top_level_references)
        container.put("targets", self.targets, [])
        container.put("build-settings", self.build_settings, {})
        # These trail the collections on purpose, because they are not the first thing a reader should see when opening a project.
        container.put("products-group", self.products_group, DEFAULT_PRODUCTS_REFERENCE)
        container.put("last-upgrade", self.last_upgrade_check, None)
        container.put("last-swift-update", self.last_swift_update_check, None)
        container.put("last-swift-migration", self.last_swift_migration, None)

    @classmethod
    def decode(cls, coder: Any) -> Self:
        container = coder.keyed()
        capabilities = container.get_or_default("required-capabilities", Decoders.set_of(Capability), frozenset())
        cls._verify_capabilities(capabilities, coder.tool_name)
        project = cls(**cls._decoded_fields(container, capabilities))
        project.verify_reference_integrity()
        return project

    @classmethod
    def _decoded_fields(cls, container: Any, capabilities: frozenset[Capability]) -> dict[str, Any]:
        return {
            "required_capabilities": capabilities,
            "object_id": container.get_optional("id", ObjectID),
            "root_group_debug_id": container.get_optional("root-group-debug-id", ObjectID),
            "configuration_list_debug_id": container.get_optional("configuration-list-debug-id", ObjectID),
            "top_level_references": container.get("files", Decoders.array_of(Reference)),
            "packages": container.get_or_default("packages", Decoders.array_of(SwiftPackage), []),
            "configurations": container.get_or_default("configurations", Decoders.array_of(Configuration), []),
            "default_configuration_name": container.get("default-configuration", ConfigurationName),
            "build_settings": container.get_or_default("build-settings", Decoders.dictionary_of(BuildSetting), {}),
            "targets": container.get_or_default("targets", Decoders.array_of(Target), []),
            "localization_info": container.get("localizations", ProjectLocalizationInfo),
            "build_independent_targets_in_parallel": container.get_or_default("build-independent-targets-in-parallel", Decoders.boolean, True),
            "last_upgrade_check": container.get_if_present("last-upgrade", MarketingVersion),
            "last_swift_update_check": container.get_if_present("last-swift-update", MarketingVersion),
            "last_swift_migration": container.get_if_present("last-swift-migration", MarketingVersion),
            "organization_name": container.get_if_present("organization", Decoders.string),
            "class_prefix": container.get_if_present("class-prefix", Decoders.string),
            "products_group": container.get_optional_with_default("products-group", GroupTreeReference, DEFAULT_PRODUCTS_REFERENCE),
            "imported_products": container.get_or_default("imported-products", Decoders.array_of(RemoteProduct), []),
        }

    @staticmethod
    def _verify_capabilities(capabilities: frozenset[Capability], tool_name: str) -> None:
        unsatisfied = sorted(capability.raw_value for capability in capabilities if not capability.is_satisfied)
        if not unsatisfied:
            return
        listed = Text.joined_with_final_separator(unsatisfied, ", ", " and ")
        raise DecodeError(f"The project requires a newer version of {tool_name} with support for {listed}.")

    @classmethod
    def from_json_text(cls, text: str | bytes) -> Self:
        return Decoder.decode_text(text, cls)

    def json_text(self, options: EncodingOptions | None = None) -> str:
        return Encoder.text_for(self, options or EncodingOptions.default())

    def json_data(self, options: EncodingOptions | None = None) -> bytes:
        return Encoder.data_for(self, options or EncodingOptions.default())

    def target(self, name: str) -> Target:
        matches = [target for target in self.targets if target.name == name]
        if not matches:
            raise KeyError(name)
        if len(matches) > 1:
            raise ValidationError(f"Target name {Text.smart_quoted(name)} is ambiguous.")
        return matches[0]

    def references(self) -> Iterator[Reference]:
        for reference in self.top_level_references:
            yield from walk_reference(reference)

    def file_references(self) -> Iterator[FileReference]:
        for reference in self.references():
            yield from file_references_of(reference)


def target_name(target: Target) -> str:
    return target.name


def walk_reference(reference: Reference) -> Iterator[Reference]:
    yield reference
    if reference.kind is not ReferenceKind.GROUP:
        return
    for child in reference.content.children:
        yield from walk_reference(child)


def file_references_of(reference: Reference) -> Iterator[FileReference]:
    if reference.kind is ReferenceKind.FILE_REFERENCE:
        yield reference.content
    elif reference.kind in GROUPED_FILE_KINDS:
        yield from reference.content.children
