```
python
import logging
from typing import Callable

from .queue import TaskQueue
from .memory import WorldModel
from .drift import DriftMonitor
from .utils import generate_id, is_numeric_feasible
from .config import EBACoreConfig
from .prompts import (
    format_prompt,
    INITIAL_TASK_PROMPT_TEMPLATE,
    GOAL_ACHIEVED_PROMPT,
)
from .critic import critic_evaluate
from .prediction import generate_prediction
from .task_generation import generate_subtasks
from .execution import execute_task

logger = logging.getLogger("eba-core")


class EBACoreAgent:
    """
    Framework-agnostic core of Enhanced BabyAGI (EBA).
    Orchestrates task queue, memory, drift monitoring, and LLM calls.
    """

    def __init__(
        self,
        objective: str,
        llm_call: Callable[[str], str],  # Single LLM function for all prompts
        config: EBACoreConfig = None,
    ):
        self.objective = objective
        self.llm = llm_call
        self.config = config or EBACoreConfig()

        self.queue = TaskQueue(max_size=self.config.max_queue_size)
        self.memory = WorldModel()
        self.drift = DriftMonitor(config=self.config)

        self.cycles: int = 0

    def seed(self, initial_task: str = None) -> None:
        """Start with an initial task (or generate one if none provided)."""
        if initial_task is None:
            prompt = format_prompt(INITIAL_TASK_PROMPT_TEMPLATE, objective=self.objective)
            initial_task = self.llm(prompt).strip()

        task = {"id": generate_id(), "text": initial_task}
        self.queue.push(task)
        logger.info(f"Agent seeded with initial task: {initial_task}")

    def step(self) -> bool:
        """Execute one full cycle of the agent loop."""
        task = self.queue.pop()
        if not task:
            logger.info("Task queue empty — nothing to do this cycle")
            return False

        task_id = task["id"]
        task_text = task["text"]

        # 1. Predict expected outcome
        prediction = generate_prediction(
            task_text=task_text,
            objective=self.objective,
            llm_call=self.llm,
        )

        # 2. Execute the task using the execution seam
        outcome = execute_task(
            task_text=task_text,
            llm_call=self.llm,
        )

        # 3. Critic evaluation
        success, feedback, error = critic_evaluate(
            task_text=task_text,
            prediction=prediction,
            result=outcome,
            objective=self.objective,
            llm_call=self.llm,
        )

        # Record everything
        self.memory.record(task_id, task_text, prediction, outcome, success, feedback)

        # 4. Drift checks
        perceptual_drift = self.drift.record_error(error)

        # Real numeric feasibility check
        was_numeric = is_numeric_feasible(prediction, outcome)
        self.drift.record_feasibility(was_numeric, success)

        if perceptual_drift:
            logger.warning(f"Perceptual drift detected on task {task_id}")
            self.drift.register_drift()
        else:
            self.drift.clear_streak()

        if self.drift.drift_streak > self.config.max_drift_streak:
            logger.critical("Repeated drift streaks detected — halting agent")
            return False

        # 5. Check if goal achieved
        goal_prompt = format_prompt(GOAL_ACHIEVED_PROMPT, objective=self.objective, result=outcome)
        goal_response = self.llm(goal_prompt).strip()
        if "YES" in goal_response.upper():
            logger.info("Goal achieved — stopping early")
            return False

        # 6. Generate subtasks with safe parsing
        # TODO: Move max_subtasks to config (e.g. config.max_subtasks_per_step)
        subtasks = generate_subtasks(
            current_task=task_text,
            objective=self.objective,
            llm_call=self.llm,
            max_subtasks=5,
        )

        logger.info(f"Generated {len(subtasks)} subtasks")

        for sub in subtasks:
            self.queue.push({"id": generate_id(), "text": sub})

        self.cycles += 1

        # 7. Periodic guard check
        if self.cycles % self.config.guard_interval == 0:
            if self.drift.severe():
                logger.error("Severe instability detected — performing partial reset")
                self.drift = DriftMonitor(config=self.config)

        return True

    def run(self) -> None:
        """Run the agent until halt condition or max iterations reached."""
        logger.info(f"Starting EBA run with objective: {self.objective}")
        while self.cycles < self.config.max_iterations:
            if not self.step():
                break
        logger.info(f"EBA run completed after {self.cycles} cycles")
```
