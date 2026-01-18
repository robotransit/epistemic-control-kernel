import statistics
from collections import deque
from typing import List

from .utils import z_score, safe_mean
from .config import EBACoreConfig, PolicyMode

class DriftMonitor:
    """
    Monitors multiple levels of drift in EBA execution.
    Tracks perceptual error outliers, goal drift streaks, and numeric feasibility confidence.
    Supports dynamic bias adjustment and severity checks for resets.
    """

    def __init__(self, config: EBACoreConfig = None):
        """
        Initialize drift monitor with configurable thresholds.
        """
        self.config = config or EBACoreConfig()

        self.error_history: List[float] = []
        self.last_error_z: float = 0.0  # Track latest z-score for policy decisions
        self.recent_drifts = deque(maxlen=20)
        self.drift_streak: int = 0

        self.feasibility_history = deque(maxlen=50)
        self.numeric_bias: float = 1.0

    def record_error(self, error: float) -> bool:
        """Record a new perceptual error and check for z-score outlier."""
        self.error_history.append(error)

        if len(self.error_history) < 10:
            self.last_error_z = 0.0
            return False

        recent = self.error_history[-10:]
        mean = statistics.mean(recent)
        std = statistics.pstdev(recent) or 1e-8
        z = abs(z_score(error, mean, std))
        self.last_error_z = z  # Update latest z-score

        return z > self.config.error_z_threshold

    def record_feasibility(self, was_numeric: bool, success: bool) -> None:
        """Record feasibility result and update numeric bias dynamically."""
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
        """Return True if conditions warrant immediate HALT."""
        if len(self.recent_drifts) > 3:
            return True

        numeric = [s for f, s in self.feasibility_history if f]
        if numeric and safe_mean(numeric) < self.config.low_conf_threshold:
            return True

        return False

    def get_policy_mode(self) -> PolicyMode:
        """
        Determine recommended policy mode based on current drift signals.

        Uses public transition thresholds from config to decide mode.
        Returns NORMAL by default, CONSERVATIVE on moderate signals, HALT on severe/repeated drift.
        """
        # HALT conditions (highest priority)
        if (
            self.severe()
            or self.drift_streak >= self.config.max_drift_streak
            or self.last_error_z >= self.config.error_z_threshold
        ):
            return PolicyMode.HALT


        return PolicyMode.NORMAL
        
