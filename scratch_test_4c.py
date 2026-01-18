from eba.agent import EBACoreAgent
from eba.config import EBACoreConfig, PolicyMode

def dummy_llm(prompt: str) -> str:
    return "dummy"

config = EBACoreConfig(
    policy_mode=PolicyMode.ENFORCED,
)

agent = EBACoreAgent(
    objective="Test",
    llm_call=dummy_llm,
    config=config,
)

# Force DEFERRED recommendation
import eba.agent
eba.agent.get_recommended_breadth = lambda **kwargs: "DEFERRED"

agent.seed("Initial task")

queue_before = len(agent.queue)
print("Queue before:", queue_before)

# Patch generate_subtasks on the agent module
original_generate_subtasks = eba.agent.generate_subtasks

def assert_not_called(*args, **kwargs):
    raise AssertionError("generate_subtasks called despite DEFERRED in ENFORCED mode — policy bypassed!")

eba.agent.generate_subtasks = assert_not_called

try:
    agent.step()
except AssertionError as e:
    print("FAIL:", str(e))
    raise
finally:
    # Restore original
    eba.agent.generate_subtasks = original_generate_subtasks

queue_after = len(agent.queue)
print("Queue after:", queue_after)

assert queue_after <= queue_before, "Queue grew despite DEFERRED in ENFORCED mode — policy bypassed!"

print("PASS: No new subtasks generated — deferral enforced correctly.")
