```
python
import logging
from typing import Callable, Dict, List, Optionalfrom .queue import TaskQueue
from .memory import WorldModel
from .drift import DriftMonitor
from .utils import generate_id
from .config import EBACoreConfiglogger = logging.getLogger("eba-core")class EBACoreAgent:
    """
    Framework-agnostic core of Enhanced BabyAGI (EBA).Orchestrates task queue, memory, drift monitoring, and LLM calls.
"""

def __init__(
    self,
    objective: str,
    predict_fn: Callable[[str], str],
    execute_fn: Callable[[str], str],
    critic_fn: Callable[[str, str, str, str], tuple[bool, str, float]],
    task_generator_fn: Callable[[str, str], List[str]],
    config: EBACoreConfig,
):
    """
    Initialize the EBA agent.

    Args:
        objective: The overall goal string.
        predict_fn: Function that generates prediction for a task (str -> str).
        execute_fn: Function that executes a task (str -> str).
        critic_fn: Function that evaluates result (task, pred, outcome, objective -> success, feedback, error).
        task_generator_fn: Function that generates subtasks (current_task, objective -> list[str]).
        config: Configuration object with all thresholds and limits.
    """
    self.objective = objective
    self.predict = predict_fn
    self.execute = execute_fn
    self.critic = critic_fn
    self.task_gen = task_generator_fn
    self.config = config

    self.queue = TaskQueue(max_size=config.max_queue_size)
    self.memory = WorldModel()
    self.drift = DriftMonitor(config=config)  # Pass config for shared thresholds

    self.cycles: int = 0

def seed(self, initial_task: str) -> None:
    """Seed the queue with the very first task."""
    task = {"id": generate_id(), "text": initial_task}
    self.queue.push(task)
    logger.info(f"Seeded initial task: {initial_task}")

def step(self) -> bool:
    """Execute one cycle of the agent loop. Returns False if queue empty or halt triggered."""
    task = self.queue.pop()
    if not task:
        logger.info("Queue empty — nothing to do")
        return False

    task_id = task["id"]
    text = task["text"]

    prediction = self.predict(text)
    outcome = self.execute(text)
    success, feedback, error = self.critic(text, prediction, outcome, self.objective)

    self.memory.record(task_id, text, prediction, outcome, success, feedback)

    # Drift checks
    perceptual_drift = self.drift.record_error(error)
    self.drift.record_feasibility(feasible=True, success=success)  # TODO: real feasible check

    if perceptual_drift:
        logger.warning(f"Perceptual drift detected on task {task_id}")
        self.drift.register_drift()
    else:
        self.drift.clear_streak()

    if self.drift.drift_streak > self.config.max_drift_streak:
        logger.critical("Repeated drift streaks — halting agent")
        return False

    # Generate and push subtasks
    subtasks = self.task_gen(text, self.objective)
    for sub in subtasks:
        self.queue.push({"id": generate_id(), "text": sub})

    self.cycles += 1

    # Periodic guard check
    if self.cycles % self.config.guard_interval == 0:
        if self.drift.severe():
            logger.error("Severe instability detected — performing partial reset")
            self.drift = DriftMonitor(config=self.config)  # Reset drift monitor

    return True

def run(self) -> None:
    """Run the agent until queue empty, halt, or max iterations reached."""
    logger.info(f"Starting EBA run with objective: {self.objective}")
    while self.cycles < self.config.max_iterations:
        if not self.step():
            break
    logger.info(f"EBA run completed after {self.cycles} cycles")
  
```


