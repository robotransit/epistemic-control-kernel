import pytest

from eck.utils import safe_parse_json_array


def test_safe_parse_json_array_valid_returns_list_of_strings():
    result = safe_parse_json_array('["a", "b", "c"]')
    assert result == ["a", "b", "c"]


def test_safe_parse_json_array_non_array_returns_empty():
    result = safe_parse_json_array('{"key": "value"}')
    assert result == []


def test_safe_parse_json_array_malformed_returns_empty():
    result = safe_parse_json_array('invalid json')
    assert result == []


def test_safe_parse_json_array_logs_warning_on_failure(caplog):
    with caplog.at_level("WARNING"):
        result = safe_parse_json_array('not json')

    assert result == []
    assert any("Subtask JSON parse failed" in r.message for r in caplog.records)


def test_safe_parse_json_array_coerces_numbers_and_bools_to_strings():
    result = safe_parse_json_array('[1, true, false, 3.14, "hello"]')
    assert result == ["1", "True", "False", "3.14", "hello"]
