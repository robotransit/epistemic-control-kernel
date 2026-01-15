# EBA Confidence → Breadth Defaults (Semantics Only)

This document defines how confidence influences breadth defaults — semantics only, no APIs, no implementation, no wiring.

## Confidence Defined

Confidence ∈ [0, 1] (see docs/eba-confidence.md)

Breadth defaults are soft guidance only (GUIDED mode).  
In ENFORCED mode, breadth may be hard-constrained.

## Breadth Levels (Canonical Set)

- FULL (default in NORMAL): no restriction on subtask generation or exploration depth  
  Breadth governs task expansion and exploration depth, not reasoning quality.  
- MODERATE: reduce max_subtasks, limit hypothesis branching  
- RESTRICTED: minimal subtasks, prioritize known safe paths  
- DEFERRED: no subtasks generated, defer to user or halt  

## Mapping (Confidence → Breadth)

| Confidence Range | Recommended Breadth | Policy Mode Permission | Notes / Invariants |
|------------------|----------------------|------------------------|--------------------|
| 0.8 – 1.0        | FULL                | NORMAL, GUIDED         | High confidence = full exploration allowed |
| 0.5 – 0.8        | MODERATE            | GUIDED only            | Moderate confidence → soft constraint on novelty |
| 0.3 – 0.5        | RESTRICTED          | GUIDED or ENFORCED     | Low confidence → prioritize safety over breadth |
| 0.0 – 0.3        | DEFERRED            | ENFORCED only          | Extreme doubt → no continuation without override |

## Invariants (must hold)

- Breadth must never increase after a failure event (unless manual override)  
- Breadth defaults must be overridable in GUIDED mode  
- All breadth defaults in GUIDED mode are advisory and may be overridden by higher-level orchestration  
- Breadth must be inspectable (logged when changed)  
- Breadth must not suppress novelty entirely — only discourage it  
- In ADVISORY mode, breadth must always be FULL (no influence)  
- In HALT mode, breadth is irrelevant (no generation occurs)  

## Non-goals

- Breadth does not replace confidence computation  
- Breadth does not directly alter prompt content  
- Breadth does not operate at token level  
- Breadth does not guarantee correctness or safety  

## Relationship to Future Commits

This semantics draft is non-binding on implementation.  
Commit 4b will consume this mapping to set defaults (soft gating).  
Commit 4c will add hard constraints under ENFORCED mode.  

This document defines semantics only — no APIs, no wiring, no forward commitments.
