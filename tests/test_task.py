import pytest

from eck.task import TaskState


def test_taskstate_values_are_stable():
    assert TaskState.CREATED.value == "created"
    assert TaskState.PREDICTED.value == "predicted"
    assert TaskState.EXECUTED.value == "executed"
    assert TaskState.SUCCEEDED.value == "succeeded"
    assert TaskState.FAILED.value == "failed"
    assert TaskState.REJECTED_BY_CRITIC.value == "rejected_by_critic"
    assert TaskState.DEFERRED.value == "deferred"


def test_taskstate_values_are_unique():
    """TaskState enum values must be unique (safe for serialization/logging)."""
    values = [s.value for s in TaskState]
    assert len(values) == len(set(values))


def test_taskstate_invalid_value_raises():
    """Invalid state value raises ValueError on construction."""
    with pytest.raises(ValueError):
        TaskState("invalid_state")
