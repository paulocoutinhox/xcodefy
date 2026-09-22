import pytest

from tests.support.round_trip import RoundTrip
from xcodefy.errors.validation_error import ValidationError
from xcodefy.library.schema.values.language import Language
from xcodefy.library.schema.values.project_localization_info import ProjectLocalizationInfo


def test_the_supported_languages_must_exclude_the_development_language():
    with pytest.raises(ValidationError, match="must not contain the development language"):
        ProjectLocalizationInfo(Language("en"), frozenset({Language("en")}))


def test_all_languages_combines_development_and_supported():
    info = ProjectLocalizationInfo(Language("en"), frozenset({Language("fr")}))
    assert info.all_languages == frozenset({Language("en"), Language("fr")})


def test_an_empty_supported_set_is_omitted_from_the_encoding():
    assert RoundTrip.text(ProjectLocalizationInfo(Language("en"))) == '{\n  "development": "en",\n}\n'


def test_supported_languages_are_encoded_in_order():
    info = ProjectLocalizationInfo(Language("en"), frozenset({Language("pt"), Language("fr")}))
    assert RoundTrip.text(info) == '{\n  "development": "en",\n  "supported": [\n    "fr",\n    "pt",\n  ],\n}\n'
