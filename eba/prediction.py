```
python
from typing import Callable

from .prompts import format_prompt, PREDICTION_PROMPT_TEMPLATE

def generate_prediction(
    task_text: str,
    objective: str,
    llm_call: Callable[[str], str],
    max_length: int = 200,
) -> str:
    """
    Generate a concise prediction of the expected task outcome.

    This function is pure: it only formats the prompt and calls the LLM.
    No side effects, no logging, no state changes.

    Args:
        task_text: The task description.
        objective: The overall goal.
        llm_call: Callable that takes a prompt and returns the LLM response.
        max_length: Optional max characters for the prediction (truncates if exceeded).

    Returns:
        Cleaned prediction string (normalized whitespace, protected against empty output, truncated if needed).
    """
    prompt = format_prompt(
        PREDICTION_PROMPT_TEMPLATE,
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
```
