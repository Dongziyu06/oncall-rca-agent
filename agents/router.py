from agents.llm_client import chat  # 唯一允许的 LLM 调用方式，禁止使用 litellm

KEYWORDS = {
    "cpu": ["cpu", "highcpu", "throttle"],
    "oom": ["oom", "memory", "oomkilled"],
    "crashloop": ["crash", "crashloop", "restart"],
    "timeout": ["timeout", "latency", "slow"],
}

def _fallback(text: str) -> str:
    text = text.lower()
    return next((k for k, ws in KEYWORDS.items() if any(w in text for w in ws)), "unknown")

async def classify_alert(alertname: str, description: str = "") -> dict:
    text = f"{alertname} {description}"
    reply = await chat(
        prompt=f"告警名：{alertname}\n描述：{description}\n\n从 cpu/oom/crashloop/timeout/unknown 中选一个最匹配的故障类型，只返回类型名，不要其他内容。",
        system="你是 SRE 故障分类助手，只输出故障类型名，不要解释。",
        timeout=15,
        model_env="LLM_MODEL_ROUTER",   # 使用轻量快速模型
    )
    if reply:
        value = reply.strip().lower().split()[0].strip("`.,。")
        if value in {"cpu", "oom", "crashloop", "timeout", "unknown"}:
            return {"error": None, "data": {"fault_type": value, "method": "llm"}}

    return {"error": None, "data": {"fault_type": _fallback(text), "method": "keyword_fallback"}}
