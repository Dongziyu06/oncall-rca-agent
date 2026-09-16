import re, json
from agents.llm_client import chat

FALLBACK_QUERIES = {
    "cpu": [
        {"type": "prometheus", "query": "sum(rate(container_cpu_usage_seconds_total[5m])) by (pod)", "purpose": "容器 CPU 使用率"},
        {"type": "prometheus", "query": "rate(container_cpu_cfs_throttled_seconds_total[5m])", "purpose": "CPU throttling"},
        {"type": "kubectl", "command": "kubectl top pod -A", "purpose": "实时资源快照"},
        {"type": "kubectl", "command": "kubectl describe pod <pod> -n <ns>", "purpose": "资源配置和事件"},
    ],
    "oom": [
        {"type": "prometheus", "query": "container_memory_working_set_bytes", "purpose": "内存使用量"},
        {"type": "prometheus", "query": "kube_pod_container_status_last_terminated_reason", "purpose": "终止原因"},
        {"type": "kubectl", "command": "kubectl logs --previous <pod>", "purpose": "崩溃前日志"},
        {"type": "kubectl", "command": "kubectl describe pod <pod>", "purpose": "OOMKilled 事件"},
    ],
    "crashloop": [
        {"type": "kubectl", "command": "kubectl logs --previous <pod>", "purpose": "崩溃前日志"},
        {"type": "kubectl", "command": "kubectl describe pod <pod>", "purpose": "退出码和事件"},
        {"type": "kubectl", "command": "kubectl get events -n <ns>", "purpose": "近期 Pod 事件"},
    ],
    "timeout": [
        {"type": "prometheus", "query": "histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))", "purpose": "P99 延迟"},
        {"type": "prometheus", "query": "rate(http_requests_total{status=~'5..'}[5m])", "purpose": "错误率"},
        {"type": "kubectl", "command": "kubectl logs <pod> --tail=100", "purpose": "最新日志"},
    ],
    "unknown": [
        {"type": "kubectl", "command": "kubectl get events -A --sort-by='.lastTimestamp'", "purpose": "全局最新事件"},
        {"type": "kubectl", "command": "kubectl get pods -A | grep -v Running", "purpose": "异常 Pod 列表"},
        {"type": "kubectl", "command": "kubectl describe pod <pod> -A", "purpose": "Pod 详细状态"},
    ],
}

def parse_confidence(report_text: str) -> float:
    """从报告文本中提取置信度数值，支持多种格式。"""
    patterns = [
        r"置信度\s*(?:[：:]\s*|\*\*\s*[：:]?\s*)\**([01](?:\.\d+)?)",
        r"confidence\**\s*(?:[=：:]\s*)([01](?:\.\d+)?)",
        r"([01]\.\d+)\s*/\s*1(?:\.0)?",
    ]
    for p in patterns:
        m = re.search(p, report_text, re.I)
        if m:
            return float(m.group(1))
    return 0.5  # 解析失败 → 默认不触发追问

def _fallback(fault_type: str, confidence: float) -> dict:
    q = FALLBACK_QUERIES.get(fault_type, FALLBACK_QUERIES["unknown"])
    return {
        "confidence": confidence,
        "needs_follow_up": confidence < 0.5,
        "missing_evidence": [x.get("query") or x.get("command") for x in q[:3]],
        "suggested_queries": q,
        "priority": "high" if confidence < 0.3 else "medium",
    }

async def generate_follow_up(fault_type: str, evidence: dict, report_text: str) -> dict:
    """解析报告置信度，若 < 0.5 则用 LLM 生成补充查询计划。"""
    confidence = parse_confidence(report_text)
    if confidence >= 0.5:
        return {"confidence": confidence, "needs_follow_up": False,
                "missing_evidence": [], "suggested_queries": [], "priority": "low"}

    # 尝试用 LLM 生成个性化追问计划
    prompt = (
        f"故障类型：{fault_type}\n"
        f"当前证据：{json.dumps(evidence, ensure_ascii=False, default=str)[:1500]}\n"
        f"报告摘要：{report_text[:1000]}\n\n"
        f"当前证据不足，请给出 3-5 条可立即执行的补充查询，以 JSON 格式返回，字段为：\n"
        f"- missing_evidence: list[str]（缺失的证据名称）\n"
        f"- suggested_queries: list of {{type, query或command, purpose}}\n"
        f"- priority: high/medium/low\n"
        f"只输出 JSON，不要其他内容。"
    )
    reply = await chat(prompt=prompt, system="你是 SRE 证据规划助手，只输出合法 JSON。", timeout=30, model_env="LLM_MODEL_FOLLOWUP")  # 中复杂度：结构化输出模型
    if reply:
        try:
            raw = re.sub(r"^```json\s*|\s*```$", "", reply.strip())
            data = json.loads(raw)
            data.update({"confidence": confidence, "needs_follow_up": True})
            return data
        except Exception:
            pass

    return _fallback(fault_type, confidence)

def format_follow_up(plan: dict) -> str:
    """将追问计划格式化为 Markdown。"""
    lines = [
        "\n---\n## 🔍 主动追问：需要补充的证据\n",
        f"> 当前置信度 **{plan['confidence']:.2f}**，证据不足，"
        f"建议在执行任何变更前先补充以下信息：\n",
        "### 缺失证据",
    ]
    lines += [f"- {x}" for x in plan.get("missing_evidence", [])]
    lines += ["\n### 建议查询", "| 类型 | 查询/命令 | 目的 |", "|------|-----------|------|"]
    for q in plan.get("suggested_queries", []):
        cmd = q.get("query") or q.get("command", "")
        lines.append(f"| {q.get('type', '-')} | `{cmd}` | {q.get('purpose', '')} |")
    return "\n".join(lines)
