# ECK Policy Modes

## 1. Purpose of Policy

Policy interprets epistemic signals (confidence, memory scores) into behavioral guidance.

Policy never generates content.  
Policy never alters memory.  
Policy governs how epistemic risk is handled, not what is believed, and not how reasoning is performed.

Non-goal: Policy does not decide truth, correctness, or safety.

## 2. Separation of Concerns

ECK explicitly separates layers:

- Memory → stores and scores past experience  
- Confidence → summarizes epistemic risk  
- Policy → interprets confidence into behavioral guidance  
- Prediction / Generation → may observe policy outputs but does not own policy logic  

Prediction may observe policy outputs, but policy must not depend on prediction internals.

Why separation matters:  
Auditability, composability, and reuse depend on clear boundaries.  
Policy must remain inspectable and modifiable without touching reasoning or memory.

## 3. Policy Modes (Canonical Set)

### 3.1 NORMAL Mode

Intent: Full agent operation (default).  
Confidence has no influence.  
No recommendations or constraints applied.

### 3.2 GUIDED Mode

Intent: Soft influence without enforcement.  

Confidence influences defaults (e.g. breadth, exploration).  
No hard limits are imposed.  
Prediction may override defaults freely.  
Novelty is discouraged, never blocked.  

This is the recommended default operational mode.

### 3.3 ENFORCED Mode

Intent: Hard epistemic control under explicit opt-in.  

Confidence may impose constraints.  
Actions may be restricted, deferred, or halted.  
Negative memory may dominate prioritization.  
Violations must be explicit and logged.  
Enforcement must be attributable to policy mode, not model behavior.  

Used for high-risk, high-cost, or safety-critical domains.

### 3.4 HALT Mode

Intent: Complete halt (irreversible until manual reset).  
No further task generation or execution.  
All effects short-circuited.

## 4. Soft vs Hard Gating

Soft Gating  
Shapes defaults  
Suggests expansion or caution  
Always overridable  
Never blocks execution  
Does not change admissible action space  

Hard Gating  
Imposes constraints  
May prevent continuation  
Requires explicit override mechanisms  
Must be mode-gated (ENFORCED only)  
Restricts admissible action space  

| Gating Type | Effect on Defaults | Override Possible? | Blocks Execution? | Changes Action Space? | Mode      |
|-------------|---------------------|---------------------|-------------------|-----------------------|-----------|
| Soft        | Influences          | Yes                 | No                | No                    | GUIDED    |
| Hard        | Constrains          | Yes (explicit)      | Yes (possible)    | Yes                   | ENFORCED  |

## 5. Authority Boundaries

Policy must not:
- Modify generation tokens  
- Rewrite prompts  
- Alter confidence values  
- Silently enforce constraints outside ENFORCED mode  

Policy must never cross into prediction, generation, or memory execution paths.

## 6. Novelty Escape Hatches

Policy may discourage novelty but must never make it impossible.  

Mechanisms include:
- Manual overrides  
- Exploration flags  
- Research mode exemptions  
- Logged justification requirements  

Invariant: Novelty may be discouraged, but must never be forbidden.

## 7. Invariants

- Policy mode must be explicit  
- Enforcement must be observable  
- Confidence remains epistemic, not correctness-based  
- Disabling policy restores baseline behavior  

## 8. Non-goals

Policy does not:
- Evaluate truth  
- Replace reasoning  
- Operate at token-level  
- Substitute for model uncertainty  
- Decide final answers  

## 9. Relationship to Other Phases (Non-binding)

This document defines semantics only.  
All runtime wiring and enforcement are complete (see Phase 2.2 and Phase 3).  
No further commitments beyond current implementation.
