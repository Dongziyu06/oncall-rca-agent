# OnCall 多 Agent RCA 助手

告警驱动的只读多 Agent 根因分析演示项目：自动路由故障类型，查询观测数据和 Runbook，并通过 SSE 输出 RCA 报告。

## 架构

```text
Alert -> FastAPI -> Router -> MetricAgent -> K8sAgent -> RunbookAgent
                                      -> Summarize -> Markdown RCA -> SSE
```

## Quick Start

```powershell
cd D:\aiops\oncall-rca-agent
python -m pip install -r requirements.txt
python -m uvicorn api.main:app --reload
```

```powershell
curl.exe -X POST http://127.0.0.1:8000/alert -H "Content-Type: application/json" -d "{\"alerts\":[{\"labels\":{\"alertname\":\"HighCPU\",\"service\":\"demo\"},\"annotations\":{\"description\":\"CPU is high\"}}]}"
# 用返回的 task_id:
curl.exe -N http://127.0.0.1:8000/task/<task_id>/stream
```

浏览器打开 `http://127.0.0.1:8000` 可使用极简演示页。

## 评测

```powershell
python eval/run_eval.py --mode both --dry-run
# 连接 API 后可加 --inject 在 kind 中注入故障
```

| Mode | Hit | Hit rate | Avg ms |
|---|---:|---:|---:|
| A baseline | 8/10（dry-run） | 80% | 0 |
| B full | 8/10（dry-run） | 80% | 0 |

真实 kind 评测结果写入 `eval/results/result_*.json` 后替换此表。

## 目录

`api/` FastAPI 与 SSE；`agents/` LangGraph 节点；`tools/` Prometheus/K8s/Loki 只读工具；`rag/` Runbook 与 Chroma/BM25 检索；`eval/` 场景、注入和评测；`infra/` kind、Prometheus、Demo 应用；`static/` 演示页面；`tests/` 自动化测试。
