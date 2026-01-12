"```"
"python"
# examples/openai_run.py
# Minimal real LLM integration example using OpenAI

# IMPORTANT:
# This example uses a real LLM and will incur API costs.
# Ensure OPENAI_API_KEY is set in your environment before running.

import os
import logging
from openai import OpenAI

from eba.agent import EBACoreAgent
from eba.config import EBACoreConfig

# Fail-fast: check API key early
if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY not set in environment. Please set it before running.")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("eba-openai-example")

client = OpenAI()  # Create once; reuse across all LLM calls

# Note: EBA Core treats this as a black-box text-in / text-out LLM.
# No tool calls, function calling, or structured outputs are assumed here.
def llm_call(prompt: str) -> str:
    """Simple OpenAI chat completion wrapper."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # or "gpt-4o", "gpt-3.5-turbo" (choose based on access/availability)
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=150,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        return "(LLM error - no response)"

# Create config (use defaults or customize)
config = EBACoreConfig(
    max_iterations=30,  # Short run for demo
    max_queue_size=50,
)

# Create agent
agent = EBACoreAgent(
    objective="Write a short poem about a curious robot exploring the stars.",
    llm_call=llm_call,
    config=config,
)

# Optional: seed with a custom initial task
# agent.seed("Start by imagining the robot's first thought upon seeing the night sky.")

print("Starting real LLM EBA run...")
agent.run()
print("Run completed.")
"```"
