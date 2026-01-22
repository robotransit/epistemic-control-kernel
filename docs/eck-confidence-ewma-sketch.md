### Minimal EWMA-style Confidence Formula (Semantics Sketch, Not Final)

Confidence is updated after each task cycle (post-critic evaluation).

**Base formula** (EWMA over success signal):

confidence_new = α × success_signal + (1 - α) × confidence_old

Where:
- **success_signal** ∈ [0, 1]  
  - 1.0 = SUCCEEDED  
  - 0.0 = FAILED  
  - 0.5 = REJECTED_BY_CRITIC or partial success (configurable)  
  - 0.0 = DEFERRED (policy halt; treated as non-success for confidence purposes)  

- **α** (smoothing factor): 0 < α ≤ 1  
  - Higher α = more weight on recent outcomes (faster adaptation)  
  - Lower α = more stability (slower to forget old outcomes)  
  - Suggested default: α = 0.3 (balances recency and history)

- **confidence_old** = previous cycle's confidence  
  - Initial value (no history): 0.5 (neutral)

**Optional severity weighting** (to make failures hurt more):

success_signal = 1.0 if success else failure_penalty
failure_penalty = 0.2  # or config.failure_penalty = 0.2

**Optional recency decay** (alternative to simple EWMA):

success_signal = success_signal × recency_factor
recency_factor = decay ^ age_in_cycles  # e.g. decay = 0.9

**Boundary conditions** (invariants):
- confidence clamped to [0, 1]
- Upward movement is suppressed for at least one update window following a failure  
- On no data (first cycle): confidence = 0.5
- Manual override: user can force confidence = 1.0 or 0.0 (novelty escape)

**Why this is minimal & useful**:
- No numeric prediction required (works with qualitative outcomes)  
- Bounded [0,1] — easy to map to breadth defaults  
- Interpretable (“recent successes build trust”)  
- Trend-sensitive (EWMA reacts to improving/degrading patterns)  
- Conservative by default (failures pull down faster if penalty > 1-α)  

This is **not a commitment** — just a sketch to test against your invariants (monotonicity, explainability, model-agnostic).
