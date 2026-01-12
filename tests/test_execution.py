```
python
from eba.execution import execute_task

def dummy_llm(prompt: str) -> str:
    """Dummy LLM returning messy whitespace to test normalization."""
    return "  LLM   response  with \n extra   spaces  "

def test_execute_task_without_tools_calls_llm():
    outcome = execute_task("some task", dummy_llm, use_tools=False)
    assert outcome == "LLM response with extra spaces"  # Proves normalization works

def test_execute_task_with_calculator_tool():
    outcome = execute_task("CALC: 2 + 3", dummy_llm, use_tools=True)
    assert "Calculation result: 5" in outcome

def test_execute_task_with_calculator_error():
    outcome = execute_task("CALC: 1 / 0", dummy_llm, use_tools=True)
    assert "Calculation failed" in outcome

def test_execute_task_with_tools_falls_back_to_llm():
    outcome = execute_task("Just a normal task", dummy_llm, use_tools=True)
    assert outcome == "LLM response with extra spaces"  # Still normalized
```
