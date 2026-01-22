"""
Epistemic Control Kernel (ECK).

Provides:

Prediction vs outcome tracking

Multi-level drift detection

Heuristic self-tuning (numeric bias adaptation)

Guard rails & reset logic
"""

version = "0.1.0"

from .agent import ECKAgent
from .config import ECKConfig

__all__ = [
    "ECKAgent",
    "ECKConfig",
]
