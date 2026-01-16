```

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
def get_recommended_breadth(
    confidence: float,
    policy_mode: PolicyMode,
) -> str:
    """
    Map confidence to a recommended breadth level (soft guidance only).

    Returns one of: 'FULL', 'MODERATE', 'RESTRICTED', 'DEFERRED'
    Semantics defined in docs/eba-confidence-breadth.md
    """

    # NORMAL mode is never affected by confidence
    if policy_mode == PolicyMode.NORMAL:
        recommended = "FULL"
    elif confidence >= 0.8:
        recommended = "FULL"
    elif confidence >= 0.5:
        recommended = "MODERATE"
    elif confidence >= 0.3:
        recommended = "RESTRICTED"
    else:
        recommended = "DEFERRED"

    logger.info(
        f"Recommended breadth: {recommended} "
        f"(confidence={confidence:.2f}, mode={policy_mode.name})"
    )

    return recommended


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
            return [str(item) for item in parsed]
        else:
            raise ValueError("Not a list")
    except (json.JSONDecodeError, ValueError, TypeError) as e:
        logger.warning(f"Subtask JSON parse failed: {e} - no subtasks generated")
        return []


def is_numeric_feasible(
    prediction: Any,
    actual: Any,
    similarity_threshold: float = 0.8,
) -> bool:
    """
    Determine if prediction and actual outcome are numeric-feasible.

    Checks:
    - Both are numeric types (int/float)
    - Or both are lists/arrays of same length
    - Or semantic similarity via string conversion (fallback)
    """
    # Direct numeric type match
    if isinstance(prediction, (int, float)) and isinstance(actual, (int, float)):
        return True

    # Array-like match
    if isinstance(prediction, (list, tuple)) and isinstance(actual, (list, tuple)):
        if len(prediction) == len(actual):
            return True

    # Semantic fallback
    try:
        pred_str = str(prediction)
        act_str = str(actual)
        if len(pred_str) == 0 or len(act_str) == 0:
            return False

        length_diff = abs(len(pred_str) - len(act_str))
        if length_diff > 50:
            return False

        # For now: accept if lengths are close
        return True
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
    """
    # Placeholder similarity (future: replace with cosine_sim on embeddings)
    current_words = set(current_task.lower().split())
    past_text = entry.get("task", "")
    past_words = set(past_text.lower().split())
    union = current_words | past_words

    if not union:
        similarity = 0.0
    else:
        intersection = current_words & past_words
        similarity = len(intersection) / len(union)

    # Outcome severity weighting
    success = entry.get("success", False)
    severity = 1.0 if success else 2.0  # TODO: move to config

    # Policy mode multiplier
    policy_multiplier = 1.0
    if policy_mode == PolicyMode.CONSERVATIVE:
        policy_multiplier = 0.8 if similarity < 0.8 else 1.0
    elif policy_mode == PolicyMode.HALT:
        policy_multiplier = 0.0

    score = similarity * severity * policy_multiplier
    return max(0.0, score)
```
