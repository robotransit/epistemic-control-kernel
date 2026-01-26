import pytest
from dataclasses import replace

from eck.drift import DriftMonitor
from eck.config import ECKConfig, PolicyMode


@pytest.fixture
def drift_monitor():
    return DriftMonitor(config=ECKConfig())


def test_record_error_outlier_trips_after_history_len_10(drift_monitor):
    """
    record_error() returns False until history >= 10, then True on outlier.
    """
    drift_monitor.config = replace(drift_monitor.config, error_z_threshold=2.0)

    # Build baseline with variance (std > 0)
    for x in [0.40, 0.60] * 5:
        assert drift_monitor.record_error(x) is False

    # Spike should trip outlier detection
    assert drift_monitor.record_error(1.00) is True
    assert drift_monitor.last_error_z >= drift_monitor.config.error_z_threshold


def test_drift_streak_increments_and_clears(drift_monitor):
    assert drift_monitor.drift_streak == 0
    drift_monitor.register_drift()
    assert drift_monitor.drift_streak == 1
    drift_monitor.register_drift()
    assert drift_monitor.drift_streak == 2
    drift_monitor.clear_streak()
    assert drift_monitor.drift_streak == 0


def test_severe_triggers_on_recent_drifts_window(drift_monitor):
    assert drift_monitor.severe() is False
    for _ in range(4):
        drift_monitor.register_drift()
    assert drift_monitor.severe() is True


def test_severe_triggers_on_low_numeric_feasibility_mean(drift_monitor):
    drift_monitor.config = replace(drift_monitor.config, low_conf_threshold=0.9)

    for _ in range(5):
        drift_monitor.record_feasibility(was_numeric=True, success=False)

    assert drift_monitor.severe() is True


def test_get_policy_mode_returns_halt_on_severe(drift_monitor):
    for _ in range(4):
        drift_monitor.register_drift()

    assert drift_monitor.severe() is True
    assert drift_monitor.get_policy_mode() == PolicyMode.HALT


def test_get_policy_mode_returns_halt_when_streak_reaches_max(drift_monitor):
    drift_monitor.config = replace(drift_monitor.config, max_drift_streak=3)
    for _ in range(3):
        drift_monitor.register_drift()
    assert drift_monitor.get_policy_mode() == PolicyMode.HALT


def test_get_policy_mode_returns_normal_otherwise(drift_monitor):
    assert drift_monitor.severe() is False
    assert drift_monitor.get_policy_mode() == PolicyMode.NORMAL
