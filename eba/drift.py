```
python
# drift.py
# Multi-level drift detection and bias adaptation for EBA

import statistics
from collections import deque
from typing import List

from .utils import z_score, safe_mean
from .config import EBACoreConfig

class DriftMonitor:
    """
    Monitors multiple levels of drift in EBA execution.
    Tracks perceptual error outliers, goal drift streaks, and numeric feasibility confidence.
    Supports dynamic bias adjustment and severity checks for resets.
    """

    def __init__(self, config: EBACoreConfig = None):
        """
        Initialize drift monitor with configurable thresholds.

        Args:
            config: Optional EBACoreConfig for custom thresholds. Uses defaults if None.
        """
        self.config = config or EBACoreConfig()

        self.error_history: List[float] = []
        self.recent_drifts = deque(maxlen=20)
        self.drift_streak: int = 0

        self.feasibility_history = deque(maxlen=50)
        self.numeric_bias: float = 1.0

    def record_error(self, error: float) -> bool:
        """
        Record a new perceptual error and check for z-score outlier.

        Returns True if z-score indicates significant drift.
        """
        self.error_history.append(error)

        if len(self.error_history) < 10:
            return False

        recent = self.error_history[-10:]
        mean = statistics.mean(recent)
        std = statistics.pstdev(recent) or 1e-8
        z = abs(z_score(error, mean, std))

        return z > self.config.error_z_threshold

    def record_feasibility(self, was_numeric: bool, success: bool) -> None:
        """
        Record feasibility result and update numeric bias dynamically.
        """
        self.feasibility_history.append((was_numeric, success))

        numeric = [s for f, s in self.feasibility_history if f]
        if not numeric:
            return

        conf = safe_mean(numeric)
        if conf > self.config.feas_conf_high:
            self.numeric_bias = min(1.3, self.numeric_bias * 1.1)
        elif conf < self.config.feas_conf_low:
            self.numeric_bias = max(0.7, self.numeric_bias * 0.9)

    def register_drift(self) -> None:
        """Record a detected drift and increment streak counter."""
        self.recent_drifts.append(True)
        self.drift_streak += 1

    def clear_streak(self) -> None:
        """Reset the drift streak counter."""
        self.drift_streak = 0

    def severe(self) -> bool:
        """Check if drift situation is severe enough for reset."""
        if len(self.recent_drifts) > 3:
            return True

        numeric = [s for f, s in self.feasibility_history if f]
        if numeric and safe_mean(numeric) < self.config.low_conf_threshold:
            return True

        return False
```
