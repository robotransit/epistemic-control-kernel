# Commit 4b — Confidence Intent & Scope (Semantics Only)

This document defines the exact intent, scope, and invariants of Commit 4b.

Commit 4b translates rolling confidence into recommended breadth defaults — soft guidance only.

It does **not** enforce, constrain, or alter generation behavior.

## What Commit 4b Introduces

Commit 4b introduces:

- Consumption of rolling confidence as an epistemic signal (see eba-rolling-confidence-semantics.md)  
- Asymmetric failure weighting (see appendix/eba-confidence-failure-asymmetry.md)  
- Observability guarantees (see eba-confidence-observability.md)  
- Translation from confidence to recommended breadth level (see eba-confidence-breadth.md)  

All of the above are **declarative semantics** — no enforcement, no side effects.

## What Commit 4b Explicitly Does Not Introduce

Commit 4b does **not**:
- Compute, smooth, or decay confidence  
- Enforce breadth limits (hard gating deferred to Commit 4c)  
- Prevent subtask generation  
- Modify prompts or context  
- Alter generation parameters (temperature, breadth, exploration)  
- Introduce new configuration fields  
- Persist state  
- Trigger irreversible suppression  
- Depend on model internals (logits, token probs)  

All enforcement, irreversible behaviour, and hard constraints are deferred to Commit 4c.

## Global Invariants (Must Hold Across 4b)

- Confidence is inspectable and attributable — never hidden or opaque  
- Confidence never claims correctness — only regulates epistemic risk  
- Breadth translation is advisory in GUIDED mode — always overridable  
- Breadth must not suppress novelty entirely — only discourage it  
- Absence of confidence data defaults to FULL breadth (no suppression by default)  
- Failure asymmetry is invariant — trust lost faster than gained  
- NORMAL mode is unaffected — no influence from confidence  
- HALT mode renders breadth irrelevant — no generation occurs  
- All changes must be explainable (“because of X recent outcomes”)  

These invariants span all prior semantics docs and must not be violated by Commit 4b.

## Why 4b Must Exist Before 4c

Commit 4b establishes:
- Confidence semantics before enforcement  
- Breadth defaults before constraints  
- Observability before power  

This prevents premature coupling, ensures auditability, and keeps hard gating (Commit 4c) a deliberate, incremental choice rather than an accident.

This document is the contract for Commit 4b — semantics only, no APIs, no wiring, no forward commitments.
