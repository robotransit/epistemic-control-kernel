```
python
from collections import deque
from typing import Dict, List, Optional


class TaskQueue:
    """
    Bounded task queue using deque for efficient operations.

    Automatically drops oldest tasks when exceeding max_size.
    """

    def __init__(self, max_size: int = 50):
        """
        Initialize with a maximum size limit.

        Args:
            max_size: Maximum number of tasks allowed (default 50).
        """
        self.queue: deque[Dict] = deque()
        self.max_size = max_size

    def push(self, task: Dict) -> None:
        """Add a task to the end; drop oldest if over max_size."""
        self.queue.append(task)
        if len(self.queue) > self.max_size:
            self.queue.popleft()

    def pop(self) -> Optional[Dict]:
        """Remove and return the oldest task, or None if empty."""
        return self.queue.popleft() if self.queue else None

    def clear(self) -> None:
        """Remove all tasks."""
        self.queue.clear()

    def __len__(self) -> int:
        """Current number of tasks in queue."""
        return len(self.queue)

    def as_list(self) -> List[Dict]:
        """Return a copy of all tasks as a list."""
        return list(self.queue)

    def __repr__(self) -> str:
        return f"TaskQueue({len(self)}/{self.max_size} tasks)"
```
