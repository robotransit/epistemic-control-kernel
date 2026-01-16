```
python
import uuid
import logging
import math
import json
from typing import List, Any, Dict

from .config import PolicyMode, EBACoreConfig

logger = logging.getLogger("eba-core")

# Why this exists before enforcement (Commit 4b)
#
# This resolver translates confidence → breadth defaults but does NOT enforce them.
# It is intentionally introduced before Commit 4c (hard gating) to:
# - Establish observability and auditability first
# - Prevent premature coupling between confidence signals and behavioural control
# - Allow safe testing/logging of recommendations without risking irreversible side effects
# ⚠️ Enforcement must not be added here — see Commit 4c.

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

def score_memory_entry(
    entry: Dict[str, Any],
    current_task: str,
    policy_mode: PolicyMode,
    config: EBACoreConfig,
) -> float:
    """
    Compute a scalar weight for a past task entry's relevance to the current task.

    This is a pure scoring function — no side effects, no memory mutation.

    Scoring factors:
    - Semantic similarity (placeholder cosine sim)
    - Outcome severity (failures weighted higher)
    - Policy mode (CONSERVATIVE/HALT penalize low relevance)

    Returns a float >= 0:
    - 0 = ignore this entry
    - Higher = more influence (for future context weighting)
    """
    # Placeholder similarity (future: replace with cosine_sim on embeddings)
    similarity = 0.0  # Replace with actual sim computation
    # For demo: simple string overlap
    current_words = set(current_task.lower().split())
    past_text = entry.get("task", "")  # Safe default if key missing
    past_words = set(past_text.lower().split())
    union = current_words | past_words
    if not union:
        similarity = 0.0
    else:
        intersection = current_words & past_words
        similarity = len(intersection) / len(union)

    # Outcome severity bonus/penalty
    success = entry.get("success", False)
    severity = 1.0 if success else 2.0  # TODO: move to config (failure_severity_weight)

    # Policy mode multiplier (CONSERVATIVE/HALT penalize low relevance)
    policy_multiplier = 1.0
    if policy_mode == PolicyMode.CONSERVATIVE:
        policy_multiplier = 0.8 if similarity < 0.8 else 1.0  # TODO: use config.memory_similarity_threshold
    elif policy_mode == PolicyMode.HALT:
        policy_multiplier = 0.0  # No memory influence in HALT

    # Final score
    score = similarity * severity * policy_multiplier

    return max(0.0, score)  # Never negative
```
