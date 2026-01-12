```
python
# examples/basic_run.py
# Simple runnable demo of EBA (Enhanced BabyAGI)

# IMPORTANT NOTE:
# This example demonstrates the EBA control loop only.
# The dummy LLM does not perform reasoning or task execution — it returns fixed responses.

from eba.agent import EBACoreAgent

def dummy_llm_call(prompt: str) -> str:
    """
    Intentionally dumb LLM that returns fixed, predictable responses for demo purposes.
    No real reasoning, no prompt parsing — just fixed outputs to show the loop.
    """
    # Print prompt for observability
    print("\n=== DUMMY LLM PROMPT ===")
    print(prompt)
    print("======================\n")

    # Fixed responses (always the same, no branching)
    return "This is a fixed dummy response."

if __name__ == "__main__":
    objective = "Demonstrate the EBA control loop safely with a fixed dummy LLM"

    print(f"Starting EBA demo with objective: {objective}")

    # Create the agent with dummy LLM
    agent = EBACoreAgent(
        objective=objective,
        llm_call=dummy_llm_call,
    )

    # Seed with an optional initial task (or let it generate one)
    # agent.seed("Begin by exploring the objective in detail.")

    # Run the agent until the task queue empties or max iterations is reached.
    agent.run()

    print("Demo run completed.")
```
