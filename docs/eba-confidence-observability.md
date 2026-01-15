# EBA Confidence Observability

This document defines the minimum inspection surface for rolling confidence.

The goal is to guarantee that confidence is never a hidden control signal.

## What Must Be Logged When Confidence Is Updated

Every time confidence is updated (including task-cycle updates or manual overrides/resets), the following must be observable:

- Current confidence value (scalar ∈ [0, 1])  
- Delta from previous value (signed change)  
- Reason for change (human-readable string)  
  Example: “confidence dropped because 2 recent tasks FAILED with severe drift”  
  Example: “confidence increased because 3 recent tasks SUCCEEDED and memory scores are low-risk”  
- Contributing inputs (summarized)  
  - Recent outcomes (success/failure count or trend)  
  - Aggregated memory signals (negative memory weight)  
  - Current policy mode (NORMAL/GUIDED/ENFORCED/HALT)  
- Timestamp of update  

All changes must be attributable to explicit inputs — no opaque internal adjustments.

## Minimum Inspection Surface

At minimum, the following must be available at runtime or in logs:

- Current confidence value  
- Confidence history (recent values + deltas)  
- Causal explanation for each change  
  Format: “Confidence changed from X to Y because: [reason]”  
- Policy mode at time of update  
- Whether manual override was applied  

This surface must be:
- Inspectable (queryable via API or log)  
- Explainable (human-readable)  
- Attributable (no anonymous updates)  

## Human-Readable Explanations

Confidence changes must be phrased in natural language, e.g.:

- “Confidence dropped from 0.75 to 0.42 because 2 recent tasks FAILED with severe drift.”  
- “Confidence increased from 0.6 to 0.82 because 3 recent tasks SUCCEEDED and memory scores are low-risk.”  
- “Confidence reset to 0.5 due to manual override (novelty escape hatch).”  

Explanations must include:
- Direction of change  
- Magnitude (approximate)  
- Primary cause(s)  
- Policy mode context  

## Mode-Dependent Verbosity Expectations

- ADVISORY mode: full verbosity (log every change + inputs)  
- GUIDED mode: moderate verbosity (log significant changes only)  
- ENFORCED mode: high verbosity on any change (audit trail required)  
- HALT mode: log final confidence and reason for halt  

Verbosity must never hide information — only reduce noise in low-risk modes.

## Audit/Debugging Expectations

- Confidence history must be replayable in principle (i.e., sufficient inputs are logged to allow deterministic reconstruction)  
- Every change must have a logged cause  
- No silent confidence updates  
- Manual overrides must be logged with justification  

This ensures confidence is fully auditable and debuggable.

## Explicit Non-Goals

This document does not define:
- Storage schema  
- Logging backend  
- UI commitments  
- Exact log format  
- Numeric update rules  

Those belong to future implementation commits.

## See also

eba-confidence.md — general confidence semantics  
eba-rolling-confidence-semantics.md — rolling update rules  
eba-confidence-breadth.md — confidence-to-breadth mapping  
eba-policy-modes.md — policy modulation of confidence influence  
appendix/eba-confidence-failure-asymmetry.md — justification for asymmetric confidence updates  

This document defines observability semantics only — no APIs, no implementation, no forward commitments.
