import pytest

from eck.task_generation import generate_subtasks


def test_generate_subtasks_parses_valid_json_array():
    def llm(prompt: str) -> str:
        return '["a", "b", "c"]'

    out = generate_subtasks("done", "obj", llm)
    assert out == ["a", "b", "c"]


def test_generate_subtasks_malformed_json_returns_empty_list():
    def llm(prompt: str) -> str:
        return "not json"

    out = generate_subtasks("done", "obj", llm)
    assert out == []


def test_generate_subtasks_strips_and_normalizes_whitespace_and_drops_empty():
    def llm(prompt: str) -> str:
        return '["  one  ", "  two\\n  words  ", "   ", ""]'

    out = generate_subtasks("done", "obj", llm)
    assert out == ["one", "two words"]


def test_generate_subtasks_truncates_to_max_subtasks():
    def llm(prompt: str) -> str:
        return '["a", "b", "c", "d", "e", "f"]'

    out = generate_subtasks("done", "obj", llm, max_subtasks=5)
    assert out == ["a", "b", "c", "d", "e"]


def test_generate_subtasks_includes_objective_and_current_task_in_prompt():
    seen = {"prompt": None}

    def llm(prompt: str) -> str:
        seen["prompt"] = prompt
        return "[]"

    _ = generate_subtasks("current task", "the objective", llm)
    assert seen["prompt"] is not None
    assert "the objective" in seen["prompt"]
    assert "current task" in seen["prompt"]
