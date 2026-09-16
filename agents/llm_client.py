"""统一 LLM 调用客户端，直接使用 httpx 调用 OpenAI 兼容接口。"""
import os
import httpx

async def chat(
    prompt: str,
    system: str = "你是资深 SRE 根因分析助手。",
    timeout: int = 20,
    model_env: str = "LLM_MODEL",   # 读哪个环境变量取模型名
) -> str | None:
    """
    调用 LLM，返回回复文本。失败返回 None（由调用方走回退逻辑）。
    model_env 指定从哪个环境变量读取模型名，默认 LLM_MODEL。
    各 Agent 可传入专属环境变量名实现多模型路由：
      Router   → model_env="LLM_MODEL_ROUTER"
      Summarize→ model_env="LLM_MODEL_SUMMARIZE"
      FollowUp → model_env="LLM_MODEL_FOLLOWUP"
    """
    key = os.environ.get("OPENAI_API_KEY", "")
    base = os.environ.get("OPENAI_BASE_URL", "")
    # 优先读专属变量，回退到通用 LLM_MODEL
    model = os.environ.get(model_env) or os.environ.get("LLM_MODEL", "")

    if not key or not base or not model:
        return None

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            r = await client.post(
                f"{base.rstrip('/')}/chat/completions",
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system},
                        {"role": "user", "content": prompt},
                    ],
                },
            )
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        import sys
        print(f"[LLM ERROR] {type(e).__name__}: {str(e)[:500]}", flush=True, file=sys.stderr)
        return None
