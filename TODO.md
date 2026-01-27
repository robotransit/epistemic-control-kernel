# TODO.md for Epistemic Control Kernel (ECK)

This file outlines outstanding tasks, placeholders, unfinished features, and
planned enhancements based on a review of the repository state as of
**ECK v0.1.1 (2026-01-27)**.

All items listed here are **explicitly out of scope for the v0.1.x series** and
do **not** affect the correctness, completeness, or invariants of the
currently tagged releases (v0.1.0, v0.1.1).

The v0.1.x line is considered **behaviorally stable** and **test-complete**.
Future work targets v0.2.0 and beyond.

## Core Functionality
These address placeholders in the code and integrate existing but unused components.

- **High: Implement dynamic rolling confidence signal**  
  In `eck/agent.py`, `self.current_confidence` is hardcoded to 0.5 with comment
  "# Current confidence (placeholder — future: rolling signal)".  
  Integrate an Exponentially Weighted Moving Average (EWMA) mechanism as outlined in:
  - `docs/eck-confidence-ewma-sketch.md`
  - `docs/eck-rolling-confidence-semantics.md`
  - `docs/appendix/eck-confidence-failure-asymmetry.md`  
  Update the agent loop to compute and update confidence based on task outcomes,
  drifts, and feasibility checks.  
  **Safety invariant**: Confidence updates cannot directly trigger enforcement
  without explicit policy mediation.

- **High: Finalize and test memory-aware prediction context wiring**  
  In `eck/memory.py`, methods like `retrieve_similar` and `retrieve_scored` are
  implemented and partially wired (memory passed to
  `build_prediction_context` via `generate_prediction`).  
  Complete controlled activation when `config.enable_memory_retrieval` is True,
  add tests for observability, and ensure read-only influence with no behavioral
  authority.

- **Medium: Upgrade task similarity computation to embedding-based cosine similarity**  
  In `eck/memory.py`, `get_similar` uses a basic string overlap metric, commented
  "Placeholder similarity function (string overlap) — future: use real cosine sim
  on embeddings".  
  Implement using a lightweight embedding library (e.g., sentence-transformers as
  optional dependency) or a TF-IDF fallback.  
  Update config thresholds and ensure backward compatibility.

- **Medium: Incorporate unused prompts or remove them**  
  In `eck/prompts.py`, confirm usage of all prompts.
  `PRIORITIZATION_PROMPT` and possibly `GOAL_ACHIEVED_PROMPT` lack clear runtime
  integration.  
  Integrate (e.g., prioritization after subtask generation) or remove to reduce
  overhead.

- **Medium: Define specific formulas and constants for confidence asymmetry**  
  Formalize EWMA alpha, decay rates, failure penalties, enforcement mechanisms,
  and persistence (details deferred in
  `docs/appendix/eck-confidence-failure-asymmetry.md`).  
  Implement in code (e.g., `drift.py` or a dedicated confidence module) and
  update documentation.

- **Low: Document task seeding patterns in README / examples**  
  `ECKAgent.seed()` is already public and functional.  
  Improve documentation clarity (README.md and/or `examples/basic_run.py`)
  for seeding patterns.

## Testing
Comprehensive deterministic unit and integration tests are in place as of v0.1.1.
Future testing work focuses on:
- Regression protection for new features
- Confidence dynamics (v0.2.0)
- Performance and scale characteristics

- **Low: Implement CI workflow**  
  GitHub Actions: pytest on push/PR, linting (black/flake8), coverage (>80%).  
  CI must not introduce behavioral dependencies (e.g., network calls, external APIs).

## Documentation
- **Medium: Add usage guide for policy modes**  
  Expand `docs/eck-policy-modes.md` with examples of dynamic switching (e.g.,
  based on drift) and impacts on breadth/confidence.

- **Low: Consolidate confidence documentation**  
  Merge scattered files (e.g., `eck-confidence.md`,
  `eck-confidence-breadth.md`,
  `eck-confidence-observability.md`) into a single guide, cross-referencing
  asymmetry and EWMA semantics.

- **Low: Add CONTRIBUTING.md issue templates**  
  Templates for bugs, features, and documentation changes.

## Miscellaneous / Refinements
- **Low: Add optional dependencies for advanced features**  
  Add an `embeddings` extra in `pyproject.toml`
  (e.g., sentence-transformers). Keep the core stdlib-only.

- **Low: Benchmark and optimize queue/performance**  
  Test `TaskQueue` for large `max_size` values; add performance tests if
  scaling becomes relevant.

Contributions are welcome; please see `CONTRIBUTING.md` for invariants, scope,
and contribution guidelines.
