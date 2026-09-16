import asyncio, json, pytest
from fastapi.testclient import TestClient
from api.main import app
from api.state import create_task, TASKS
from agents.orchestrator import run_workflow
from api.models import AlertRequest

def test_health(): assert TestClient(app).get('/health').json()=={'status':'ok'}
@pytest.mark.asyncio
async def test_sse_event_order():
    tid='test-sse'; create_task(tid)
    await run_workflow(tid, AlertRequest.model_validate({'alerts':[{'labels':{'alertname':'HighCPU','service':'demo'},'annotations':{}}]}))
    events=[]
    while not TASKS[tid]['queue'].empty(): events.append(await TASKS[tid]['queue'].get())
    nodes=[e['node'] for e in events if e.get('type')=='progress']
    assert nodes==['Router','Router','MetricAgent','MetricAgent','K8sAgent','K8sAgent','RunbookAgent','RunbookAgent','Summarize','Summarize','FollowUpAgent','FollowUpAgent','Report']
    assert 'Runbook' in TASKS[tid]['report']


