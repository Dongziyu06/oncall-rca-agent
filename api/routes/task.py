import asyncio, json
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from api.state import TASKS

router = APIRouter()

@router.get("/task/{task_id}/stream")
async def stream_task(task_id: str):
    task = TASKS.get(task_id)
    if not task:
        raise HTTPException(404, "task not found")
    async def events():
        while True:
            try:
                event = await asyncio.wait_for(task["queue"].get(), timeout=30)
                yield f"data: {json.dumps(event, ensure_ascii=False)}\n\n"
                if event.get("type") == "report":
                    break
            except asyncio.TimeoutError:
                yield ": keep-alive\n\n"
    return StreamingResponse(events(), media_type="text/event-stream")

