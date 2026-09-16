import pytest
from tools.common import bounded
from tools.prometheus_tools import query_metric
from tools.k8s_tools import get_pod_status,get_pod_logs,get_events
from tools.loki_tools import query_logs
from agents.router import classify_alert
@pytest.mark.asyncio
async def test_router_all_types():
    for name,expected in [('HighCPU','cpu'),('OOMKilled','oom'),('CrashLoopBackOff','crashloop'),('RequestTimeout','timeout'),('SomethingElse','unknown')]: assert (await classify_alert(name))['data']['fault_type']==expected
@pytest.mark.asyncio
async def test_mock_fallbacks():
    assert (await query_metric('up'))['data']['source']=='mock-prometheus'; assert (await get_pod_status())['data']['source']=='mock-kubernetes'; assert (await get_pod_logs())['data']['source']=='mock-kubernetes'; assert (await get_events())['data']['source']=='mock-kubernetes'; assert (await query_logs('demo'))['data']['source']=='mock-loki'
def test_bounded_boundaries():
    assert len(bounded('x'*2000))==2000; assert len(bounded('x'*2001))==2000; assert bounded('x'*2001).endswith('[TRUNCATED]')
import pytest
from agents import router, summarize
class Msg:
 content='timeout'
class Choice: message=Msg()
class Resp: choices=[Choice()]
@pytest.mark.asyncio
async def test_router_llm(monkeypatch):
 async def fake(**kwargs): return Resp()
 monkeypatch.setattr(router,'acompletion',fake); monkeypatch.setenv('OPENAI_API_KEY','test'); monkeypatch.setenv('LLM_MODEL','mock-model')
 out=await router.classify_alert('WeirdAlert','dependency issue'); assert out['data']=={'fault_type':'timeout','method':'llm'}
@pytest.mark.asyncio
async def test_summarize_llm(monkeypatch):
 async def fake(**kwargs): return Resp()
 monkeypatch.setattr(summarize,'acompletion',fake); monkeypatch.setenv('OPENAI_API_KEY','test'); monkeypatch.setenv('LLM_MODEL','mock-model')
 out=await summarize.build_report({'fault_type':'cpu'},{'metric':{'value':99},'k8s':{},'runbook':[]}); assert 'timeout' in out and 'RCA 报告' in out
