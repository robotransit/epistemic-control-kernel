import pytest

from eck.agent import ECKAgent
from eck.config import ECKConfig, PolicyMode


def dummy_llm(prompt: str) -> str:
    """Deterministic stub for agent loop tests."""
    # Ensure goal check never returns YES
    return "NO"


@pytest.fixture
def agent():
    config = ECKConfig(policy_mode=PolicyMode.ENFORCED)
    return ECKAgent(
        objective="Test agent loop",
        llm_call=dummy_llm,
        config=config,
    )


def test_enforced_deferred_no_execution_no_subtasks(agent, monkeypatch):
    """ENFORCED + DEFERRED → no execution, no subtask generation."""
    import eck.agent as agent_mod

    agent.seed("Seed task")

    # Lock drift recommendation to ENFORCED (prevents upgrade before should_execute)
    monkeypatch.setattr(agent.drift, "get_policy_mode", lambda: PolicyMode.ENFORCED)

    # Force DEFERRED breadth at agent import point
    monkeypatch.setattr(agent_mod, "get_recommended_breadth", lambda *a, **k: "DEFERRED")

    # Assert should_execute received "DEFERRED" and correct policy mode, then return False
    received_breadth = []

    def assert_deferred_and_false(policy_mode, breadth):
        received_breadth.append(breadth)
        assert breadth == "DEFERRED", "should_execute did not receive DEFERRED"
        assert policy_mode == PolicyMode.ENFORCED, "should_execute did not receive ENFORCED policy mode"
        return False
    monkeypatch.setattr(agent_mod, "should_execute", assert_deferred_and_false)

    # Raise if execute_task or generate_subtasks called
    def raise_if_called(*args, **kwargs):
        raise AssertionError("Execution or subtask generation should not be called")

    monkeypatch.setattr(agent_mod, "execute_task", raise_if_called)
    monkeypatch.setattr(agent_mod, "generate_subtasks", raise_if_called)

    # Run one step — should pop the task, then skip execution + subtask gen
    assert agent.step() is True

    # Confirm should_execute was called with DEFERRED (called twice in step: exec + subtasks)
    assert received_breadth == ["DEFERRED", "DEFERRED"], "should_execute was not called with DEFERRED twice"

    # No new subtasks enqueued
    assert len(agent.queue) == 0


def test_halt_at_start_stops_step(monkeypatch):
    """HALT mode → step() returns False, no execution/generation."""
    import eck.agent as agent_mod

    halt_agent = ECKAgent(
        objective="Test HALT",
        llm_call=dummy_llm,
        config=ECKConfig(policy_mode=PolicyMode.HALT),
    )

    def raise_if_called(*args, **kwargs):
        raise AssertionError("No actions should be called in HALT")

    monkeypatch.setattr(agent_mod, "execute_task", raise_if_called)
    monkeypatch.setattr(agent_mod, "generate_subtasks", raise_if_called)
    monkeypatch.setattr(agent_mod, "generate_prediction", raise_if_called)
    monkeypatch.setattr(agent_mod, "critic_evaluate", raise_if_called)

    assert halt_agent.step() is False


def test_queue_empty_step_returns_false(agent):
    """Empty queue → step() returns False (no loop iterations)."""
    # Safe clear via TaskQueue API (confirmed in queue.py)
    agent.queue.clear()
    assert len(agent.queue) == 0
    assert agent.step() is False


def test_policy_mode_upgrades_are_irreversible(monkeypatch):
    """
    Irreversible upgrade rule:
    if drift recommends a higher mode, agent upgrades;
    if drift later recommends a lower mode, agent must NOT downgrade.
    """
    import eck.agent as agent_mod

    agent = ECKAgent(
        objective="Test irreversible upgrades",
        llm_call=dummy_llm,
        config=ECKConfig(policy_mode=PolicyMode.NORMAL),
    )

    # Make the step cheap/deterministic (no execution/subtasks)
    monkeypatch.setattr(agent_mod, "generate_prediction", lambda *a, **k: "pred")
    monkeypatch.setattr(agent_mod, "get_recommended_breadth", lambda *a, **k: "DEFERRED")
    monkeypatch.setattr(agent_mod, "should_execute", lambda *a, **k: False)
    monkeypatch.setattr(agent_mod, "critic_evaluate", lambda *a, **k: (True, "", 0.0))

    monkeypatch.setattr(agent.drift, "record_error", lambda *a, **k: False)
    monkeypatch.setattr(agent.drift, "record_feasibility", lambda *a, **k: None)
    monkeypatch.setattr(agent.drift, "register_drift", lambda *a, **k: None)
    monkeypatch.setattr(agent.drift, "clear_streak", lambda *a, **k: None)

    # Force drift recommendations across steps:
    # NORMAL -> GUIDED -> ENFORCED -> (attempted downgrade) NORMAL
    seq = iter([PolicyMode.GUIDED, PolicyMode.ENFORCED, PolicyMode.NORMAL])
    monkeypatch.setattr(agent.drift, "get_policy_mode", lambda: next(seq))

    assert agent.current_policy_mode == PolicyMode.NORMAL

    agent.seed("t1")
    assert agent.step() is True
    assert agent.current_policy_mode == PolicyMode.GUIDED

    agent.seed("t2")
    assert agent.step() is True
    assert agent.current_policy_mode == PolicyMode.ENFORCED

    agent.seed("t3")
    assert agent.step() is True
    # Must NOT downgrade back to NORMAL
    assert agent.current_policy_mode == PolicyMode.ENFORCED
