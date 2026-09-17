"""
用真实告警场景的 description 做 RAG 测试（out-of-distribution，更真实）
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rag.retriever import retrieve
import json

# fault_type → 期望能检索到的 runbook id（任意一个命中即算 hit）
FAULT_TO_RUNBOOKS = {
    'cpu':       ['high_cpu_load', 'CPU_Throttling_High_kube_prometheus_runbooks',
                  'Kube_CPU_Quota_Overcommit_kube_prometheus_runbooks', 'Kube_CPU_Overcommit_kube_prometheus_runbooks'],
    'oom':       ['oom_killed', 'Kube_Memory_Overcommit_kube_prometheus_runbooks'],
    'crashloop': ['crashloop_backoff', 'Kube_Pod_Crash_Looping_kube_prometheus_runbooks'],
    'timeout':   ['service_timeout', 'Kubelet_Pod_Start_Up_Latency_High_kube_prometheus_runbooks'],
    'unknown':   ['node_not_ready', 'pod_pending', 'disk_pressure',
                  'Kube_Node_Not_Ready_kube_prometheus_runbooks', 'Kube_Pod_Not_Ready_kube_prometheus_runbooks'],
}

def main():
    scenarios_dir = Path(__file__).parent / 'scenarios'
    scenarios = [
        json.loads(p.read_text(encoding='utf-8-sig'))
        for p in sorted(scenarios_dir.glob('s*.json'))
    ]

    print('=' * 65)
    print('RAG 真实评测：用 alert description 作 query（out-of-distribution）')
    print('=' * 65)

    hits1, hits3, rr_sum = 0, 0, 0.0

    for s in scenarios:
        query = s['description']
        fault = s['ground_truth']
        expected = FAULT_TO_RUNBOOKS.get(fault, [])
        results = retrieve(query, top_k=3)
        ids = [r['id'] for r in results]
        scores = [round(r.get('rrf_score', r.get('score', 0)), 4) for r in results]

        hit1 = any(e in ids[:1] for e in expected)
        hit3 = any(e in ids[:3] for e in expected)
        rr = 0.0
        for rank, rid in enumerate(ids, 1):
            if rid in expected:
                rr = 1.0 / rank
                break

        hits1 += hit1
        hits3 += hit3
        rr_sum += rr

        icon = '✅' if hit3 else '❌'
        print(f'\n{icon} [{s["id"]}] fault={fault}')
        print(f'   query: "{query}"')
        for i, (rid, sc) in enumerate(zip(ids, scores), 1):
            mark = ' ←命中' if rid in expected else ''
            print(f'   Top-{i}: {rid}  (score={sc}){mark}')

    n = len(scenarios)
    print()
    print('=' * 65)
    print(f'测试样本数  : {n}（来自真实告警场景，非 RAG 定制查询）')
    print(f'Recall@1   : {hits1}/{n} = {hits1/n*100:.1f}%')
    print(f'Recall@3   : {hits3}/{n} = {hits3/n*100:.1f}%')
    print(f'MRR        : {rr_sum/n:.3f}')
    print('=' * 65)
    print()
    print('对比：')
    print('  Codex 定制查询集（in-dist） : Recall@3 = 100.0%（过于理想，循环评测）')
    print(f'  真实告警描述（out-of-dist） : Recall@3 = {hits3/n*100:.1f}%（这是更有意义的数字）')

if __name__ == '__main__':
    main()
