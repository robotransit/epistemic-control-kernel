# eba-core

**Enhanced BabyAGI** — a perceptually self-regulating autonomous agent with predictive foresight and drift detection.

EBA Core is an early-stage, framework-agnostic reliability kernel for autonomous agents.
It focuses on explicit prediction–execution–evaluation loops, conservative defaults, and first-class drift handling.

## Current Status (v0.1.x)

**Implemented & stable components**  
- Agent loop orchestration (`agent.py`)  
- Prediction-before-execution discipline (`prediction.py`)  
- Modular task generation and execution seams (`task_generation.py`, `execution.py`)  
- Critic evaluation pipeline with consensus and verification hooks (`critic.py`)  
- Drift monitoring (perceptual, streak, numeric feasibility bias) (`drift.py`)  
- Safe JSON parsing and pessimistic fallbacks (`utils.py`)  
- Typed config and minimal memory store (`config.py`, `memory.py`)

**Designed / Planned (not yet implemented)**  
- Embedding-based proactive task filtering (objective–task similarity)
- Full tool integration (execution seam is ready)  
- External vector memory  
- Multi-model or ensemble critics  
- Adaptive threshold tuning  

**Current focus**  
Reliability first: explicit phases, no silent hallucinations, clear halting conditions, and modular seams for future extensions.

## Architecture Overview

EBA Core separates cognition from execution and control:

**Stateless cognitive functions**  
(Pure transformations over text; behavior is entirely mediated by the provided LLM)  
- `prediction.generate_prediction`  
- `task_generation.generate_subtasks`

**Execution seam**  
(Where real-world effects or tools may be invoked)  
- `execution.execute_task`

**Stateful control & safety layer**  
- `EBACoreAgent` (main loop and orchestration)  
- `WorldModel` (task history & annotations)  
- `DriftMonitor` (error tracking, drift detection, recovery)

This design allows EBA Core to plug into any LLM stack (raw APIs, LangChain, LangGraph, etc.) without coupling to a specific framework, while keeping execution effects strictly isolated behind a single seam.

## What EBA Core Is *Not*

EBA Core is intentionally minimal and conservative. It is **not**:

- A multi-agent framework
- A parallel or asynchronous execution engine
- A production-ready autonomous system
- A tool-rich agent (tools are opt-in and currently minimal)
- A LangChain/LangGraph replacement or wrapper
- An opinionated UI or application
- A complete agent with built-in planning or reasoning strategies

EBA Core focuses on **reliability, explicit control flow, and drift-aware autonomy**, and is designed to be embedded into larger systems rather than used as a standalone product.

## Quick Start

EBA Core requires you to supply your own LLM callable (e.g. OpenAI, Groq, local model).

Minimal example (stub LLM):
```
python
from eba.agent import EBACoreAgent

def my_llm(prompt: str) -> str:
    return "stub response"  # Replace with real LLM call

agent = EBACoreAgent(
    objective="Example objective - replace this!",
    llm_call=my_llm,
)

agent.seed()  # Starts with an initial task (or generate one automatically)
agent.run()   # Runs until halt or max iterations
```
Note: This stub LLM does not perform real reasoning; it only demonstrates the EBA control flow.  
See examples/ for progressively richer integrations (coming soon).

### How to Run (Local / Minimal Setup)

```
git clone https://github.com/robotransit/eba-core.git
cd eba-core
pip install -e .
```
Then run your own script using the stub example above.

## Project Structure

EBA Core is organized as a Python package with a single core module folder and examples.

**Core package (`eba/`)**  
- `agent.py` → main loop orchestration  
- `config.py` → typed thresholds & limits  
- `prompts.py` → LLM prompt templates  
- `utils.py` → safe helpers (parsing, numeric checks, etc.)  
- `queue.py` → bounded task queue  
- `memory.py` → task history store with metadata  
- `drift.py` → multi-level drift detection  
- `critic.py` → evaluation with consensus & verification  
- `prediction.py` → pure prediction generation  
- `task_generation.py` → pure subtask generation  
- `execution.py` → execution seam (LLM-first, tool-extensible)

**Examples (`examples/`)**  
- `basic_run.py` → minimal runnable demo with dummy LLM  
- `openai_run.py` → minimal real LLM integration example (OpenAI; API key required)

**Note**  
EBA Core does **not** deduplicate tasks by text, allowing repetition when the agent judges it useful.

## Dependencies

EBA Core is designed with **minimal runtime dependencies**.

Core modules currently rely primarily on the Python standard library, with optional lightweight packages used for planned or experimental features. Full list in `pyproject.toml`.

Note: Additional dependencies may be introduced in future releases to support embeddings, tool execution, or external memory backends.

## Acknowledgements

This project has been developed with the assistance of AI-based coding tools.
All design decisions and final implementations are reviewed and owned by the maintainer.

## License

MIT License — see the LICENSE file for details.
