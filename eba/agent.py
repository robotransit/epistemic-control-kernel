import logging
from typing import Callable

from dataclasses import replace

from .queue import TaskQueue
from .memory import WorldModel
from .drift import DriftMonitor
from .utils import generate_id, is_numeric_feasible, get_recommended_breadth
from .config import EBACoreConfig, PolicyMode
from .prompts import (
    format_prompt,
    INITIAL_TASK_PROMPT_TEMPLATE,
    GOAL_ACHIEVED_PROMPT,
)
from .critic import critic_evaluate
from .prediction import generate_prediction
from .task_generation import generate_subtasks
from .execution import execute_task
from .task import TaskState

logger = logging.getLogger("eba-core")


# Policy ordering for safe, irreversible upgrades
_POLICY_ORDER = {
    PolicyMode.NORMAL: 0,
    PolicyMode.GUIDED: 1,
    PolicyMode.ENFORCED: 2,
    PolicyMode.HALT: 3,
}


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

        # Current active policy mode (derived from config)
        self.current_policy_mode: PolicyMode = self.config.policy_mode

        # Current confidence (placeholder for Commit 4b — future: rolling signal)
        self.current_confidence: float = 0.5

        self.queue = TaskQueue(max_size=self.config.max_queue_size)
        self.memory = WorldModel()
        self.drift = DriftMonitor(config=self.config)

        self.cycles: int = 0

    def _record_task_created(self, task_id: str, task_text: str) -> None:
        """Helper to record CREATED state when task is enqueued."""
        self.memory.record(
            task_id=task_id,
            task_text=task_text,
            prediction="",
            outcome="",
            success=False,
            feedback="",
            state=TaskState.CREATED
        )

    def seed(self, initial_task: str = None) -> None:
        """Start with an initial task (or generate one if none provided)."""
        if initial_task is None:
            prompt = format_prompt(INITIAL_TASK_PROMPT_TEMPLATE, objective=self.objective)
            initial_task = self.llm(prompt).strip()

        task_id = generate_id()
        task = {"id": task_id, "text": initial_task}
        self.queue.push(task)

        # Record CREATED state
        self._record_task_created(task_id, initial_task)
        logger.info(f"Agent seeded with initial task: {initial_task}")

    def step(self) -> bool:
        """Execute one full cycle of the agent loop."""
        # Early exit on HALT policy (irreversible escalation)
        recommended_mode = self.drift.get_policy_mode()
        if _POLICY_ORDER[recommended_mode] > _POLICY_ORDER[self.current_policy_mode]:
            self.current_policy_mode = recommended_mode
            self.config = replace(self.config, policy_mode=recommended_mode)
            logger.info(f"Policy upgrade: {self.current_policy_mode.name}")

        if self.current_policy_mode == PolicyMode.HALT:
            logger.critical("Policy mode: HALT - stopping agent")
            return False

        task = self.queue.pop()
        if not task:
            logger.info("Task queue empty — nothing to do this cycle")
            return False

        task_id = task["id"]
        task_text = task["text"]

        # Record PREDICTED state
        self.memory.record(
            task_id=task_id,
            task_text=task_text,
            prediction="",
            outcome="",
            success=False,
            feedback="",
            state=TaskState.PREDICTED
        )

        # 1. Predict expected outcome
        prediction = generate_prediction(
            task_text=task_text,
            objective=self.objective,
            llm_call=self.llm,
            memory=self.memory,
            config=self.config,
        )

        # 2. Execute the task using the execution seam (Phase 3: gate execution on DEFERRED in ENFORCED mode)
        recommended_breadth = get_recommended_breadth(
            confidence=self.current_confidence,  # Pre-computed (placeholder for future rolling)
            policy_mode=self.current_policy_mode
        )

        if self.current_policy_mode == PolicyMode.ENFORCED and recommended_breadth == "DEFERRED":
            logger.critical(
                f"ENFORCED mode: DEFERRED recommended — skipping task execution "
                f"(confidence={self.current_confidence:.2f}, mode={self.current_policy_mode.name})"
            )
            # Skip execution, do not mutate world state
            # Cycle continues (return True later)
            outcome = ""  # No real outcome — placeholder
        else:
            outcome = execute_task(task_text, self.llm)

        # Record EXECUTED state (even if skipped)
        self.memory.record(
            task_id=task_id,
            task_text=task_text,
            prediction=prediction,
            outcome=outcome,
            success=False,  # Updated below after critic
            feedback="",
            state=TaskState.EXECUTED
        )

        # 3. Critic evaluation
        success, feedback, error = critic_evaluate(
            task_text=task_text,
            prediction=prediction,
            result=outcome,
            objective=self.objective,
            llm_call=self.llm,
        )

        # Final state after critic
        if success:
            final_state = TaskState.SUCCEEDED
        elif feedback:  # non-empty feedback currently treated as critic rejection
            final_state = TaskState.REJECTED_BY_CRITIC
        else:
            final_state = TaskState.FAILED

        # Record final outcome
        self.memory.record(
            task_id=task_id,
            task_text=task_text,
            prediction=prediction,
            outcome=outcome,
            success=success,
            feedback=feedback,
            state=final_state
        )

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

        # TODO: record TaskState.DEFERRED when policy halts execution

        # 5. Check if goal achieved
        goal_prompt = format_prompt(GOAL_ACHIEVED_PROMPT, objective=self.objective, result=outcome)
        goal_response = self.llm(goal_prompt).strip()
        if "YES" in goal_response.upper():
            logger.info("Goal achieved — stopping early")
            return False

        # 6. Generate subtasks with safe parsing
        subtasks = generate_subtasks(
            current_task=task_text,
            objective=self.objective,
            llm_call=self.llm,
            max_subtasks=5,
        )

        logger.info(f"Generated {len(subtasks)} subtasks")

        for sub in subtasks:
            sub_id = generate_id()
            self.queue.push({"id": sub_id, "text": sub})
            self._record_task_created(sub_id, sub)  # Record CREATED for new subtasks

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

