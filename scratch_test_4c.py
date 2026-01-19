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

# Patch generate_subtasks at the agent call site
original_generate_subtasks = eba.agent.generate_subtasks

def assert_generate_not_called(*args, **kwargs):
    raise AssertionError(
        "generate_subtasks called despite DEFERRED in ENFORCED mode — policy bypassed!"
    )

eba.agent.generate_subtasks = assert_generate_not_called

# Patch execute_task at the agent call site
original_execute_task = eba.agent.execute_task

def assert_execute_not_called(*args, **kwargs):
    raise AssertionError(
        "execute_task called despite DEFERRED in ENFORCED mode — policy bypassed!"
    )

eba.agent.execute_task = assert_execute_not_called

try:
    agent.step()
except AssertionError as e:
    print("FAIL:", str(e))
    raise
finally:
    # Restore originals
    eba.agent.generate_subtasks = original_generate_subtasks
    eba.agent.execute_task = original_execute_task

queue_after = len(agent.queue)
print("Queue after:", queue_after)

assert queue_after <= queue_before, (
    "Queue grew despite DEFERRED in ENFORCED mode — policy bypassed!"
)

print("PASS: No execution and no subtask generation — deferral enforced correctly.")

