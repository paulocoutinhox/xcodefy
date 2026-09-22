from xcodefy.library.schema.values.product_type_id import ProductTypeID


def test_an_apple_product_type_reports_its_abbreviation():
    assert ProductTypeID("com.apple.product-type.application").abbreviated_representation == "application"


def test_a_foreign_product_type_has_no_abbreviation():
    assert ProductTypeID("unusual.prefix").abbreviated_representation is None


def test_an_abbreviation_expands_to_the_full_identifier():
    assert ProductTypeID.from_abbreviated("app") == ProductTypeID("com.apple.product-type.app")
    assert ProductTypeID.from_abbreviated("app").abbreviated_representation == "app"
