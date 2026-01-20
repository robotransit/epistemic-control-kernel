# NOTE:
# memory_context is opaque, human-readable text.
# Prediction must not interpret, parse, or branch on its contents.
# All semantic interpretation belongs to policy layers only.

from typing import Callable

from .prompts import format_prompt, PREDICTION_PROMPT_TEMPLATE
from .memory import WorldModel
from .config import EBACoreConfig

def build_prediction_context(
    task_text: str,
    objective: str,
    memory: WorldModel,
    config: EBACoreConfig,
) -> str:
    """
    Build optional context from relevant past task outcomes for the prediction prompt.

    This is read-only: retrieves past tasks but does not modify memory or state.
    Disabled by default via config.enable_memory_retrieval.

    Returns empty string when disabled or no relevant outcomes found.
    """
    if not config.enable_memory_retrieval:
        return ""

    similar = memory.retrieve_similar(
        task_text=task_text,
        threshold=config.memory_similarity_threshold,
        limit=config.memory_retrieval_limit,
        prefer_failures=config.prefer_negative_memory,
    )

    if not similar:
        return ""

    context_lines = ["Relevant past outcomes:"]
    for entry in similar:
        task = entry.get("task", "")[:100]
        task_str = task if len(task) < 100 else f"{task}..."
        state = entry.get("state", "unknown")
        outcome = entry.get("outcome", "(no outcome)")[:100]
        outcome_str = outcome if len(outcome) < 100 else f"{outcome}..."
        success = entry.get("success", False)
        feedback = entry.get("feedback", "(no feedback)")[:100]
        if len(feedback) == 100:
            feedback += "..."
        line = f"- Task: {task_str} | State: {state} | Outcome: {outcome_str} | Success: {success} | Feedback: {feedback}"
        context_lines.append(line)

    return "\n".join(context_lines)


def generate_prediction(
    task_text: str,
    objective: str,
    llm_call: Callable[[str], str],
    memory: WorldModel,
    config: EBACoreConfig,
    max_length: int = 200,
) -> str:
    """
    Generate a concise prediction of the expected task outcome.

    This function is pure: it formats the prompt, calls the LLM, and safely parses the result.
    No side effects, no logging, no state changes.

    Memory context is opaque text. Do not interpret here.
    """
    # Build memory context (empty if disabled or no relevant outcomes)
    memory_context = build_prediction_context(task_text, objective, memory, config)

    prompt = format_prompt(
        PREDICTION_PROMPT_TEMPLATE,
        memory_context=memory_context,
        objective=objective,
        task_text=task_text
    )

    raw_prediction = llm_call(prompt).strip()

    # Normalize internal whitespace (collapse multiples, remove newlines/tabs)
    raw_prediction = ' '.join(raw_prediction.split())

    # Protect against empty/whitespace-only output
    if not raw_prediction:
        raw_prediction = "(no prediction generated)"

    # Optional length constraint
    if len(raw_prediction) > max_length:
        raw_prediction = raw_prediction[:max_length].rstrip(" .,!?") + "..."

    return raw_prediction
