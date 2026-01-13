```
python
from dataclasses import dataclass
from enum import Enum
from typing import Mapping
from types import MappingProxyType


class PolicyMode(Enum):
    """
    NORMAL: full agent operation (default)
    CONSERVATIVE: reduced risk profile (lower breadth, stricter critic, pessimistic prediction)
    HALT: no further task generation or execution (irreversible until manual reset)
    """
    NORMAL = "normal"
    CONSERVATIVE = "conservative"
    HALT = "halt"


@dataclass(frozen=True)
class EBACoreConfig:
    """
    Central configuration for EBA (Enhanced BabyAGI).
    All thresholds, limits, and policy overrides are defined here.

    Transition thresholds (public) define when drift signals trigger mode changes.
    Effect parameters (_conservative_*) are private and resolved via effective_policy().
    """

    # Existing public fields (abbreviated)
    max_iterations: int = 100
    max_queue_size: int = 50
    semantic_drift_threshold: float = 0.7
    error_z_threshold: float = 3.0
    max_drift_streak: int = 3
    guard_interval: int = 5
    feas_conf_high: float = 0.8
    feas_conf_low: float = 0.5
    low_conf_threshold: float = 0.4
    task_similarity_threshold: float = 0.75

    # Policy mode (current active mode)
    policy_mode: PolicyMode = PolicyMode.NORMAL

    # Public transition thresholds (drift → policy)
    conservative_drift_streak: int = 2
    conservative_error_z: float = 2.0
    halt_drift_streak: int = 4
    halt_error_z: float = 4.0

    # Private: policy effect parameters (resolved via effective_policy())
    _conservative_max_subtasks: int = 2
    _conservative_critic_strictness: float = 0.9
    _conservative_prediction_bias_delta: float = -0.2

    def effective_policy(self) -> Mapping[str, object]:
        """
        Resolve effective parameters based on current policy mode.

        Returns an immutable mapping view with the following possible keys (all optional):

        - max_subtasks: int — maximum subtasks to generate per step
        - critic_strictness: float — higher values = stricter success threshold
        - prediction_bias_delta: float — signed bias adjustment to predictions
        - halt: bool — if True, agent should stop immediately

        This is a read-only view — do not attempt to modify it.
        """
        if self.policy_mode == PolicyMode.NORMAL:
            return MappingProxyType({})

        if self.policy_mode == PolicyMode.CONSERVATIVE:
            return MappingProxyType({
                "max_subtasks": self._conservative_max_subtasks,
                "critic_strictness": self._conservative_critic_strictness,
                "prediction_bias_delta": self._conservative_prediction_bias_delta,
            })

        if self.policy_mode == PolicyMode.HALT:
            return MappingProxyType({"halt": True})

        raise ValueError(f"Unknown policy mode: {self.policy_mode}")
```
