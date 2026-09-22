from xcodefy.library.schema.values.file_path_base_kind import FilePathBaseKind


def test_every_file_path_base_is_represented():
    assert [member.value for member in FilePathBaseKind] == ["absolute", "group", "PROJECT", "DEVELOPER", "PRODUCTS", "SDK", "source-root"]
