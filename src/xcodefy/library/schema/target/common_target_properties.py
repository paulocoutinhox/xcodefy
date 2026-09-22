from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Self

from xcodefy.errors.encode_error import EncodeError
from xcodefy.library.schema.build_phases.build_phase import BuildPhase
from xcodefy.library.schema.build_rules.build_rule import BuildRule
from xcodefy.library.schema.configuration import Configuration
from xcodefy.library.schema.target.dependencies.swift_package_product_target_member import SwiftPackageProductTargetMember
from xcodefy.library.schema.target.dependencies.target_dependency import TargetDependency
from xcodefy.library.schema.target.target_kind import TargetKind
from xcodefy.library.schema.values.build_setting import BuildSetting
from xcodefy.library.schema.values.group_tree_reference import GroupTreeReference
from xcodefy.library.schema.values.legacy_provisioning_style import LegacyProvisioningStyle
from xcodefy.library.schema.values.local_target_reference import LocalTargetReference
from xcodefy.library.schema.values.marketing_version import MarketingVersion
from xcodefy.library.schema.values.object_id import ObjectID
from xcodefy.library.schema.values.product_type_id import ProductTypeID
from xcodefy.library.serialization.compact_array import CompactArray
from xcodefy.library.serialization.decoders import Decoders
from xcodefy.library.utilities.copy_with import CopyWith
from xcodefy.library.utilities.sequences import Sequences
from xcodefy.library.utilities.text import Text


@dataclass(slots=True)
class CommonTargetProperties(CopyWith):
    name: str
    object_id: ObjectID
    configuration_list_debug_id: ObjectID | None = None
    dependencies: list[TargetDependency] = field(default_factory=list)
    build_phases: list[BuildPhase] = field(default_factory=list)
    build_rules: list[BuildRule] = field(default_factory=list)
    specialized_configurations: list[Configuration] = field(default_factory=list)
    build_settings: dict[str, BuildSetting] = field(default_factory=dict)
    product: GroupTreeReference | None = None
    product_type_id: ProductTypeID | None = None
    test_host_target: LocalTargetReference | None = None
    legacy_provisioning_style: LegacyProvisioningStyle | None = None
    legacy_team_id: str | None = None
    last_swift_update_check: MarketingVersion | None = None
    last_swift_migration: MarketingVersion | None = None
    package_product_target_members: list[SwiftPackageProductTargetMember] = field(default_factory=list)

    def verify_specialized_configurations(self) -> None:
        for configuration in self.specialized_configurations:
            if not configuration.is_specialized:
                quoted_configuration = Text.smart_quoted(configuration.name.raw_value)
                raise EncodeError(f"Redundant configuration specialization for {quoted_configuration} in {Text.smart_quoted(self.name)}.")

    def encode_with_kind(self, container: Any, kind: TargetKind) -> None:
        self.verify_specialized_configurations()
        container.put_unconditionally("name", self.name)
        container.put_unconditionally("id", self.object_id)
        container.put("configuration-list-debug-id", self.configuration_list_debug_id, None)
        container.put("kind", kind, TargetKind.NATIVE)
        container.put("product", self.product, None)
        self._encode_product_type(container)
        container.put("last-swift-update", self.last_swift_update_check, None)
        container.put("last-swift-migration", self.last_swift_migration, None)
        container.put("legacy-provisioning-style", self.legacy_provisioning_style, None)
        container.put("legacy-team-id", self.legacy_team_id, None)
        container.put("test-host-target", self.test_host_target, None)
        container.put("specialized-configurations", CompactArray.of(self.specialized_configurations), CompactArray())
        container.put("dependencies", self.dependencies, [])
        container.put("build-phases", self.build_phases, [])
        container.put("build-rules", self.build_rules, [])
        container.put("package-product-members", Sequences.sorted_on(self.package_product_target_members, sort_by_encoding_order), [])
        container.put("build-settings", self.build_settings, {})

    def _encode_product_type(self, container: Any) -> None:
        abbreviated = self.product_type_id.abbreviated_representation if self.product_type_id is not None else None
        if abbreviated is not None:
            container.put("product-type", abbreviated, None)
            return
        container.put("full-product-type", self.product_type_id, None)

    @classmethod
    def decode_inline(cls, container: Any) -> Self:
        name = container.get("name", Decoders.string)
        object_id = container.get("id", ObjectID)
        product = container.get_optional("product", GroupTreeReference)
        product_type_id = cls._decode_product_type(container)
        test_host_target = container.get_optional("test-host-target", LocalTargetReference)
        last_swift_update_check = container.get_optional("last-swift-update", MarketingVersion)
        last_swift_migration = container.get_optional("last-swift-migration", MarketingVersion)
        legacy_provisioning_style = container.get_optional("legacy-provisioning-style", LegacyProvisioningStyle)
        legacy_team_id = container.get_optional("legacy-team-id", Decoders.string)
        dependencies = container.get_or_default("dependencies", Decoders.array_of(TargetDependency), [])
        build_rules = container.get_or_default("build-rules", Decoders.array_of(BuildRule), [])
        build_phases = container.get_or_default("build-phases", Decoders.array_of(BuildPhase), [])
        specialized = container.get_or_default("specialized-configurations", Decoders.array_of(Configuration), [])
        build_settings = container.get_or_default("build-settings", Decoders.dictionary_of(BuildSetting), {})
        members = container.get_or_default("package-product-members", Decoders.array_of(SwiftPackageProductTargetMember), [])
        configuration_list_debug_id = container.get_optional("configuration-list-debug-id", ObjectID)
        return cls(name, object_id, configuration_list_debug_id, dependencies, build_phases, build_rules, specialized, build_settings, product, product_type_id, test_host_target, legacy_provisioning_style, legacy_team_id, last_swift_update_check, last_swift_migration, members)

    @classmethod
    def _decode_product_type(cls, container: Any) -> ProductTypeID | None:
        if container.contains("product-type"):
            return ProductTypeID.from_abbreviated(container.get("product-type", Decoders.string))
        return container.get_if_present("full-product-type", ProductTypeID)


def sort_by_encoding_order(member: SwiftPackageProductTargetMember) -> Any:
    return member.encoding_order
