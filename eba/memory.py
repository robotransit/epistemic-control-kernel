```
python
from datetime import datetime
from typing import Dict, Optional, Any

from .task import TaskState

class WorldModel:
    """
    Minimal in-memory store for task history — no vector DB required yet.

    Maps task_id to a dict of task details (text, prediction, outcome, etc.).
    Note: Records latest state only (overwrites previous entry for the same task_id).
    """

    def __init__(self):
        self.tasks: Dict[str, Dict[str, Any]] = {}

    def record(
        self,
        task_id: str,
        task_text: str,
        prediction: str,
        outcome: str,
        success: bool,
        feedback: str,
        state: TaskState = TaskState.CREATED,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Record a task’s execution data.

        All core fields are stored as provided; pass None for unknown values.
        Optional metadata may be supplied for provenance or annotations.
        Optional state records the task's lifecycle position.
        """
        entry = {
            "task": task_text,
            "state": state.value,  # "created", "predicted", etc.
            "prediction": prediction,
            "outcome": outcome,
            "success": success,
            "feedback": feedback,
            "timestamp": datetime.utcnow().isoformat(),
        }

        if metadata is not None:
            if not isinstance(metadata, dict):
                raise TypeError("metadata must be a dict if provided")
            entry["metadata"] = dict(metadata)  # shallow copy

        self.tasks[task_id] = entry

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
