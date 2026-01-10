```
python
import uuid
import logging
import math
from typing import List

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

    Returns 0.0 if either vector has zero magnitude.
    """
    if not a or not b:
        return 0.0

    dot = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x * x for x in a))
    mag_b = math.sqrt(sum(x * x for x in b))

    if mag_a == 0 or mag_b == 0:
        return 0.0

    return dot / (mag_a * mag_b)
```
