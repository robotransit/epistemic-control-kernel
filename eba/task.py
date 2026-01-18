from enum import Enum

class TaskState(Enum):
    """
    Canonical lifecycle states for a task within EBA.

    States describe observable task progression and outcomes.
    Causes and interpretations are handled elsewhere (critic, drift, policy).
    """
    CREATED = "created"
    PREDICTED = "predicted"
    EXECUTED = "executed"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    REJECTED_BY_CRITIC = "rejected_by_critic"
    DEFERRED = "deferred"
