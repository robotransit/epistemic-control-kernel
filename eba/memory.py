```
python
from datetime import datetime
from typing import Dict, Optional, Any, List

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
            "timestamp": datetime.utcnow(),  # Store datetime object (serialize at boundaries)
        }

        if metadata is not None:
            if not isinstance(metadata, dict):
                raise TypeError("metadata must be a dict if provided")
            entry["metadata"] = dict(metadata)  # shallow copy

        self.tasks[task_id] = entry

    def get(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve data for a specific task by ID, or None if not found."""
        entry = self.tasks.get(task_id)
        if entry is not None:
            # Serialize timestamp for output
            entry = dict(entry)  # shallow copy
            entry["timestamp"] = entry["timestamp"].isoformat()
        return entry

    def get_recent(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Return the most recent tasks (sorted by timestamp descending)."""
        sorted_tasks = sorted(
            self.tasks.values(),
            key=lambda e: e["timestamp"],
            reverse=True
        )
        recent = sorted_tasks[:limit]
        # Serialize timestamps for output
        return [dict(t, timestamp=t["timestamp"].isoformat()) for t in recent]

    def get_similar(
        self,
        task_text: str,
        threshold: float = 0.7,
        limit: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Return tasks with cosine similarity above threshold to the given task_text.

        Placeholder similarity function — future: use real embeddings.
        """
        similar = []
        for entry in self.tasks.values():
            past_text = entry["task"]
            union = set(task_text.split()) | set(past_text.split())
            if not union:
                continue  # Avoid division by zero
            intersection = set(task_text.split()) & set(past_text.split())
            sim = len(intersection) / len(union)
            if sim >= threshold:
                similar.append(entry)

        # Sort by timestamp descending
        similar.sort(key=lambda e: e["timestamp"], reverse=True)
        recent = similar[:limit]
        # Serialize timestamps for output
        return [dict(t, timestamp=t["timestamp"].isoformat()) for t in recent]

    # Deprecated: use all_tasks() instead
    # def get_entries(self) -> Dict[str, Dict[str, Any]]:
    #     return dict(self.tasks)

    def all_tasks(self) -> Dict[str, Dict[str, Any]]:
        """Return a copy of the entire task history with serialized timestamps."""
        return {k: dict(v, timestamp=v["timestamp"].isoformat()) for k, v in self.tasks.items()}

    def __len__(self) -> int:
        """Number of recorded tasks."""
        return len(self.tasks)

    def __repr__(self) -> str:
        return f"WorldModel({len(self)} tasks recorded)"
```
