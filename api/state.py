import asyncio
from typing import Any

TASKS: dict[str, dict[str, Any]] = {}

def create_task(task_id: str) -> asyncio.Queue:
    q: asyncio.Queue = asyncio.Queue()
    TASKS[task_id] = {"queue": q, "done": False, "report": None}
    return q

