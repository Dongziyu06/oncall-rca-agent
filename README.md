# OnCall 多 Agent RCA 助手

告警驱动 + 自然语言对话的只读多 Agent 根因分析（RCA）演示项目。  
默认只读，不自动变更生产资源；高风险操作在报告中标注需人工审批。

- 仓库：https://github.com/Dongziyu06/oncall-rca-agent  
- 演示：http://123.56.47.94:8000  

---

## 架构（当前）

### 告警流水线（Plan-Execute）

```text
Alert → FastAPI → Router → PlannerAgent
         → [按计划动态执行 Metric / K8s / Forensics]
         → RunbookAgent(RAG) → Summarize → FollowUpAgent → Report(SSE)
```

- **Mode A（baseline）**：Router → Summarize → Report（无工具、无 RAG）  
- **Mode B（full）**：完整 Plan-Execute 流水线  

### 对话模式（ReAct）

```text
用户自然语言 → ChatAgent(think → tool → think → … → answer)
                工具：Prometheus / K8s / Events / Logs / RAG
                多轮历史保存在 session（最近 20 条）
```

### MCP 工具层

```text
Prometheus / K8s / Loki 只读工具
        ↓ 包装
MCP Streamable HTTP  →  /mcp
（供 MCP Inspector 或支持 MCP 的客户端调用）
```

> 说明：项目内部 Chat / Orchestrator **直接调用** Python 工具函数；MCP 是对外暴露的标准协议层，便于简历技术栈与外部客户端对接，不是重复实现一套工具。

---

## Quick Start

```powershell
cd D:\aiops\oncall-rca-agent
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# 编辑 .env：至少填写 OPENAI_API_KEY / OPENAI_BASE_URL
python -m uvicorn api.main:app --reload
```

浏览器打开：http://127.0.0.1:8000  

- **告警分析**：表单提交 Alert  
- **对话分析**：右上角切换到 💬，用自然语言描述故障  

### API 示例

```powershell
# 告警 RCA
curl.exe -X POST http://127.0.0.1:8000/alert -H "Content-Type: application/json" -d "{\"alerts\":[{\"labels\":{\"alertname\":\"CrashLoopBackOff\",\"service\":\"vlb\"},\"annotations\":{\"description\":\"Pod repeatedly crashes\"}}]}"
curl.exe -N http://127.0.0.1:8000/task/<task_id>/stream

# 对话
curl.exe -X POST http://127.0.0.1:8000/chat -H "Content-Type: application/json" -d "{\"message\":\"我的 vlb 服务 CrashLoopBackOff 了\"}"
curl.exe -N http://127.0.0.1:8000/chat/<session_id>/stream
```

### MCP

端点：`http://127.0.0.1:8000/mcp`（Streamable HTTP）  
这不是普通 GET JSON；请用 MCP Inspector 或 MCP 客户端发送 `initialize` / `tools/list`。

暴露工具：`prometheus_query`、`kubernetes_pod_status`、`kubernetes_pod_logs`、`kubernetes_events`、`loki_logs`。

---

## 评测结果

### RCA A/B（分类命中，10 场景）

| Mode | Hit | Hit rate | 说明 |
|---|---:|---:|---|
| A baseline | 8/10 | 80% | 仅告警文本 / 关键词兜底 |
| B full | 8/10 | 80% | 早期 mock 评测；真实集群数字待补跑 |

### RAG（更有意义的 out-of-distribution）

| 评测类型 | 样本 | Recall@3 | MRR |
|---|---|---:|---:|
| in-distribution（定制 query） | 20 | 100% | 0.79 |
| **真实告警 description** | 10 | **70%** | **0.48** |

运行：

```powershell
python eval/test_rag.py
python eval/honest_rag_test.py
python eval/run_eval.py --mode both --dry-run
```

---

## 目录

| 路径 | 作用 |
|---|---|
| `api/` | FastAPI、SSE、告警/任务/对话路由 |
| `agents/` | Router / Planner / Chat(ReAct) / Summarize / FollowUp / Orchestrator |
| `tools/` | Prometheus、K8s、Loki 只读工具 + `mcp_server.py` |
| `rag/` | Runbook 入库、Chroma + BM25 + RRF |
| `runbooks/` | 147 份知识库文档 |
| `eval/` | 场景、RAG 评测、A/B 评测 |
| `static/` | Web UI（告警分析 + 对话分析） |
| `infra/` | kind / Prometheus / demo 应用 |
| `DEPLOY.md` | 阿里云更新清单 |

---

## Docker / 云部署

```powershell
Copy-Item .env.example .env
docker compose up -d --build
```

**主部署路径是实验室**（与 K8s/Prometheus 同网）：见 [DEPLOY.md](DEPLOY.md)。  
GitLab CI：`.gitlab-ci.yml`（`test` 自动；`deploy_lab` 在 main 上手动触发）。

Compose 通过 `env_file` 注入密钥；`.env` 不打进镜像；Runbook 只读挂载；Chroma 持久化在 `chroma_data` volume。

---

## Tech Stack

- **LangGraph**：告警流水线状态图 + Chat ReAct 循环  
- **RAG**：Chroma 向量 + BM25 + RRF，147 份 Runbook / Postmortem  
- **Plan-Execute**：PlannerAgent 动态选择 Metric / K8s / Forensics  
- **ReAct 多轮对话**：自然语言取证 + SSE 流式进度  
- **MCP**：工具层按 Anthropic MCP 标准对外暴露（`/mcp`）  
- **多模型路由**：Router / FollowUp / Summarize 使用不同复杂度模型  
- **可观测性**：Prometheus / Kubernetes / Loki（真实连接，失败自动 mock 回退）  
- **FastAPI + SSE**：告警任务流与对话流  

---

## 测试

```powershell
python -m pytest -q
```

当前基线：`10 passed`。
