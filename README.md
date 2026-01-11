# eba-core

Enhanced BabyAGI: A perceptually self-regulating autonomous agent with predictive foresight and drift detection.

EBA builds on the classic BabyAGI concept by adding strong safeguards and self-correction mechanisms to prevent goal drift, off-topic task generation, and unrealistic predictions — making it more reliable for real-world autonomous agent experiments.

## Key Enhancements over original BabyAGI

- **Multi-level drift detection** — monitors goal similarity, perceptual/numeric prediction errors, config tampering, and drift streaks with automatic partial/complete resets.
- **Proactive task topic filtering** — every generated subtask is checked against objective embedding similarity before being added.
- **Critic with consensus & verification** — dual critic evaluations (strict AND logic) + optional tool result checks.
- **Prediction-before-execution discipline** — generates explicit outcome predictions stored before running each task.
- **Numeric feasibility bias adaptation** — dynamically adjusts similarity thresholds based on historical numeric task success.
- **Robust JSON handling** — improved parsing with fallbacks to handle LLM output fragility.

## Features

- Goal-directed task decomposition and prioritization
- Semantic embeddings for similarity checks (using all-MiniLM-L6-v2)
- Integration-ready for LangChain agents and tools
- Modular structure for easy extension (drift, critic, queue, etc.)

## Installation

```bash
# Clone the repo
git clone https://github.com/robotransit/eba-core.git
cd eba-core

# Install dependencies (editable mode recommended for development)
pip install -e .
```

(Requires Python 3.10+)

## Quick Start

See the [examples/basic_run.py](examples/basic_run.py) for a simple runnable demo (to be added soon).

```python
# Example usage (once implemented)
from eba.agent import run_eba

objective = "Your main goal here"
run_eba(objective, max_iterations=50)
```

## Project Structure

- `eba/` — core package with modules:
  - `agent.py` → main loop
  - `drift.py` → drift detection & guards
  - `critic.py` → evaluation logic
  - `prediction.py` → pre-execution predictions
  - `task_generation.py` → task creation with filtering
  - `queue.py` → task management
  - `models.py` → data structures
  - `prompts.py` → LLM templates
  - `utils.py` → helpers (JSON, embeddings, etc.)
  - `config.py` → constants & thresholds
  - `execution.py` → task running

- `examples/` → runnable demos (coming soon)

## License

MIT License — see the [LICENSE](LICENSE) file for details.


# eba-core
This is a test header
- This is a test bullet
This is plain text line
""python print"Hello, world!" ""


