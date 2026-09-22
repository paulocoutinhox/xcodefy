from xcodefy.library.schema.values.legacy_provisioning_style import LegacyProvisioningStyle


def test_both_provisioning_styles_are_represented():
    assert [member.value for member in LegacyProvisioningStyle] == ["automatic", "manual"]
