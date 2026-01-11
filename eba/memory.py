```
python
from datetime import datetime
from typing import Dict, Optional, Anyclass WorldModel:
    """
    Minimal in-memory store for task history — no vector DB required yet.Maps task_id to a dict of task details (text, prediction, outcome, etc.).
"""

def __init__(self):
    self.tasks: Dict[str, Dict[str, Any]] = {}

def record(
    self,
    task_id: str,
    task_text: str,
    prediction: Optional[str] = None,
    outcome: Optional[str] = None,
    success: Optional[bool] = None,
    feedback: Optional[str] = None,
) -> None:
    """
    Record (or update) a task's execution data.

    All fields except task_id and task_text are optional.
    """
    self.tasks[task_id] = {
        "task": task_text,
        "prediction": prediction,
        "outcome": outcome,
        "success": success,
        "feedback": feedback,
        "timestamp": datetime.utcnow().isoformat(),
    }

def get(self, task_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve data for a specific task by ID, or None if not found."""
    return self.tasks.get(task_id)

def all_tasks(self) -> Dict[str, Dict[str, Any]]:
    """Return a copy of the entire task history."""
    return dict(self.tasks)

def __len__(self) -> int:
    """Number of recorded tasks."""
    return len(self.tasks)

def __repr__(self) -> str:
    return f"WorldModel({len(self)} tasks recorded)"
  ```

