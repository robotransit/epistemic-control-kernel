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
    values = [s.value for s in TaskState]
    assert len(values) == len(set(values))
