# ECK Confidence → Breadth Defaults (Semantics Only)

This document defines how confidence influences breadth defaults — semantics only, no APIs, no implementation, no wiring.

## Confidence Defined

Confidence ∈ [0, 1] (see docs/eck-confidence.md)

Breadth defaults are soft guidance only and apply exclusively in GUIDED mode (NORMAL is unaffected).  
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
- In NORMAL mode, breadth must always be FULL (no influence)  
- In HALT mode, breadth is irrelevant (no generation occurs)  
- Absence of confidence data or computation must default to FULL breadth (no suppression by default)

## Non-goals

- Breadth does not replace confidence computation  
- Breadth does not directly alter prompt content  
- Breadth does not operate at token level  
- Breadth does not guarantee correctness or safety  

## Confidence → Breadth Resolver (Semantics Sketch)

This section describes semantic intent only; it does not imply a callable component.

Confidence → breadth mapping is a **pure, declarative resolver** — no computation, no enforcement, no side effects.

It answers:

“What breadth default is justified given current confidence and policy mode?”

The resolver consumes:
- Current confidence (scalar ∈ [0, 1], opaque)
- Current policy mode (NORMAL / GUIDED / ENFORCED / HALT)

It produces:
- Recommended breadth level (FULL, MODERATE, RESTRICTED, DEFERRED)

The mapping is defined in the table above.

The resolver must:
- Be deterministic (same inputs → same output)
- Be inspectable (logged when consulted)
- Be overridable (higher-level orchestration may ignore)
- Never enforce (soft guidance only in GUIDED mode)
- Never increase breadth after failure (monotonicity invariant)

The resolver must not:
- Compute confidence
- Modify confidence
- Read memory directly
- Depend on prediction internals
- Alter prompts or generation
- Trigger hard gating (deferred to future commits)

This resolver is a **translation layer** — confidence (epistemic signal) → breadth (behavioral guidance).

It is **not** a decision engine.

## See also 
eck-confidence.md — general confidence semantics 
eck-rolling-confidence-semantics.md — rolling update rules 
eck-policy-modes.md — policy modulation of confidence influence
appendix/eck-confidence-failure-asymmetry.md — justification for asymmetric confidence updates

## Relationship to Other Commits

- **Commit 4a**  
  Supplies gated, read-only context used upstream in confidence estimation

- **Commit 4b (this commit)**  
  Translates confidence into recommended breadth defaults

- **Commit 4c (future)**  
  Introduces hard constraints and irreversible enforcement under ENFORCED mode  

This document defines semantics only — no APIs, no wiring, no forward commitments.
