# ECK Rolling Confidence Semantics

This document defines how rolling confidence is computed and used — semantics only, no APIs, no implementation details.

## Confidence Defined

Rolling confidence (hereafter “confidence”) ∈ [0, 1] (see docs/eck-confidence.md)

Confidence is an epistemic posture signal:  
“How justified am I, right now, in expanding the search space?”

Confidence is **not**:
- Probability of correctness
- Token-level uncertainty
- Prediction error (MAE/RMSE)
- Model log-probability
- Calibration score

## Computation (Semantics Only)

Confidence is updated per task cycle based on recent outcomes.

Suggested approach (candidate, not final):
- Start at neutral (0.5)  
- Each outcome nudges confidence:  
  - Success → increase (weighted by recency)  
  - Failure → decrease (weighted by severity)  
  - Partial / rejected → small decrease  
- Use EWMA (exponential moving average) over success signal (0/1 or partial credit)  
- Decay older outcomes exponentially  

This gives:
- Bounded [0,1]  
- Smooth trend sensitivity  
- Interpretable (“recent successes build trust”)  
- No numeric prediction required  

Alternative (future): Beta posterior (α successes, β failures) for Bayesian uncertainty modeling.

## Inputs

- Recent task outcomes (success/failure, severity)  
- Aggregated outcome signals (negative outcomes weigh heavier via memory retrieval)  
- Policy mode (NORMAL permissive, CONSERVATIVE tighter bounds)  

## Invariants

- Confidence must be monotonic within a mode: cannot increase after a failure event (unless manual override)  
- Confidence must be monotonically non-increasing after a failure event; upward updates must be clamped or reduced (asymmetric smoothing required)  
- Confidence must always be explainable (“because of X recent outcomes”)  
- Confidence must default to 0.5 (neutral) on no data  
- Confidence must allow intentional override (novelty escape hatches)  

## Non-goals

- Confidence does not estimate factual correctness  
- Confidence does not replace model uncertainty  
- Confidence does not operate at token level  
- Confidence does not guarantee safety  

## Relationship to Other Docs

- **eck-confidence.md** — general confidence semantics  
- **eck-confidence-breadth.md** — how confidence maps to breadth defaults  
- **eck-policy-modes.md** — how policy mode modulates confidence influence  

This document defines semantics only — no APIs, no wiring, no forward commitments.
