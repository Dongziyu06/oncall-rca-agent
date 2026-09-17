from typing import Any, TypedDict
import json
import re
from langgraph.graph import StateGraph, END
from api.models import AlertRequest
from api.state import TASKS
from agents.router import classify_alert
from tools.prometheus_tools import query_metric
from tools.k8s_tools import get_pod_status, get_pod_logs, get_events
from agents.runbook_agent import runbook_agent
from agents.summarize import build_report
from agents.follow_up import generate_follow_up, format_follow_up
from agents.llm_client import chat

class RCAState(TypedDict, total=False):
    task_id: str
    alert: dict[str, Any]
    route: dict[str, Any]
    evidence: dict[str, Any]
    report: str
    follow_up: dict[str, Any] | None
    baseline: bool
    plan: list[str]

async def _emit(task_id: str, node: str, status: str, **extra: Any) -> None:
    task = TASKS.get(task_id)
    if task and task.get('queue'):
        await task['queue'].put({'type': 'progress', 'node': node, 'status': status, **extra})

async def run_workflow(task_id: str, payload: AlertRequest) -> None:
    item = payload.alerts[0] if payload.alerts else None
    alert = {
        'alertname': item.labels.alertname if item else 'NaturalLanguage',
        'service': item.labels.service if item and item.labels.service else 'demo',
        'description': item.annotations.get('description', '') if item else (payload.description or ''),
    }
    baseline = bool(getattr(payload, 'baseline', False))

    async def router(s: RCAState) -> RCAState:
        await _emit(task_id, 'Router', 'started')
        result = await classify_alert(alert['alertname'], alert['description'])
        s['route'] = result.get('data', {})
        await _emit(task_id, 'Router', 'completed', result=s['route'])
        return s

    async def planner(s: RCAState) -> RCAState:
        await _emit(task_id, 'PlannerAgent', 'started')
        fault_type = s.get('route', {}).get('fault_type', 'unknown')
        description = alert.get('description', '')
        prompt = f"""故障类型：{fault_type}
告警描述：{description}

可用 Agent：
- MetricAgent：查询 Prometheus 指标（适用于 CPU/内存/网络性能问题）
- K8sAgent：查询 Pod 状态和重启次数（几乎总是需要）
- ForensicsAgent：自动收集容器日志和事件（仅适用于 crashloop/oom）

请以 JSON 数组输出需要调用的 Agent 名称，例如：[\"K8sAgent\", \"ForensicsAgent\"]
只输出 JSON，不要解释。"""
        plan = None
        try:
            reply = await chat(prompt, system='你是 SRE Agent 规划助手，只输出合法 JSON 数组。', timeout=15, model_env='LLM_MODEL_ROUTER')
            match = re.search(r'\[.*?\]', reply or '', re.DOTALL)
            if match:
                candidate = json.loads(match.group())
                allowed = {'MetricAgent', 'K8sAgent', 'ForensicsAgent'}
                plan = [x for x in candidate if x in allowed]
        except Exception:
            plan = None
        if not plan:
            plan = ['K8sAgent']
            if fault_type in ('cpu', 'timeout'):
                plan.append('MetricAgent')
            if fault_type in ('crashloop', 'oom'):
                plan.append('ForensicsAgent')
        s['plan'] = plan
        await _emit(task_id, 'PlannerAgent', 'completed', result=plan)
        return s
    async def metric(s: RCAState) -> RCAState:
        # 遵从 Planner 调度：plan 为空时默认执行（兜底）
        if s.get('plan') and 'MetricAgent' not in s['plan']:
            return s
        await _emit(task_id, 'MetricAgent', 'started')
        try:
            result = await query_metric('up{job="rca-demo"}')
            s.setdefault('evidence', {})['metric'] = result.get('data', {})
        except Exception as exc:
            s.setdefault('evidence', {})['metric'] = {'error': str(exc)[:500]}
        await _emit(task_id, 'MetricAgent', 'completed', result=s.get('evidence', {}).get('metric'))
        return s

    async def k8s(s: RCAState) -> RCAState:
        # 遵从 Planner 调度
        if s.get('plan') and 'K8sAgent' not in s['plan']:
            return s
        await _emit(task_id, 'K8sAgent', 'started')
        try:
            result = await get_pod_status(alert['service'], namespace='default')
            s.setdefault('evidence', {})['k8s'] = result.get('data', {})
        except Exception as exc:
            s.setdefault('evidence', {})['k8s'] = {'error': str(exc)[:500]}
        await _emit(task_id, 'K8sAgent', 'completed', result=s.get('evidence', {}).get('k8s'))
        return s

    async def forensics(s: RCAState) -> RCAState:
        # 遵从 Planner 调度（同时保留 fault_type 安全门控）
        if s.get('plan') and 'ForensicsAgent' not in s['plan']:
            return s
        fault_type = s.get('route', {}).get('fault_type', 'unknown')
        enabled = fault_type in ('crashloop', 'oom') and not baseline
        if not enabled:
            return s
        await _emit(task_id, 'ForensicsAgent', 'started')
        evidence = s.setdefault('evidence', {})
        try:
            logs_result = await get_pod_logs(alert['service'], tail_lines=80, namespace='default')
            evidence['logs'] = logs_result.get('data', {})
        except Exception as exc:
            evidence['logs'] = {'error': str(exc)[:500]}
        try:
            events_result = await get_events(alert['service'], namespace='default')
            evidence['events'] = events_result.get('data', {})
        except Exception as exc:
            evidence['events'] = {'error': str(exc)[:500]}
        await _emit(task_id, 'ForensicsAgent', 'completed', result={'enabled': enabled})
        return s

    async def runbook(s: RCAState) -> RCAState:
        await _emit(task_id, 'RunbookAgent', 'started')
        try:
            result = await runbook_agent(s.get('route', {}).get('fault_type', 'unknown'), alert['description'])
            s.setdefault('evidence', {})['runbook'] = result.get('data', [])
        except Exception as exc:
            s.setdefault('evidence', {})['runbook'] = {'error': str(exc)[:500]}
        await _emit(task_id, 'RunbookAgent', 'completed', result=s.get('evidence', {}).get('runbook'))
        return s

    async def summarize(s: RCAState) -> RCAState:
        await _emit(task_id, 'Summarize', 'started')
        s['report'] = await build_report(s.get('route', {}), s.get('evidence', {}))
        await _emit(task_id, 'Summarize', 'completed')
        return s

    async def followup(s: RCAState) -> RCAState:
        await _emit(task_id, 'FollowUpAgent', 'started')
        plan = await generate_follow_up(s.get('route', {}).get('fault_type', 'unknown'), s.get('evidence', {}), s.get('report', ''))
        s['follow_up'] = plan
        if plan.get('needs_follow_up'):
            s['report'] = s.get('report', '') + format_follow_up(plan)
        await _emit(task_id, 'FollowUpAgent', 'completed', result=plan)
        return s

    async def report(s: RCAState) -> RCAState:
        await _emit(task_id, 'Report', 'started')
        if task_id in TASKS:
            TASKS[task_id]['report'] = s.get('report', '')[:2000]
            await TASKS[task_id]['queue'].put({'type': 'report', 'report': TASKS[task_id]['report']})
        return s

    async def baseline_summarize(s: RCAState) -> RCAState:
        await _emit(task_id, 'Summarize', 'started')
        s['evidence'] = {}
        s['report'] = await build_report(s.get('route', {}), {})
        await _emit(task_id, 'Summarize', 'completed')
        return s

    graph = StateGraph(RCAState)
    if baseline:
        for name, fn in [('router', router), ('summarize', baseline_summarize), ('report', report)]:
            graph.add_node(name, fn)
        graph.set_entry_point('router')
        graph.add_edge('router', 'summarize')
        graph.add_edge('summarize', 'report')
    else:
        for name, fn in [('router', router), ('planner', planner), ('metric', metric), ('k8s', k8s), ('forensics', forensics), ('runbook', runbook), ('summarize', summarize), ('followup', followup), ('report', report)]:
            graph.add_node(name, fn)
        graph.set_entry_point('router')
        for first, second in [('router', 'planner'), ('planner', 'metric'), ('metric', 'k8s'), ('k8s', 'forensics'), ('forensics', 'runbook'), ('runbook', 'summarize'), ('summarize', 'followup'), ('followup', 'report')]:
            graph.add_edge(first, second)
    graph.add_edge('report', END)
    await graph.compile().ainvoke({'task_id': task_id, 'alert': alert, 'baseline': baseline, 'evidence': {}, 'plan': []})
    if task_id in TASKS:
        TASKS[task_id]['done'] = True






