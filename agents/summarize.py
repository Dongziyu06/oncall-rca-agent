import json
from agents.llm_client import chat

def _strip_frontmatter(text: str) -> str:
    text = text.strip()
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            text = text[end + 3:].lstrip("\n")
    return text.strip()

def _template(route: dict, evidence: dict) -> str:
    kind = route.get("fault_type", "unknown")
    causes = {
        "cpu": "CPU 使用率持续过高",
        "oom": "容器可能发生内存耗尽",
        "crashloop": "Pod 可能处于 CrashLoopBackOff",
        "timeout": "服务或依赖存在响应超时",
    }
    excerpts = evidence.get("runbook") or []
    refs = "\n".join(
        f"- **{x.get('id', 'runbook')}**：{_strip_frontmatter(x.get('text', ''))[:400]}"
        for x in excerpts
    ) or "- 暂无匹配 Runbook"
    return (
        f"# RCA 报告\n\n"
        f"- **故障类型**：{kind}\n"
        f"- **推测根因**：{causes.get(kind, '无法从告警确定根因')}\n"
        f"- **置信度**：0.72\n\n"
        f"## 证据链\n\n"
        f"- 指标：`{evidence.get('metric')}`\n"
        f"- K8s：`{evidence.get('k8s')}`\n\n"
        f"## 参考 Runbook 摘录\n\n{refs}\n\n"
        f"## 建议\n\n"
        f"1. 核对指标、Pod 状态和事件。\n"
        f"2. 任何变更必须经过人工审批。"
    )

async def build_report(route: dict, evidence: dict) -> str:
    kind = route.get("fault_type", "unknown")
    excerpts = evidence.get("runbook") or []
    clean = [
        {"id": x.get("id", "runbook"), "text": _strip_frontmatter(x.get("text", ""))[:600]}
        for x in excerpts
    ]
    # Runbook 摘录只取前 200 字，去掉页眉重复行（网页抓取残留）
    def _clean_rb(text: str) -> str:
        lines = [l for l in text.splitlines() if l.strip()]
        # 去掉前两行重复标题（Prometheus Operator 页面抓取残留）
        if len(lines) > 3 and lines[0].strip() == lines[1].strip():
            lines = lines[2:]
        return " ".join(lines)[:200]

    refs = "\n".join(f"- **{x['id']}**：{_clean_rb(x['text'])}" for x in clean) or "- 暂无匹配 Runbook"

    prompt = (
        f"故障类型：{kind}\n\n"
        f"证据数据：\n{json.dumps({'metric': evidence.get('metric'), 'k8s': evidence.get('k8s'), 'runbook': clean}, ensure_ascii=False, default=str)[:2000]}\n\n"
        f"请生成结构清晰的中文 RCA 报告，包含：\n"
        f"1. 推断根因（结合证据，不要编造）\n"
        f"2. 置信度评估（0-1 数字）\n"
        f"3. 具体建议（高风险操作注明需人工审批）\n"
        f"要求：全部使用中文，技术术语（PromQL、kubectl 命令等）保留英文原文。\n"
        f"使用 Markdown 格式。"
    )

    # Include forensic evidence when available, bounded for prompt safety.
    forensic_parts = []
    if evidence.get("logs"):
        forensic_parts.append(f"容器前次运行日志（截断 1500 字）：{str(evidence.get('logs'))[:1500]}")
    if evidence.get("events"):
        forensic_parts.append(f"Pod Events（最近 10 条）：{str(evidence.get('events'))[:1000]}")
    if forensic_parts:
        prompt += "\n\n" + "\n".join(forensic_parts)
    prompt += "\n若日志中出现 panic/error/exit code/signal，必须在根因分析中引用原文，不要忽略。"
    reply = await chat(prompt=prompt, timeout=60, model_env="LLM_MODEL_SUMMARIZE")  # 高复杂度：深度推理模型
    if reply:
        # LLM 已消化 Runbook 知识，不再重复贴原文（避免中英混杂）
        # 只在底部列出参考来源名称，不展示原文内容
        source_list = "\n".join(f"- `{x['id']}`" for x in clean) or "- 暂无"
        return f"# RCA 报告\n\n{reply}\n\n---\n> 📚 参考知识库：{', '.join(x['id'] for x in clean)}"

    evidence_clean = dict(evidence)
    evidence_clean["runbook"] = clean
    return _template(route, evidence_clean)

