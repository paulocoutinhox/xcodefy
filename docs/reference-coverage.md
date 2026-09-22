# Apple reference coverage

This page maps every source file in Apple's `xcode-project-format` package to the Xcodefy module
that implements it. Swift keeps several types per file; Xcodefy keeps one per file, so most rows
fan out.

## Serialization

| Reference file | Xcodefy module |
| --- | --- |
| `Serialization/JSON.swift` | `library/serialization/json.py` |
| `Serialization/Values/Value.swift` | `library/serialization/values/value.py` |
| `Serialization/Values/ValueType.swift` | `library/serialization/values/value_type.py` |
| `Serialization/Values/Object.swift` | `library/serialization/values/object.py` |
| `Serialization/Values/Field.swift` | `library/serialization/values/field.py` |
| `Serialization/Values/FieldOrComment.swift` | `library/serialization/values/field_or_comment.py` |
| `Serialization/Values/ValueOrComment.swift` | `library/serialization/values/value_or_comment.py` |
| `Serialization/Values/Comment.swift` | `library/serialization/values/comment.py` |
| `Serialization/Values/CommentStyle.swift` | `library/serialization/values/comment_style.py` |
| `Serialization/Path.swift` | `library/serialization/absolute_path.py`, `library/serialization/path_component.py` |
| `Serialization/Printer.swift` | `library/serialization/printer.py`, `library/serialization/density_validator.py` |
| `Serialization/Encoder.swift` | `library/serialization/encoder.py`, `library/serialization/encoding_coder.py`, `library/serialization/encoding_container.py`, `library/serialization/primitive_encoding_container.py`, `library/serialization/ordinal_encoding_container.py`, `library/serialization/keyed_encoding_container.py`, `library/serialization/printing_density.py`, `library/serialization/encoding_options.py` |
| `Serialization/Decoder.swift` | `library/serialization/decoder.py`, `library/serialization/decoding_coder.py`, `library/serialization/decoding_container.py`, `library/serialization/primitive_decoding_container.py`, `library/serialization/ordinal_decoding_container.py`, `library/serialization/keyed_decoding_container.py` |
| `Serialization/Encodable.swift` | `library/serialization/encodable.py`, `library/serialization/inline_keyed_codable.py` |
| `Serialization/Decodable.swift` | `library/serialization/decodable.py` |
| `Serialization/Codable.swift` | `library/serialization/codable.py` |
| `Serialization/Conformances.swift` | `library/serialization/decoders.py`, `library/serialization/coding_order.py`, `library/serialization/codable_str_enum.py`, dispatch in `library/serialization/encoder.py` |
| `Serialization/CompactArray.swift` | `library/serialization/compact_array.py` |
| `Serialization/CompactDictionary.swift` | `library/serialization/compact_dictionary.py` |
| JSON5 reading (`Value.init(data:)`, `JSONSerialization`) | `library/serialization/parser.py` |

## Utilities

| Reference file | Xcodefy module |
| --- | --- |
| `Utilities/Utilities.swift` | `library/utilities/text.py`, `library/utilities/path_names.py`, `library/utilities/sequences.py`, `library/utilities/unescape_result.py`, `library/utilities/unescape_status.py` |
| `Utilities/LexigraphicalOrder.swift` | `library/utilities/lexicographical_order.py` |
| `Utilities/CopyWith.swift` | `library/utilities/copy_with.py` |
| `Utilities/Platform.swift` | not ported; a console script turns the value `main` returns into the exit status |

## Schema

| Reference file | Xcodefy module |
| --- | --- |
| `Schema/Schema.swift` | the `library/schema` package |
| `Schema/ShortNames.swift` | not ported; Swift's `package typealias` list has no Python equivalent and every import already names its defining module |
| `Schema/Project.swift` | `library/schema/project.py` |
| `Schema/Configuration.swift` | `library/schema/configuration.py` |
| `Schema/BuildFiles/BuildFile.swift` | `library/schema/build_files/project_build_file.py`, `library/schema/build_files/target_build_file.py`, `library/schema/build_files/build_file_properties.py` |
| `Schema/BuildFiles/BuildFileAttributes.swift` | `library/schema/build_files/build_file_attributes.py`, `library/schema/build_files/header_role.py`, `library/schema/build_files/header_preservation.py`, `library/schema/build_files/mach_interface_generation.py`, `library/schema/build_files/code_generation.py`, `library/schema/build_files/code_generation_visibility.py` |
| `Schema/BuildPhaseReferences/ProjectBuildPhaseReference.swift` | `library/schema/build_phase_references/project_build_phase_reference.py` |
| `Schema/BuildPhaseReferences/TargetBuildPhaseReference.swift` | `library/schema/build_phase_references/target_build_phase_reference.py` |
| `Schema/BuildPhases/BuildPhase.swift` | `library/schema/build_phases/build_phase.py`, `library/schema/build_phases/build_phase_kind.py` |
| `Schema/BuildPhases/BuildPhaseProperties.swift` | `library/schema/build_phases/build_phase_properties.py` |
| `Schema/BuildPhases/AppleScriptBuildPhaseProperties.swift` | `library/schema/build_phases/apple_script_build_phase_properties.py` |
| `Schema/BuildPhases/CopyFilesBuildPhaseProperties.swift` | `library/schema/build_phases/copy_files_build_phase_properties.py` |
| `Schema/BuildPhases/ScriptBuildPhaseProperties.swift` | `library/schema/build_phases/script_build_phase_properties.py` |
| `Schema/BuildPhases/BuildPhaseScope.swift` | `library/schema/build_phases/build_phase_scope.py` |
| `Schema/BuildRules/BuildRule.swift` | `library/schema/build_rules/build_rule.py` |
| `Schema/Packages/SwiftPackage.swift` | `library/schema/packages/swift_package.py` |
| `Schema/Packages/LocalSwiftPackage.swift` | `library/schema/packages/local_swift_package.py` |
| `Schema/Packages/RemoteSwiftPackage.swift` | `library/schema/packages/remote_swift_package.py` |
| `Schema/Packages/SwiftPackageLocation.swift` | `library/schema/packages/swift_package_location.py`, `library/schema/packages/swift_package_location_kind.py` |
| `Schema/Packages/SwiftPackageVersionConstraint.swift` | `library/schema/packages/swift_package_version_constraint.py`, `library/schema/packages/swift_package_version_kind.py` |
| `Schema/References/Reference.swift` | `library/schema/references/reference.py`, `library/schema/references/reference_kind.py`, `library/schema/references/common_reference_properties.py` |
| `Schema/References/File/FileReference.swift` | `library/schema/references/file/file_reference.py`, `library/schema/references/line_ending.py` |
| `Schema/References/FilePath.swift` | `library/schema/values/file_path.py`, `library/schema/values/file_path_base.py`, `library/schema/values/file_path_base_kind.py` |
| `Schema/References/Groups/Group.swift` | `library/schema/references/groups/group.py` |
| `Schema/References/Groups/VariantGroup.swift` | `library/schema/references/groups/variant_group.py` |
| `Schema/References/Groups/VersionGroup.swift` | `library/schema/references/groups/version_group.py` |
| `Schema/References/Folder/Folder.swift` | `library/schema/references/folder/folder.py` |
| `Schema/References/Folder/FolderMemberID.swift` | `library/schema/values/folder_member_id.py` |
| `Schema/References/Folder/ExceptionSets/FolderExceptionSet.swift` | `library/schema/references/folder/exception_sets/folder_exception_set.py`, `library/schema/references/folder/exception_sets/exception_set_sense.py` |
| `Schema/References/Folder/ExceptionSets/CommonExceptionSetProperties.swift` | `library/schema/references/folder/exception_sets/common_exception_set_properties.py` |
| `Schema/References/Folder/ExceptionSets/TargetExceptionSet.swift` | `library/schema/references/folder/exception_sets/target_exception_set.py` |
| `Schema/References/Folder/ExceptionSets/BuildPhaseExceptionSet.swift` | `library/schema/references/folder/exception_sets/build_phase_exception_set.py` |
| `Schema/Target/Target.swift` | `library/schema/target/target.py`, `library/schema/target/target_kind.py`, `library/schema/target/common_target_properties.py`, `library/schema/target/external_build_system_target_properties.py` |
| `Schema/Target/Dependencies/TargetDependency.swift` | `library/schema/target/dependencies/target_dependency.py`, `library/schema/target/dependencies/target_dependency_kind.py` |
| `Schema/Target/Dependencies/RemoteTarget.swift` | `library/schema/target/dependencies/remote_target.py` |
| `Schema/Target/Dependencies/RemoteTargetProduct.swift` | `library/schema/target/dependencies/remote_product.py` |
| `Schema/Target/Dependencies/SwiftPackageProductReference.swift` | `library/schema/target/dependencies/swift_package_product_reference.py` |
| `Schema/Target/Dependencies/SwiftPackageProductTargetMember.swift` | `library/schema/target/dependencies/swift_package_product_target_member.py` |
| `Schema/Values/TypedStringWrapper.swift` | `library/schema/values/typed_string_wrapper.py` |
| `Schema/Values/AssetTag.swift` | `library/schema/values/asset_tag.py` |
| `Schema/Values/BuildSetting.swift` | `library/schema/values/build_setting.py` |
| `Schema/Values/BundleBasePath.swift` | `library/schema/values/bundle_base_path.py` |
| `Schema/Values/Capability.swift` | `library/schema/values/capability.py` |
| `Schema/Values/ConfigurationName.swift` | `library/schema/values/configuration_name.py` |
| `Schema/Values/FileTypeID.swift` | `library/schema/values/file_type_id.py` |
| `Schema/Values/GroupTreeAnchoredReference.swift` | `library/schema/values/group_tree_anchored_reference.py` |
| `Schema/Values/GroupTreeReference.swift` | `library/schema/values/group_tree_reference.py` |
| `Schema/Values/Language.swift` | `library/schema/values/language.py` |
| `Schema/Values/LegacyProvisioningStyle.swift` | `library/schema/values/legacy_provisioning_style.py` |
| `Schema/Values/LocalTargetReference.swift` | `library/schema/values/local_target_reference.py` |
| `Schema/Values/MarketingVersion.swift` | `library/schema/values/marketing_version.py` |
| `Schema/Values/MultilineString.swift` | `library/schema/values/multiline_text.py` |
| `Schema/Values/NamePath.swift` | `library/schema/values/name_path.py`, `library/schema/values/name_path_component.py`, `library/schema/values/relative_reference.py` |
| `Schema/Values/ObjectID.swift` | `library/schema/values/object_id.py` |
| `Schema/Values/PlatformFilter.swift` | `library/schema/values/platform_filter.py` |
| `Schema/Values/ProductTypeID.swift` | `library/schema/values/product_type_id.py` |
| `Schema/Values/ProjectLocalizationInfo.swift` | `library/schema/values/project_localization_info.py` |
| `Schema/Values/String.Encoding+JSONCodable.swift` | `library/schema/values/string_encoding.py` |
| `Schema/Values/TextEncoding.swift` | `library/schema/values/text_encoding.py` |
| `Schema/Values/SwiftPackageName.swift` | `library/schema/values/swift_package_name.py` |
| `Schema/Values/SwiftPackageProductType.swift` | `library/schema/values/swift_package_product_type.py` |

## Tool

| Reference file | Xcodefy module |
| --- | --- |
| `Tool/main.swift` | `tool/main.py`, `project_file.py` |
| `Tool/Arguments.swift` | `tool/arguments.py` |
| `Tool/Help.swift` | `tool/help.py` |

## Tests

| Reference file | Xcodefy test |
| --- | --- |
| `Tests/JSONTests.swift` | `tests/test_json.py`, `tests/unit/library/serialization/test_printer.py`, `tests/unit/library/serialization/test_parser.py` |
| `Tests/RoundTripSomeOfEverythingTests.swift` | `tests/test_round_trip.py` |
| `Tests/TestInstances.swift` | `tests/support/instances.py` |
| `Tests/TestUtilities.swift` | `tests/support/combinatorics.py`, `tests/support/round_trip.py` |
| `Tests/TestStringEscapingDuringEncoding.swift` | `tests/test_string_escaping.py` |
| `Tests/UtilitiesTests.swift` | `tests/test_utilities.py`, `tests/unit/library/utilities/test_text.py` |
| `Tests/SampleData.swift` | not ported; it reads projects from an environment-provided directory |
| `Tests/TestPerformance.swift` | not ported; it is a release-build benchmark, not a correctness test |

## Python-only modules

These have no counterpart in the reference package. Swift models failures with `NSError` and exposes
no manipulation API above the schema, so both are additions.

| Xcodefy module | Purpose |
| --- | --- |
| `errors/xcodefy_error.py` | the root of the exception hierarchy |
| `errors/decode_error.py` | a failure while reading a document, annotated with its coding path |
| `errors/encode_error.py` | a failure while writing a document |
| `errors/validation_error.py` | a schema rule violation |
| `errors/argument_error.py` | an invalid command line |
| `xcode_project.py` | the high-level manipulation API |
| `target_references.py` | removes every reference to a target when that target is removed |

## Deliberate differences

- **Comments survive a read.** The reference reads JSON5 through `JSONSerialization`, which discards
  comments. Xcodefy's own parser keeps them in the value tree, so a document can be inspected
  without losing anything. Comments are still absent from a re-encoded project, because the schema
  types do not emit any.
- **Compactness validation accumulates.** The reference's density validator assigns rather than
  combines the result of a comment sibling, so a well-formed comment after a nested line comment can
  leave a compact request in place that the printer then refuses. Xcodefy combines the results, so a
  nested line comment always erases an ancestor's compact request.
- **`TextEncoding` carries an integer.** The reference wraps Foundation's `String.Encoding`. Xcodefy
  wraps its raw integer and maps the known values onto `StringEncoding`, which keeps the reference's
  behaviour of persisting an unknown encoding as a number without depending on Foundation.
- **Two degenerate enum cases are dropped.** `XCJSON.ContentShape.comment` is unreachable here
  because a comment is already a distinct entry type rather than a shape of a value, and
  `XCJSON.PrintingDensity.sprawling` is never read: a node is compact when it is marked and
  multi-line otherwise, in the reference as well. `Value.is_container` replaces the two-case shape.
- **Reading always raises `DecodeError`.** Swift throws `NSError` everywhere. Xcodefy separates
  reading, writing and rule violations, so the read path normalises any failure onto `DecodeError`
  to keep a single type to catch.
- **Performance and sample-data tests are not ported.** They benchmark the reference's Objective-C
  fast path and read projects from a directory supplied through an environment variable.
