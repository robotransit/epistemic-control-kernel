import pytest
from types import MappingProxyType

from eck.config import ECKConfig, PolicyMode


def test_effective_policy_normal_returns_empty_mappingproxy():
    config = ECKConfig(policy_mode=PolicyMode.NORMAL)
    effective = config.effective_policy()
    assert isinstance(effective, MappingProxyType)
    assert dict(effective) == {}


def test_effective_policy_guided_returns_expected_keys_and_values():
    config = ECKConfig(policy_mode=PolicyMode.GUIDED)
    effective = config.effective_policy()

    assert isinstance(effective, MappingProxyType)
    assert set(effective.keys()) == {
        "max_subtasks",
        "critic_strictness",
        "prediction_bias_delta",
    }

    assert effective["max_subtasks"] == config._guided_max_subtasks
    assert effective["critic_strictness"] == config._guided_critic_strictness
    assert effective["prediction_bias_delta"] == config._guided_prediction_bias_delta


def test_effective_policy_halt_returns_halt_true():
    config = ECKConfig(policy_mode=PolicyMode.HALT)
    effective = config.effective_policy()

    assert isinstance(effective, MappingProxyType)
    assert dict(effective) == {"halt": True}


def test_effective_policy_is_immutable():
    config = ECKConfig(policy_mode=PolicyMode.GUIDED)
    effective = config.effective_policy()

    with pytest.raises(TypeError):
        effective["new_key"] = "value"
