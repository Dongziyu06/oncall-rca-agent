import asyncio, uuid
from fastapi import APIRouter
from api.models import AlertRequest, AlertResponse
from api.state import create_task, TASKS
from agents.orchestrator import run_workflow

router = APIRouter()

@router.post("/alert", response_model=AlertResponse)
async def receive_alert(payload: AlertRequest):
    task_id = str(uuid.uuid4())
    create_task(task_id)
    asyncio.create_task(run_workflow(task_id, payload))
    return AlertResponse(task_id=task_id, status="accepted")

