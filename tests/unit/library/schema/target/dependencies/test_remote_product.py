from tests.support.instances import Instances
from tests.support.round_trip import RoundTrip
from xcodefy.library.schema.target.dependencies.remote_product import RemoteProduct
from xcodefy.library.schema.values.group_tree_reference import GroupTreeReference
from xcodefy.library.schema.values.object_id import ObjectID

PROJECT = GroupTreeReference.of_child_names(["Other.xcodeproj"])


def test_a_single_component_path_is_written_as_a_name():
    product = RemoteProduct(PROJECT, "T", ObjectID("P1"), "My.framework")
    assert product.path_is_name is True
    assert '"name": "My.framework"' in RoundTrip.text(product)
    RoundTrip.expect_equal(product, RemoteProduct)


def test_a_multi_component_path_is_written_as_a_path():
    product = RemoteProduct(PROJECT, "T", ObjectID("P1"), "build/My.framework")
    assert product.path_is_name is False
    assert '"path": "build/My.framework"' in RoundTrip.text(product)
    RoundTrip.expect_equal(product, RemoteProduct)


def test_the_target_membership_is_always_written():
    product = RemoteProduct(PROJECT, "T", ObjectID("P1"), "My.framework")
    assert '"target-membership": [\n  ],' in RoundTrip.text(product)


def test_the_suggested_encoding_order_covers_every_identifying_field():
    product = Instances.populated_remote_product()
    assert product.suggested_encoding_order.content == ("MyFramework.framework", "MyFramework", "0123456789ABCDEF", "sourcecode.swift")


def test_a_product_without_a_file_type_still_sorts():
    product = RemoteProduct(PROJECT, "T", ObjectID("P1"), "My.framework")
    assert product.suggested_encoding_order.content[3] == ""


def test_a_populated_product_round_trips():
    RoundTrip.expect_equal(Instances.populated_remote_product(), RemoteProduct)
