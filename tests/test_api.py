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
    # ForensicsAgent 只对 crashloop/oom 触发；HighCPU 走 cpu 路径，不触发
    assert 'Router' in nodes and 'PlannerAgent' in nodes
    assert nodes.index('Router') < nodes.index('PlannerAgent')
    for optional in ('MetricAgent', 'K8sAgent', 'ForensicsAgent'):
        if optional in nodes:
            assert nodes.index('PlannerAgent') < nodes.index(optional)
    for name in ('RunbookAgent', 'Summarize', 'FollowUpAgent', 'Report'):
        assert name in nodes
    assert nodes.index('PlannerAgent') < nodes.index('RunbookAgent') < nodes.index('Summarize') < nodes.index('FollowUpAgent') < nodes.index('Report')
    # LLM 生成时报告含"参考知识库"，模板回退时含"Runbook"，两者都算通过
    assert 'Runbook' in TASKS[tid]['report'] or '参考知识库' in TASKS[tid]['report'] or 'RCA' in TASKS[tid]['report']



