```
python
from typing import Callable, List

from .prompts import format_prompt, SUBTASK_GENERATION_PROMPT
from .utils import safe_parse_json_array

def generate_subtasks(
    current_task: str,
    objective: str,
    llm_call: Callable[[str], str],
    max_subtasks: int = 5,
) -> List[str]:
    """
    Generate up to max_subtasks concise subtasks to advance the current task toward the objective.

    This function is pure: it formats the prompt, calls the LLM, and safely parses the result.
    No side effects, no logging, no state changes.

    Args:
        current_task: The most recently completed task.
        objective: The overall goal.
        llm_call: Callable that takes a prompt and returns the LLM response.
        max_subtasks: Optional cap on number of subtasks returned (default 5).

    Returns:
        List of cleaned subtask strings (empty list if no subtasks needed or parsing fails).
    """
    prompt = format_prompt(
        SUBTASK_GENERATION_PROMPT,
        objective=objective,
        current_task=current_task
    )

    raw_response = llm_call(prompt).strip()

    subtasks = safe_parse_json_array(raw_response)

    # Defensive cleanup: strip whitespace, drop empty/whitespace-only entries
    cleaned_subtasks = [
        ' '.join(sub.strip().split())  # normalize internal whitespace
        for sub in subtasks
        if sub.strip()  # drop empty or whitespace-only
    ]

    # Enforce max_subtasks cap (truncate if over-generated)
    if len(cleaned_subtasks) > max_subtasks:
        cleaned_subtasks = cleaned_subtasks[:max_subtasks]

    return cleaned_subtasks
```
