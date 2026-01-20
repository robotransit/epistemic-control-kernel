import json
import logging
from typing import Tuple, Callable, Optional

logger = logging.getLogger("eba-core")


def critic_evaluate(
    task_text: str,
    prediction: str,
    result: str,
    objective: str,
    llm_call: Callable[[str], str],
    enable_cross_validation: bool = True,
    verifier_callback: Optional[Callable[[str, str], bool]] = None,
) -> Tuple[bool, str, float]:
    """
    Evaluate task result using critic prompt with consensus and optional verification.

    Args:
        task_text: The task description.
        prediction: Predicted outcome.
        result: Actual execution outcome.
        objective: Overall goal.
        llm_call: Callable that takes prompt and returns LLM response string.
        enable_cross_validation: If True, use dual critic calls for consensus (default True).
        verifier_callback: Optional callback for external verification (e.g. tool result check).

    Returns:
        Tuple[bool, str, float]: (final_success, feedback, error_score)
        - error_score is float 0.0-1.0 (0.0 = perfect alignment, 1.0 = failure)
    """
    prompt = f"""
Evaluate the result against the task and objective.

Task: {task_text}
Prediction: {prediction}
Result: {result}
Objective: {objective}

Return ONLY valid JSON:
{{
  "success": true/false,
  "feedback": "brief explanation"
}}

Respond with true if the result meaningfully advances the objective.
"""

    # First critic call
    response1 = llm_call(prompt)
    success1, feedback1 = _parse_critic_response(response1)

    if not enable_cross_validation:
        error = 1.0 if not success1 else 0.0  # Binary for now - TODO: upgrade to graded/semantic score
        return success1, feedback1, error

    # Second critic call for consensus
    response2 = llm_call(prompt)
    success2, feedback2 = _parse_critic_response(response2)

    final_success = success1 and success2  # Strict AND
    final_feedback = f"{feedback1} | Consensus: {success2}"

    if success1 != success2:
        logger.warning("Critic disagreement detected - potential instability")

    # Optional external verification hook
    if verifier_callback is not None:
        if not verifier_callback(task_text, result):
            final_success = False
            final_feedback += " | External verification failed"

    # Error score: binary for now, but typed float for future graded evolution
    error = 1.0 if not final_success else 0.0  # TODO: upgrade to semantic/graded score (0.0-1.0)

    return final_success, final_feedback, error


def _parse_critic_response(response: str) -> Tuple[bool, str]:
    """Parse critic JSON response. Pessimistic fallback on failure."""
    try:
        data = json.loads(response.strip())
        return bool(data.get("success", False)), str(data.get("feedback", "No feedback"))
    except (json.JSONDecodeError, TypeError):
        logger.warning("Critic JSON parse failed - defaulting to failure (pessimistic)")
        return False, "Parse failed - treated as non-success"

