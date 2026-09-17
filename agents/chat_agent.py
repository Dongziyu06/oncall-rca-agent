from __future__ import annotations

import asyncio
import json
from typing import Any, TypedDict, Awaitable, Callable

from agents.llm_client import chat
from tools.k8s_tools import get_pod_status, get_pod_logs, get_events
from tools.prometheus_tools import query_metric
from rag.retriever import retrieve

SESSIONS: dict[str, list[dict[str, str]]] = {}

class ChatState(TypedDict, total=False):
    session_id: str
    messages: list[dict[str, Any]]
    tool_calls: list[dict[str, Any]]
    final_answer: str
    step: int
    action: dict[str, Any]

TOOLS = {
    'get_pod_status': get_pod_status,
    'query_metric': query_metric,
    'get_pod_logs': get_pod_logs,
    'get_events': get_events,
}

SYSTEM = '''你是 SRE OnCall 助手。可用工具：get_pod_status(service)、query_metric(promql)、get_pod_logs(service)、get_events(service)、retrieve_runbook(fault_description)。用户描述故障时，先调用工具收集证据，再给出根因分析。每次只输出合法 JSON：需要工具时输出 {"action":"tool","tool":"工具名","args":{...}}；可以回答时输出 {"action":"answer","content":"..."}。不要输出 Markdown 代码围栏。'''

async def _emit(emit: Callable[[dict], Awaitable[None]] | None, event: dict) -> None:
    if emit:
        await emit(event)

async def _think(s: ChatState, emit=None) -> ChatState:
    await _emit(emit, {'type': 'thinking', 'content': '正在分析下一步行动...'})
    history = s.get('messages', [])[-20:]
    prompt = '对话历史：\n' + json.dumps(history, ensure_ascii=False, default=str) + '\n请决定下一步动作。'
    reply = await chat(prompt=prompt, system=SYSTEM, timeout=30, model_env='LLM_MODEL')
    action: dict[str, Any] = {}
    if reply:
        try:
            raw = reply.strip().removeprefix('```json').removesuffix('```').strip()
            action = json.loads(raw)
        except Exception:
            action = {'action': 'answer', 'content': reply}
    if not action:
        text = ' '.join(str(m.get('content', '')) for m in history if m.get('role') == 'user').lower()
        if s.get('tool_calls'):
            action = {'action': 'answer', 'content': '已完成工具取证。根据当前返回结果，请结合 Pod 状态、指标和事件进行人工复核；如需进一步分析，请提供具体服务名或时间范围。'}
        elif any(k in text for k in ('crash', 'pod', 'kubernetes', 'oom')):
            action = {'action': 'tool', 'tool': 'get_pod_status', 'args': {'service': 'demo'}}
        else:
            action = {'action': 'answer', 'content': '请提供服务名、告警现象或错误描述，我会先收集相关运行证据。'}
    s['action'] = action
    s['step'] = s.get('step', 0) + 1
    return s

async def _execute_tool(s: ChatState, emit=None) -> ChatState:
    action = s.get('action', {})
    name = action.get('tool', '')
    args = action.get('args') or {}
    await _emit(emit, {'type': 'thinking', 'content': f'正在调用 {name}...'})
    try:
        if name == 'retrieve_runbook':
            raw = await asyncio.wait_for(
                asyncio.to_thread(retrieve, str(args.get('fault_description', args.get('query', ''))), 3),
                timeout=10,
            )
            result = raw
        elif name in TOOLS:
            result = await asyncio.wait_for(TOOLS[name](**args), timeout=30)
        else:
            result = {'error': f'未知工具: {name}', 'data': None}
    except asyncio.TimeoutError:
        result = {'error': f'工具 {name} 超时（>30s），可能是网络问题，已跳过', 'data': None}
    except Exception as exc:
        result = {'error': str(exc)[:500], 'data': None}
    s.setdefault('tool_calls', []).append({'tool': name, 'args': args, 'result': result})
    s.setdefault('messages', []).append({'role': 'tool', 'name': name, 'content': json.dumps(result, ensure_ascii=False, default=str)[:2000]})
    await _emit(emit, {'type': 'tool_result', 'tool': name, 'result': result})
    return s

async def _answer(s: ChatState, emit=None) -> ChatState:
    content = s.get('action', {}).get('content', '')
    if not content:
        content = '已完成证据收集，但未生成可用回答。'
    s['final_answer'] = content[:2000]
    s.setdefault('messages', []).append({'role': 'assistant', 'content': s['final_answer']})
    await _emit(emit, {'type': 'answer', 'content': s['final_answer']})
    return s

async def run_chat(session_id: str, message: str, emit=None) -> str:
    history = SESSIONS.setdefault(session_id, [])
    history.append({'role': 'user', 'content': message[:2000]})
    history[:] = history[-20:]
    state: ChatState = {'session_id': session_id, 'messages': list(history), 'tool_calls': [], 'step': 0}
    while state.get('step', 0) < 10:
        await _think(state, emit)
        if state.get('action', {}).get('action') == 'tool':
            await _execute_tool(state, emit)
            continue
        await _answer(state, emit)
        break
    else:
        state['action'] = {'action': 'answer', 'content': '已达到最大推理步数，请根据已收集证据进行人工复核。'}
        await _answer(state, emit)
    SESSIONS[session_id] = state.get('messages', [])[-20:]
    return state.get('final_answer', '')

