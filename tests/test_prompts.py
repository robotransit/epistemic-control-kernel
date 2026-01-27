import pytest

from eck.prompts import (
    format_prompt,
    INITIAL_TASK_PROMPT_TEMPLATE,
    SUBTASK_GENERATION_PROMPT,
    PREDICTION_PROMPT_TEMPLATE,
    GOAL_ACHIEVED_PROMPT,
    CRITIC_EVALUATION_PROMPT,
)


def test_format_prompt_substitutes_placeholders_correctly():
    """format_prompt replaces all {placeholders} and leaves no {} tokens."""
    template = "Hello {name}, your age is {age}."
    result = format_prompt(template, name="Alice", age=30)
    assert result == "Hello Alice, your age is 30."
    assert "{" not in result and "}" not in result


def test_initial_task_prompt_contains_contractual_constraints():
    """INITIAL_TASK_PROMPT_TEMPLATE mentions objective and requests a single task output."""
    text = INITIAL_TASK_PROMPT_TEMPLATE.lower()
    assert "objective" in text
    assert "task" in text
    assert "only" in text  # “task string only”


def test_subtask_generation_prompt_contains_contractual_constraints():
    """SUBTASK_GENERATION_PROMPT includes “Return ONLY a valid JSON array”."""
    assert "Return ONLY a valid JSON array" in SUBTASK_GENERATION_PROMPT


def test_prediction_prompt_contains_contractual_constraints():
    """PREDICTION_PROMPT_TEMPLATE includes “Return ONLY a brief string prediction”."""
    assert "Return ONLY a brief string prediction" in PREDICTION_PROMPT_TEMPLATE


def test_goal_achieved_prompt_contains_contractual_constraints():
    """GOAL_ACHIEVED_PROMPT includes Answer ONLY "YES" or "NO"."""
    assert 'Answer ONLY "YES" or "NO"' in GOAL_ACHIEVED_PROMPT


def test_critic_evaluation_prompt_contains_contractual_constraints():
    """CRITIC_EVALUATION_PROMPT includes Return ONLY valid JSON and the schema."""
    assert "Return ONLY valid JSON" in CRITIC_EVALUATION_PROMPT
    assert '"success": true/false' in CRITIC_EVALUATION_PROMPT
    assert '"feedback": "brief explanation"' in CRITIC_EVALUATION_PROMPT
