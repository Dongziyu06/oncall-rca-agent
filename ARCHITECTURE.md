# 模块技术路线说明

面向面试口述 / 复习用。细节以代码为准。

## 1. API 层（`api/`）

- FastAPI 接收请求，异步起后台任务，不阻塞 HTTP。
- 告警：`POST /alert` → `task_id` → `GET /task/{id}/stream`（SSE）。
- 对话：`POST /chat` → `session_id` → `GET /chat/{id}/stream`（SSE）。
- 启动时 `load_dotenv()`；MCP 子应用在 FastAPI lifespan 里启动 session manager。

## 2. Orchestrator（`agents/orchestrator.py`）

- LangGraph `StateGraph` 串起 RCA 流水线。
- `baseline=True`：只跑 Router + Summarize（Mode A）。
- 完整模式：Router → Planner → Metric/K8s/Forensics（按 plan 跳过）→ Runbook → Summarize → FollowUp → Report。
- 每个节点通过队列推 SSE 进度。

## 3. Router（`agents/router.py`）

- 轻量模型（`LLM_MODEL_ROUTER`）把告警分成 cpu/oom/crashloop/timeout/unknown。
- 失败或无 Key → 关键词兜底（`keyword_fallback`）。

## 4. Planner（同一文件内）

- 根据 fault_type + 描述输出要调用的 Agent 列表（Plan-Execute）。
- 下游 metric/k8s/forensics 有 guard：不在 plan 中则跳过。

## 5. Tools（`tools/`）

- Prometheus / K8s / Loki：真实连接失败自动 mock 回退。
- K8s 返回 `last_state`（exit_code / reason / message）。
- `mcp_server.py`：FastMCP 包装同一批工具，挂 `/mcp`。

## 6. RAG（`rag/` + `runbooks/`）

- 147 文档入库 Chroma；检索 = 向量 + BM25 + RRF。
- 评测分两层：定制 query（in-dist）与真实告警描述（out-of-dist，Recall@3≈70%）。

## 7. Summarize / FollowUp

- Summarize：重模型生成中文 RCA，引用 logs/events/退出码；失败回退模板。
- FollowUp：解析置信度，低于 0.5 时生成缺失证据与建议查询。

## 8. ChatAgent（`agents/chat_agent.py`）

- ReAct：LLM 决定 `tool` 或 `answer`；工具超时 30s；最多 10 步。
- 多轮历史在内存 `SESSIONS`。

## 9. 评测 / 部署

- `eval/`：场景、A/B、RAG 量化。
- Docker Compose + 阿里云 ECS；日常更新见 `DEPLOY.md`。
