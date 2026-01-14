# EBA Canonical Roadmap

## Phase 2 — Epistemic Memory & Control

### Phase 2.1 — Memory Infrastructure (COMPLETED)

*Persistent, scoreable memory with zero behavioral authority*

Phase 2.1  
├─ ✔ Commit 1   Memory storage primitives  
│               - Task records  
│               - Outcomes, success, timestamps  
│  
├─ ✔ Commit 2a  Memory retrieval API  
│               - get_similar()  
│               - retrieve_similar()  
│  
├─ ✔ Commit 2b  Config gating for memory usage  
│               - Disabled by default  
│               - No implicit behavior change  
│  
├─ ✔ Commit 3   Memory scoring primitives  
│               - Severity weighting  
│               - Similarity weighting  
│               - Policy-aware scoring  
│  
└─ ✔ Commit 4   retrieve_scored() primitive  
                - Deterministic ordering  
                - Score > 0 filtering  
                - Still read-only  

### Phase 2.1.5 — Epistemic Semantics (COMPLETED)

*Define epistemic signals before wiring behavior*

Phase 2.1.5  
├─ ✔ docs/eba-confidence.md  
│    ├─ Confidence definition (epistemic, not correctness)  
│    ├─ Bounds, invariants, non-goals  
│    └─ Model-agnostic semantics  
│  
├─ ✔ docs/eba-confidence-vs-llm-uncertainty.md  
│    ├─ External vs internal uncertainty  
│    ├─ Task-level vs token-level  
│    └─ Why EBA must remain separate  
│  
└─ ✔ Cross-reference hygiene  
     - Consistent terminology  
     - Explicit separation preserved  

### Phase 2.1.75 — Policy Semantics (PLANNED — DOCS ONLY)

*Formalize soft vs hard control before enforcement*

Phase 2.1.75  
└─ ⏳ docs/eba-policy-modes.md  
     ├─ Policy modes  
     │    - ADVISORY  
     │    - GUIDED  
     │    - ENFORCED  
     │  
     ├─ Soft vs hard gating  
     │    - Defaults vs constraints  
     │  
     ├─ Authority boundaries  
     │    - Prediction ≠ policy  
     │    - Policy ≠ generation  
     │  
     └─ Novelty escape hatches  
          - Intentional violation  
          - User-forced exploration  

📌 No runtime behavior in this phase.

### Phase 2.2 — Memory-Aware Prediction (NOT STARTED)

*Behavior informed by confidence — policy-controlled*

Phase 2.2  
├─ ⏳ Commit 5a  Prediction receives confidence + policy mode (read-only)  
│               - retrieve_scored() used  
│               - No enforcement  
│               - Observability only  
│  
├─ ⏳ Commit 5b  Policy interprets confidence → breadth defaults  
│               - Soft gating  
│               - Breadth / expansion hints  
│               - No hard limits  
│  
└─ ⏳ Commit 5c  Policy enforces constraints under ENFORCED mode  
                - Hard gating  
                - Deferral / halt permitted  
                - Negative memory dominance  

## Structural Invariants (Global)

- Memory never directly alters generation  
- Confidence never claims correctness  
- Policy interprets, prediction observes  
- Enforcement is explicit, mode-gated  
- Novelty is suppressible but never forbidden  

## Layering Summary

| Layer                  | Phase          | Status | Key Principle                          |
|------------------------|----------------|--------|----------------------------------------|
| Infrastructure         | Phase 2.1      | ✅     | Persistent, scoreable, read-only memory |
| Semantics              | Phase 2.1.5    | ✅     | Define signals before wiring behavior  |
| Policy                 | Phase 2.1.75   | ⏳     | Formalize soft vs hard control         |
| Behavior               | Phase 2.2      | ⏳     | Confidence → controlled influence      |

Each layer is strictly dependent on the guarantees of the previous one; later phases must not retroactively alter earlier-layer invariants.
