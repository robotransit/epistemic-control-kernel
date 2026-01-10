```
python
from dataclasses import dataclass

@dataclass(frozen=True)
class EBACoreConfig:
    """
    Central configuration for EBA (Enhanced BabyAGI).

    All thresholds, limits and tuning parameters are defined here with defaults.
    Use EBACoreConfig() to instantiate with defaults, or override values as needed.
    """

    # Execution limits
    max_iterations: int = 100
    max_queue_size: int = 50

    # Drift detection thresholds
    semantic_drift_threshold: float = 0.7
    error_z_threshold: float = 3.0
    max_drift_streak: int = 3

    # Guard interval (check every N cycles)
    guard_interval: int = 5

    # Self-tuning confidence thresholds
    feas_conf_high: float = 0.8
    feas_conf_low: float = 0.5
    low_conf_threshold: float = 0.4

    # Task similarity proactive filter
    task_similarity_threshold: float = 0.75
```
