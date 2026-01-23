# Epistemic Control Kernel (ECK)

**Epistemic Control Kernel (ECK)** — a minimal, reliability-first control kernel for autonomous agents.

ECK is a framework-agnostic **control and observability core**, designed to sit *beneath* agent behaviour rather than define it.  
It enforces explicit phase separation, records epistemic signals, detects drift, and provides **policy-gated control seams** without embedding planning, reasoning, or tool ideology.

ECK prioritises:
- observability before enforcement  
- explicit state transitions  
- testable, auditable invariants  
- refusal to silently “do the wrong thing”

This repository contains the **core kernel only** — not a full agent product.

---

## Current Status (v0.1.x)

ECK is in an **early but internally consistent** state.

### Implemented & Stable

- Deterministic agent control loop (`agent.py`)
- Explicit prediction → execution → evaluation phases
- Policy-gated execution and subtask generation
- Critic-mediated outcome evaluation
- Drift monitoring (error signals, feasibility checks, streak tracking)
- Append-only task memory with explicit task states
- Bounded task queue
- Centralised prompt templates
- Minimal execution seam (LLM-first, tool-extensible)
- Strict config-driven thresholds and limits

### Explicitly Not Implemented (by design)

- No planning engine
- No hidden reasoning layer
- No implicit tool use
- No asynchronous or parallel execution
- No task deduplication heuristics
- No automatic “intelligence amplification”

If something is not visible in code or tests, **it does not exist**.

---

## Design Philosophy

ECK is built around **epistemic control**, not task throughput.

Key principles:

- **Explicit phases**  
  Prediction, execution, and evaluation are separate and observable.

- **Observability before enforcement**  
  Signals (confidence, drift, feasibility) are recorded *before* they affect behaviour.

- **No silent coupling**  
  Confidence does not alter behaviour unless an explicit policy mode allows it.

- **Single execution seam**  
  All real-world effects flow through one narrow interface.

- **Irreversible safety upgrades**  
  Policy modes can only move in safer directions during runtime.

---

## Architecture Overview

ECK separates *cognition*, *control*, and *effects*.

### Pure / Stateless Components
(no side effects, no memory mutation)

- `prediction.generate_prediction`
- `task_generation.generate_subtasks`

### Execution Seam
(single, auditable effects boundary)

- `execution.execute_task`

### Stateful Control Layer

- `ECKAgent` — orchestration and policy control
- `WorldModel` — append-only task history
- `DriftMonitor` — epistemic error & instability tracking
- `TaskQueue` — bounded work queue

This architecture allows ECK to integrate with **any LLM stack** without inheriting framework assumptions.

---

## Policy Enforcement

ECK can now enforce recommendations in ENFORCED mode across both subtask generation and task execution.  
When recommended breadth is DEFERRED, generation and execution are skipped for the cycle.  

- Enforcement is minimal, reversible, and fully logged  
- See Commit 4c for implementation details  
- See scratch_test_4c.py for a minimal proof-of-concept run demonstrating deferral  

This completes the core reliability loop within ECK: detection → recommendation → consequence.

---

## What ECK Is *Not*

ECK is intentionally narrow.

It is **not**:

- A general agent framework
- A planner or reasoning engine
- A tool orchestration system
- A LangChain / LangGraph replacement
- A multi-agent system
- A production-ready autonomous product
- An opinionated AI ideology

ECK exists to make agent behaviour **inspectable, interruptible, and correctable**.

---

## Quick Start

You must supply your own LLM callable.
```
# First install the package locally
# pip install -e .

from eck.agent import ECKAgent

def llm(prompt: str) -> str:
    return "stub response"

agent = ECKAgent(
    objective="Replace with a real objective",
    llm_call=llm,
)

agent.seed()
agent.run()
```
⚠️ A stub LLM will not produce meaningful behaviour — this example demonstrates control flow only.

---

## Project Structure

### Core Package (`eck/`)

- **agent.py** — control loop orchestration & policy enforcement  
- **config.py** — immutable configuration & policy thresholds  
- **task.py** — canonical task lifecycle states  
- **queue.py** — bounded task queue  
- **memory.py** — append-only task history  
- **prediction.py** — pure prediction generation  
- **task_generation.py** — pure subtask generation  
- **execution.py** — execution seam  
- **critic.py** — outcome evaluation  
- **drift.py** — drift & instability detection  
- **utils.py** — safe helpers (parsing, feasibility checks, scoring)  
- **prompts.py** — centralised prompt templates  

---

## Dependencies

ECK intentionally relies almost entirely on the **Python standard library**.

Additional dependencies may be introduced **only** when they provide:

- clear epistemic value
- testable behaviour
- no hidden control flow

---

## License

MIT License — see the `LICENSE` file for details.
