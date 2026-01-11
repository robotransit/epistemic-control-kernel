```
python
# utils.py
# Shared helper functions for EBA (ID generation, statistics, similarity, parsing)

import uuid
import logging
import math
import json
from typing import List, Any

logger = logging.getLogger("eba-core")

def generate_id() -> str:
    """Generate a unique task ID using UUID4."""
    return str(uuid.uuid4())

def safe_mean(values: List[float]) -> float:
    """Compute mean safely, returning 0 if the list is empty."""
    return sum(values) / max(1, len(values))

def z_score(value: float, mean: float, std: float) -> float:
    """Compute z-score, returning 0 if standard deviation is zero."""
    if std == 0:
        return 0.0
    return (value - mean) / std

def cosine_sim(a: List[float], b: List[float]) -> float:
    """
    Compute cosine similarity between two vectors (pure Python).

    Returns 0.0 if either vector has zero magnitude or is empty.
    """
    if not a or not b:
        return 0.0

    dot = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x * x for x in a))
    mag_b = math.sqrt(sum(x * x for x in b))

    if mag_a == 0 or mag_b == 0:
        return 0.0

    return dot / (mag_a * mag_b)

def safe_parse_json_array(response: str) -> List[str]:
    """
    Safely parse a JSON array string from LLM output.

    Returns empty list on any failure, with warning logged.
    """
    try:
        parsed = json.loads(response.strip())
        if isinstance(parsed, list):
            return [str(item) for item in parsed]  # Ensure all are strings
        else:
            raise ValueError("Not a list")
    except (json.JSONDecodeError, ValueError, TypeError) as e:
        logger.warning(f"Subtask JSON parse failed: {e} - no subtasks generated")
        return []

# Note: This is a heuristic compatibility check, not a correctness test.
def is_numeric_feasible(prediction: Any, actual: Any, similarity_threshold: float = 0.8) -> bool:
    """
    Determine if prediction and actual outcome are numeric-feasible.

    Checks:
    - Both are numeric types (int/float)
    - Or both are lists/arrays of same length
    - Or semantic similarity via string conversion (fallback with cosine sim)
    """
    # Direct numeric type match
    if isinstance(prediction, (int, float)) and isinstance(actual, (int, float)):
        return True

    # Array-like match
    if isinstance(prediction, (list, tuple)) and isinstance(actual, (list, tuple)):
        if len(prediction) == len(actual):
            return True

    # Semantic fallback: convert to strings and check length + content similarity
    try:
        pred_str = str(prediction)
        act_str = str(actual)
        if len(pred_str) == 0 or len(act_str) == 0:
            return False

        # Simple heuristic: length difference and basic content overlap
        length_diff = abs(len(pred_str) - len(act_str))
        if length_diff > 50:
            return False

        # Optional: use cosine sim on character vectors if needed
        # For now, return True if lengths are close
        return True
        # TODO: Upgrade to full embedding similarity using sentence-transformers
    except Exception as e:
        logger.debug(f"Numeric feasibility fallback failed: {e}")
        return False
```
