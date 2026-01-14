# Commit 4a API Boundary Sketch (Design-Only)

## Intent

Commit 4a introduces the first read-only behavioural influence of memory on prediction.

It must remain strictly non-authoritative: memory context is informational only, never prescriptive.

The commit must satisfy all of the following invariants:

## Invariants (must be true after commit)

1. No behavioural change unless explicitly enabled
   - When config.enable_memory_retrieval = False → prediction prompt unchanged
   - No default-on behaviour

2. Prediction prompt must have an explicit, dedicated slot
   - {memory_context} placeholder exists in PREDICTION_PROMPT_TEMPLATE
   - Context is injected via format_prompt (no string concatenation)

3. Context is always optional and non-binding
   - Context is a string (possibly empty)
   - Prediction function must handle empty context identically to pre-Commit 4a

4. No policy or confidence modulation yet
   - No reading of policy_mode inside prediction.py
   - No confidence adjustment based on retrieved memory

5. Retrieval is read-only
   - No memory mutation
   - No state change
   - No side effects

6. Gating is explicit and centralized
   - Config.enable_memory_retrieval is the single gate
   - No implicit enabling

7. Auditability guarantee
   - When context is non-empty, it must be possible to log or inspect it
   - No silent injection

8. Forbidden: Any interpretation of memory context semantics inside prediction logic (e.g. “if failures exist, then…”)

9. Prediction treats {memory_context} as opaque text; it must not parse or reason over its structure

## Boundary Conditions

Allowed in Commit 4a:
- Call retrieve_scored() or equivalent in prediction context builder
- Inject context string into prompt via placeholder
- Truncate or format context for brevity

Forbidden in Commit 4a:
- Any weighting of context tokens
- Any confidence score adjustment
- Any change to prediction breadth or temperature
- Any policy mode reading inside prediction.py
- Any memory mutation or state change

## Success Criteria

After Commit 4a:
- config.enable_memory_retrieval = False → identical prompt to pre-commit
- config.enable_memory_retrieval = True → prompt includes memory context (if relevant)
- No new behaviour in agent loop
- No new dependencies
- No new side effects

This commit completes the “memory-aware prediction infrastructure” without yet exercising influence.
