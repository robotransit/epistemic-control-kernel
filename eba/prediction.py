```
python
from typing import Callable, List, Dict, Any

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

    # Retrieve similar past tasks
    similar = memory.retrieve_similar(
        task_text=task_text,
        threshold=config.memory_similarity_threshold,
        limit=config.memory_retrieval_limit,
        prefer_failures=config.prefer_negative_memory,
    )

    if not similar:
        return ""

    # Build concise context summary
    context_lines = ["Relevant past outcomes:"]
    for entry in similar:
        task = entry.get("task", "")[:100]
        state = entry.get("state", "unknown")
        outcome = entry.get("outcome", "(no outcome)")[:100]
        success = entry.get("success", False)
        feedback = entry.get("feedback", "(no feedback)")[:100]
        if len(feedback) == 100:
            feedback += "..."
        line = f"- Task: {task}... | State: {state} | Outcome: {outcome}... | Success: {success} | Feedback: {feedback}"
        context_lines.append(line)

    return "\n".join(context_lines)
```
