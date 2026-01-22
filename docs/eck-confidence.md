# ECK Confidence Definition

ECK's confidence is the system's belief that its current epistemic trajectory is safe to continue without forced expansion (breadth increase, alternative hypothesis generation, or deferral).

## Confidence Defined

Confidence ∈ [0, 1]

**Confidence is not a probability of correctness and must not be interpreted as such.**

Increases when:
- Similar past tasks succeeded
- Failures were rare / distant
- Memory scores are low-risk
- Policy mode is permissive

Decreases when:
- Similar tasks failed
- Failures were severe
- Failures cluster
- Policy mode tightens

## Bounds

- Confidence is monotonic within a mode: cannot increase after a failure event (unless manual override)
- Confidence is bounded: 0 = complete doubt (halt or defer)
- Confidence is inspectable: always log confidence changes with causal attribution
- A failure event refers to a failure relevant to the current task or epistemic trajectory (as defined by similarity and policy).

## Inputs

- Similarity-weighted past outcomes (failure/success, severity)
- Drift signals (perceptual z-score, streak, feasibility bias)
- Policy mode (NORMAL = permissive, CONSERVATIVE = tighter bounds, HALT = 0)
- Explicit novelty overrides (user-forced exploration)

## Failure Modes

- Over-suppression: too aggressive on negative memory → sterile reasoning
- Under-suppression: too permissive on failures → hallucinated novelty
- Divergence: confidence drift from policy mode → inspectable via logs

## Invariants

- Confidence must never increase after a failure event (unless manual override)
- Confidence must always be explainable ("because of X, Y, Z")
- Confidence must allow intentional violation (novelty escape hatches)
- Confidence must remain model-agnostic (no logits, no token probs)

## Non-goals

Confidence does not estimate factual correctness  
Confidence does not guarantee safety  
Confidence does not replace model uncertainty  
Confidence does not operate at token level

This document defines semantics only; it does not prescribe a specific computation or update rule.

See also: ECK Confidence vs LLM Uncertainty for how this differs from LLM internals.
