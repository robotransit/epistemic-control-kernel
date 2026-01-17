# Commit 4c Go / No-Go Checklist

**Binding Reference**  
This checklist is governed by ADR-00X: Deferred Enforcement via Breadth Recommendation (docs/ADR-00X-deferred-enforcement.md).  
Any enforcement introduced in Commit 4c must comply with the ADR’s invariants, separation of concerns, and staged model.  
If any item fails, do NOT merge Commit 4c. Fix first.

## Must be TRUE before merge

[ ] All tests from Commit 4b pass (mapping, thresholds, logging observability)  
[ ] Resolver is deterministic (same inputs → same breadth recommendation)  
[ ] Config disable (enable_memory_retrieval = False) restores pre-4a/4b behavior (bit-for-bit prompt identity)  
[ ] Logging is present and attributable (confidence changes, breadth recommendations, mode upgrades)  
[ ] No silent enforcement exists (GUIDED mode remains advisory; no hard limits applied outside ENFORCED)  
[ ] Manual override works and takes precedence over enforcement (forced FULL or DEFERRED via config/policy)  
[ ] Failure asymmetry invariant holds (confidence cannot increase after failure)  
[ ] Novelty escape hatch works (forced exploration possible in GUIDED mode)  
[ ] HALT mode renders breadth irrelevant (no generation occurs)  
[ ] Policy mode is single-sourced (config.policy_mode is authoritative)  
[ ] DriftMonitor config is synced after policy upgrade (self.drift.config = self.config)  
[ ] No new dependencies introduced  
[ ] No prompt mutation outside gated context  
[ ] All enforcement decisions are explainable in logs (“enforced because confidence X triggered Y in mode Z”)  

## Must be FALSE (safety gates)

[ ] No hard constraints applied in GUIDED mode  
[ ] No irreversible suppression in NORMAL mode  
[ ] No automatic mode downgrade after failure  
[ ] No silent policy mutation (config remains immutable)  
[ ] No confidence computation inside enforcement logic  

## Post-merge observability (must be verifiable)

[ ] Run a short test loop with config.enable_memory_retrieval = True  
[ ] Verify logs show confidence → breadth recommendation  
[ ] Verify logs show policy mode upgrades (if drift triggers)  
[ ] Verify HALT mode stops generation  
[ ] Verify no unintended prompt changes when disabled  
[ ] Verify logs distinguish recommendation from enforcement (advisory vs applied)  

If any item above fails → do NOT merge Commit 4c. Fix first.

This checklist must be completed and signed off before any enforcement commit.
