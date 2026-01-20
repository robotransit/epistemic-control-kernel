# examples/openai_run.py
# Example demonstrating ECK with a real OpenAI-backed LLM

import os

from eck.agent import ECKAgent
from eck.config import ECKConfig
from openai import OpenAI


def openai_llm_call(prompt: str) -> str:
    """
    Minimal OpenAI-backed LLM call.
    Assumes OPENAI_API_KEY is set in the environment.
    """
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
    )

    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    objective = "Demonstrate the ECK control loop with a real LLM"

    print(f"Starting ECK demo with objective: {objective}")

    config = ECKConfig()

    agent = ECKAgent(
        objective=objective,
        llm_call=openai_llm_call,
        config=config,
    )

    agent.run()

    print("OpenAI-backed demo run completed.")

