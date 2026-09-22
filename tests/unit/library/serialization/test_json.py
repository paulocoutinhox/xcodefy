import pytest

from xcodefy.errors.decode_error import DecodeError
from xcodefy.library.serialization.encoding_options import EncodingOptions
from xcodefy.library.serialization.json import JSON
from xcodefy.library.serialization.values.value import Value


def test_parse_returns_the_value_tree():
    assert isinstance(JSON.parse("{}"), Value)


def test_loads_returns_plain_python():
    assert JSON.loads('{ "a": [1] }') == {"a": [1]}


def test_dumps_accepts_both_python_and_a_value_tree():
    assert JSON.dumps({"a": 1}) == '{\n  "a": 1,\n}\n'
    assert JSON.dumps(Value.integer(1)) == "1\n"


def test_dumps_honours_the_encoding_options():
    assert JSON.dumps(1, EncodingOptions(add_trailing_newline=False)) == "1"


def test_encode_runs_a_value_through_the_coder():
    assert JSON.encode([1, 2]) == "[\n  1,\n  2,\n]\n"


def test_load_and_dump_round_trip_through_a_file(tmp_path):
    path = tmp_path / "value.json"
    JSON.dump({"a": 1}, path)
    assert JSON.load(path) == {"a": 1}


def test_malformed_text_is_rejected():
    with pytest.raises(DecodeError):
        JSON.loads("{")
