from __future__ import annotations

import asyncio
import uuid
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from agents.chat_agent import run_chat, SESSIONS

router = APIRouter()
QUEUES: dict[str, asyncio.Queue] = {}

class ChatRequest(BaseModel):
    session_id: str | None = None
    message: str

async def _run(session_id: str, message: str) -> None:
    queue = QUEUES[session_id]
    async def emit(event: dict) -> None:
        await queue.put(event)
    try:
        await run_chat(session_id, message, emit)
    except Exception as exc:
        await queue.put({'type': 'answer', 'content': f'聊天处理失败：{str(exc)[:500]}'})
    await queue.put({'type': 'done'})

@router.post('/chat')
async def create_chat(payload: ChatRequest):
    session_id = payload.session_id or str(uuid.uuid4())
    QUEUES.setdefault(session_id, asyncio.Queue())
    SESSIONS.setdefault(session_id, [])
    asyncio.create_task(_run(session_id, payload.message))
    return {'session_id': session_id, 'status': 'accepted'}

@router.get('/chat/{session_id}/stream')
async def chat_stream(session_id: str):
    queue = QUEUES.setdefault(session_id, asyncio.Queue())
    async def events():
        while True:
            try:
                event = await asyncio.wait_for(queue.get(), timeout=30)
                import json
                yield f'data: {json.dumps(event, ensure_ascii=False, default=str)}\n\n'
                if event.get('type') == 'done':
                    break
            except asyncio.TimeoutError:
                yield ': keep-alive\n\n'
    return StreamingResponse(events(), media_type='text/event-stream')
