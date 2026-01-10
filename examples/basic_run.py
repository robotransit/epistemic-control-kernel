# examples/basic_run.py
# Simple runnable demo of EBA (Enhanced BabyAGI)

```python
from eba.agent import run_eba  # Will import from your package once installable

if __name__ == "__main__":
    objective = "Your main goal here - replace this string!"
    print(f"Starting EBA with objective: {objective}")
    run_eba(objective, max_iterations=20)  # Small number for quick testing
```
