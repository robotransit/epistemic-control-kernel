# EBA Confidence — Failure Asymmetry

This appendix explains why confidence decreases more strongly on failures than it increases on successes.

It is a deliberate design choice, not an implementation accident.

## Why Symmetric Smoothing Is Unsafe for Epistemic Systems

Symmetric updates (equal gain on success, equal loss on failure) treat epistemic risk as reversible.

In real reasoning:
- A single severe failure can invalidate a long chain of successes  
- Repeated minor successes rarely fully restore trust after a major violation  
- Epistemic posture must be conservative: trust lost faster than trust gained  

Symmetric smoothing would allow:
- Confidence to rebound too quickly after failure  
- Overconfident continuation after a red flag  
- Drift into dangerous trajectories without lasting consequence  

Asymmetry is the safest default for self-regulating epistemic systems.

## Failure Severity vs Success Accumulation

Failures are not symmetric to successes because:

- Successes are expected baseline behavior  
- Failures are evidence of epistemic violation  

A single high-severity failure (e.g. critic rejection, severe drift) should outweigh multiple low-severity successes.

Accumulation of successes builds confidence slowly and steadily.  
A single failure can collapse it rapidly.

This mirrors human reasoning hygiene:  
“Trust is hard to earn and easy to lose.”

## One-Way Ratchets and Recovery Lag

Failures create a one-way ratchet effect:

- Confidence drops sharply on failure  
- Recovery requires sustained evidence of safety  
- No automatic upward reset after failure  

This lag enforces caution:
- Agent remains constrained until confidence rebuilds  
- Novelty is discouraged during recovery  
- Exploration is gated by demonstrated reliability  

Recovery lag is intentional — it prevents oscillation between optimism and panic.

## Human-Interpretable Rationale

“Trust lost faster than gained” is not just intuitive — it is epistemically rational:

- False positives (overconfident continuation) are more dangerous than false negatives (overcautious restraint)  
- In agent systems, over-suppression is recoverable; under-suppression can lead to irreversible drift  
- Asymmetry is the natural safety bias for autonomous reasoning  

## Explicit Non-Goals

This document does not prescribe a specific formula, constant, or implementation.

It does not define:
- EWMA alpha or decay rates
- Failure penalty values
- Enforcement mechanisms
- Persistence or memory mechanics

Those belong to future implementation commits.

## See also

eba-confidence.md — general confidence semantics  
eba-rolling-confidence-semantics.md — rolling update rules  
eba-confidence-breadth.md — confidence-to-breadth mapping  
eba-confidence-observability.md — logging and attribution  
eba-policy-modes.md — policy modulation of confidence influence  

This appendix is semantics only — it justifies asymmetry as a design invariant.
