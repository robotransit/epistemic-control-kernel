"""
Prompt templates and formatting utilities for EBA LLM calls.

All prompts are defined as constants here for easy maintenance and testing.
"""

INITIAL_TASK_PROMPT_TEMPLATE = """
Generate the very first concrete task to start pursuing the objective: {objective}

Return a concise, actionable task string only.
"""

SUBTASK_GENERATION_PROMPT = """
You are an autonomous agent working toward the objective: "{objective}"

Given the completed task: "{current_task}"

Generate 0-5 concise subtasks that directly advance the objective.
If no further subtasks are needed (goal achieved or task complete), return an empty list.
Stay strictly on-topic; subtasks must align with the objective.

Return ONLY a valid JSON array of strings, e.g.:
["Subtask 1", "Subtask 2"]
or
[]
"""

# memory_context may be empty; it is informational only
PREDICTION_PROMPT_TEMPLATE = """
{memory_context}

Predict the expected outcome for this task toward the objective '{objective}'.

Task: {task_text}

Return ONLY a brief string prediction of the result.
"""

CRITIC_EVALUATION_PROMPT = """
Evaluate the result against the task and objective.

Task: {task_text}
Prediction: {prediction}
Result: {result}
Objective: {objective}

Return ONLY valid JSON:
{{
  "success": true/false,
  "feedback": "brief explanation"
}}

Respond with true if the result meaningfully advances the objective.
"""

GOAL_ACHIEVED_PROMPT = """
Did this result achieve the final objective?

Objective: {objective}
Latest result: {result}

Answer ONLY "YES" or "NO".
"""

PRIORITIZATION_PROMPT = """
Prioritize the following tasks by relevance and urgency to the objective: "{objective}"

Tasks:
{task_list_json}

Return ONLY a JSON array of the task texts in prioritized order.
Example: ["Highest priority", "Next", ...]
"""

def format_prompt(template: str, **kwargs) -> str:
    """Format a prompt template with variables."""
    return template.format(**kwargs)
