# eba-core

Enhanced BabyAGI: A perceptually self-regulating autonomous agent with predictive foresight and drift detection.

EBA Core is an early-stage, framework-agnostic reliability kernel for autonomous agents.  
It focuses on explicit prediction–execution–evaluation loops, conservative defaults, and first-class drift handling.

## Current Status (v0.1.x)

Implemented & stable components:
- Agent loop orchestration (agent.py)
- Prediction-before-execution discipline
- Modular task generation and execution seams
- Critic evaluation pipeline with consensus and verification hooks
- Drift monitoring (perceptual, streak, numeric feasibility bias)
- Safe JSON parsing and pessimistic fallbacks
- Typed config and minimal memory store

Designed / Planned (not yet implemented):
- Embedding-based proactive task filtering
- Full tool integration (execution.py seam is ready)
- External vector memory
- Multi-model or ensemble critics
- Adaptive threshold tuning

The focus right now is on reliability first: explicit phases, no silent hallucinations, clear halting conditions, and modular seams for future extensions.

## Architecture Overview

EBA Core separates cognition from execution:

Pure cognitive functions (stateless, deterministic given LLM):
- prediction.generate_prediction
- task_generation.generate_subtasks
- execution.execute_task

Stateful control & safety layer:
- EBACoreAgent (main loop)
- WorldModel (task history & annotations)
- DriftMonitor (error tracking & recovery)

This design allows EBA Core to plug into any LLM stack (raw APIs, LangChain, LangGraph, etc.) without coupling to a specific framework.

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
See examples/ for progressively richer integrations (coming soon).
### How to Run (Local / Minimal Setup)

```
git clone https://github.com/robotransit/eba-core.git
cd eba-core
pip install -e .
```
Then run your own script using the stub example above.

## Project Structure

- eba/ — core package with modules:
  - agent.py → main loop orchestration
  - config.py → typed thresholds & limits
  - prompts.py → LLM prompt templates
  - utils.py → safe helpers (parsing, numeric checks, etc.)
  - queue.py → bounded task queue
  - memory.py → task history store with metadata
  - drift.py → multi-level drift detection
  - critic.py → evaluation with consensus & verification
  - prediction.py → pure prediction generation
  - task_generation.py → pure subtask generation
  - execution.py → execution seam (LLM-only placeholder for now)

- examples/ → runnable demos (coming soon)

Note: EBA Core does not deduplicate tasks by text (allows repetition if desired).

## Dependencies

EBA Core currently has minimal runtime dependencies.

Note: Additional dependencies may be introduced in future releases to support embeddings, tool execution, or external memory backends.

## License

MIT License — see the LICENSE file for details.
