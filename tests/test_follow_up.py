import pytest
from agents.follow_up import parse_confidence,generate_follow_up

def test_parse_confidence_formats():
 assert parse_confidence('置信度：0.35')==0.35
 assert parse_confidence('confidence: 0.45 / 1.0')==0.45
 assert parse_confidence('confidence: 0.72')==0.72
 assert parse_confidence('no confidence')==0.5
@pytest.mark.asyncio
async def test_followup_thresholds(monkeypatch):
 monkeypatch.delenv('OPENAI_API_KEY',raising=False);monkeypatch.delenv('LLM_MODEL',raising=False)
 low=await generate_follow_up('cpu',{},'置信度：0.35'); high=await generate_follow_up('cpu',{},'置信度：0.72')
 assert low['needs_follow_up'] is True and len(low['suggested_queries'])>=3
 assert high['needs_follow_up'] is False
@pytest.mark.asyncio
async def test_followup_llm_mock(monkeypatch):
 import agents.follow_up as f
 class M: content='{"missing_evidence":["metric"],"suggested_queries":[{"type":"prometheus","query":"up","purpose":"check"}],"priority":"high"}'
 class C: message=M()
 class R: choices=[C()]
 async def fake(**kwargs): return R()
 monkeypatch.setattr(f,'acompletion',fake);monkeypatch.setenv('OPENAI_API_KEY','x');monkeypatch.setenv('LLM_MODEL','mock')
 x=await f.generate_follow_up('cpu',{},'confidence: 0.35'); assert x['needs_follow_up'] and x['priority']=='high'
