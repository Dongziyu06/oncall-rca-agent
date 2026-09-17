import pytest
from tools.common import bounded
from tools.prometheus_tools import query_metric
from tools.k8s_tools import get_pod_status, get_pod_logs, get_events
from tools.loki_tools import query_logs
from agents.router import classify_alert


@pytest.mark.asyncio
async def test_router_all_types():
    for name, expected in [
        ("HighCPU", "cpu"),
        ("OOMKilled", "oom"),
        ("CrashLoopBackOff", "crashloop"),
        ("RequestTimeout", "timeout"),
        ("SomethingElse", "unknown"),
    ]:
        assert (await classify_alert(name))["data"]["fault_type"] == expected


@pytest.mark.asyncio
async def test_mock_fallbacks(monkeypatch):
    # 强制断开真实后端，验证 mock 回退路径
    monkeypatch.setenv("PROMETHEUS_URL", "http://localhost:19090")  # 不存在的端口
    monkeypatch.setenv("LOKI_URL", "http://localhost:13100")
    monkeypatch.delenv("KUBECONFIG", raising=False)
    assert (await query_metric("up"))["data"]["source"] == "mock-prometheus"
    assert (await get_pod_status())["data"]["source"] == "mock-kubernetes"
    assert (await get_pod_logs())["data"]["source"] == "mock-kubernetes"
    assert (await get_events())["data"]["source"] == "mock-kubernetes"
    assert (await query_logs("demo"))["data"]["source"] == "mock-loki"


def test_bounded_boundaries():
    assert len(bounded("x" * 2000)) == 2000
    assert len(bounded("x" * 2001)) == 2000
    assert bounded("x" * 2001).endswith("[TRUNCATED]")


# ── LLM path tests（mock llm_client.chat，不依赖真实 API）─────────────

@pytest.mark.asyncio
async def test_router_llm(monkeypatch):
    """Router 通过 llm_client.chat 分类，mock 返回 'timeout'。"""
    import agents.router as r

    async def fake_chat(prompt, system="", timeout=20, model_env="LLM_MODEL_ROUTER"):
        return "timeout"

    # 必须 patch 模块内已绑定的 chat 引用
    monkeypatch.setattr(r, "chat", fake_chat)
    monkeypatch.setenv("OPENAI_API_KEY", "test")
    monkeypatch.setenv("LLM_MODEL_ROUTER", "mock-model")
    out = await r.classify_alert("WeirdAlert", "dependency issue")
    assert out["data"] == {"fault_type": "timeout", "method": "llm"}


@pytest.mark.asyncio
async def test_summarize_llm(monkeypatch):
    """Summarize 通过 llm_client.chat 生成报告，mock 返回含置信度的文本。"""
    import agents.llm_client as lc
    from agents import summarize

    async def fake_chat(prompt, system="", timeout=60, model_env="LLM_MODEL_SUMMARIZE"):
        return "根因：CPU 高负载。置信度：0.8。建议：检查 limits。"

    monkeypatch.setattr(lc, "chat", fake_chat)
    monkeypatch.setenv("OPENAI_API_KEY", "test")
    monkeypatch.setenv("LLM_MODEL_SUMMARIZE", "mock-model")
    out = await summarize.build_report(
        {"fault_type": "cpu"},
        {"metric": {"value": 99}, "k8s": {}, "runbook": []},
    )
    assert "RCA 报告" in out and "置信度" in out
