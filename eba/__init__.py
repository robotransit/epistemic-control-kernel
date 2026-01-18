"""
EBA Core — Enhanced BabyAGI reliability kernel.

Provides:

Prediction vs outcome tracking

Multi-level drift detection

Heuristic self-tuning (numeric bias adaptation)

Guard rails & reset logic
"""

version = "0.1.0"

from .agent import EBACoreAgent
from .config import EBACoreConfig

all = [
"EBACoreAgent",
"EBACoreConfig",
]
