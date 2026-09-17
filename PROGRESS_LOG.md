# 项目进度记录

---

## 第 1 周（2026-09-15）：骨架完成

**完成内容：**
- 完整第四章目录结构
- FastAPI `POST /alert` + `GET /task/{id}/stream`（SSE）
- LangGraph 5 节点串行编排：Router → MetricAgent → K8sAgent → Summarize → Report
- 关键词故障分类（cpu/oom/crashloop/timeout），LLM 可用时调 LiteLLM
- 所有工具 mock 数据，无需外部依赖
- 统一 `{"error","data"}` 返回 + 2000 字截断 + structlog
- 3 个 pytest 通过

**验收命令：**
```cmd
curl -X POST http://127.0.0.1:8000/alert -H "Content-Type: application/json" -d "{\"alerts\":[{\"labels\":{\"alertname\":\"HighCPU\",\"service\":\"demo\"},\"annotations\":{\"description\":\"CPU usage is high\"}}]}"
curl -N http://127.0.0.1:8000/task/<task_id>/stream
```

---

## 第 2 周（2026-09-15）：真实工具 + RAG

**基础设施搭建（手动完成）：**
- Docker Desktop 启动
- kind v0.23.0 安装（直接下载 exe 到 System32）
- helm v4.3.0 安装（winget）
- `kind create cluster --name rca-demo`
- `helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring --create-namespace --set grafana.enabled=false`
- `kubectl apply -f infra/sample-app/deployment.yaml`（rca-demo Pod Running）
- `kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090`
- 浏览器验证 `http://localhost:9090` ✅

**代码完成（Codex 实现）：**
- `tools/prometheus_tools.py`：真实 httpx 调 Prometheus API，无连接时 mock 回退
- `tools/k8s_tools.py`：kubernetes client 只读（Pod状态/日志/Events），无 kubeconfig 时 mock 回退
- `tools/loki_tools.py`：Loki HTTP API，mock 回退
- `rag/runbooks/`：4 份 Runbook（cpu_high / oom_killed / crashloop / timeout）
- `rag/ingest.py`：Chroma 向量化
- `rag/retriever.py`：BM25 + Chroma + RRF 融合，top-3 召回
- `agents/runbook_agent.py`：RAG 取证节点
- `agents/summarize.py`：从 orchestrator 拆出
- `agents/orchestrator.py`：6 节点编排（加入 RunbookAgent）
- 5 个 pytest 通过

**实际 SSE 输出验证：**
```
Router(cpu) → MetricAgent → K8sAgent → RunbookAgent → Summarize → Report
报告含：故障类型/根因/置信度/证据链/Runbook摘录/建议
```

**注：** 指标/K8s 证据仍显示 mock（port-forward 需保持开启才走真实数据）

---

## 第 3 周（进行中）：评测 + 收尾

**目标：**
- 10 个故障场景 JSON
- `eval/inject_fault.py`：kubectl 故障注入
- `eval/run_eval.py`：Mode A（基线）vs Mode B（完整）对照实验
- 极简演示页面 `static/index.html`
- README 完善（架构图 + 评测结果表）

**代码完成（Codex 实现）：**
- 10 个故障场景 JSON（S01-S10，覆盖 cpu/oom/crashloop/timeout/scale/image/pending 等）
- `eval/inject_fault.py`：Windows 兼容 kubectl 注入器
- `eval/run_eval.py`：Mode A（基线）vs Mode B（完整）A/B 对照评测
- `USE_MOCK=true/false` 工具开关
- `static/index.html`：极简 SSE 演示页面（FastAPI 挂载）
- README 完善：架构图 + Quick Start + 评测占位表 + 目录说明
- 5 个 pytest 通过

**dry-run 数字（mock 数据，仅验证流程）：**
- Mode A (baseline): hit 8/10  80%  avg 0ms
- Mode B (full):     hit 8/10  80%  avg 0ms
- ⚠️ dry-run 两者相同是正常的（都走 fallback 关键词匹配），真实数字需接集群后跑

**待完成：真实评测**
- kind.exe 需重新安装（System32 里不存在，Codex 沙箱装的没生效到本机）
- 重装后：`python eval/run_eval.py --mode both --inject` 跑真实数字
- 填入简历的最终数字：Mode A __/10，Mode B __/10

---

## 环境快速恢复（每次重启后）

```powershell
# 1. 启动 Docker Desktop（等绿灯）

# 2. 暴露 Prometheus（新开窗口保持运行）
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090

# 3. 启动 RCA 助手（另一个窗口）
cd D:\aiops\oncall-rca-agent
.venv\Scripts\Activate.ps1
uvicorn api.main:app --reload
```

---

## 第 4 节点（2026-09-15）：LLM 完整接入成功

**里程碑：** qwen3.8-flash via Token Plan API 全链路接入，Router + Summarize 均走 LLM 生成

**完成事项：**
- `agents/llm_client.py`：统一封装 httpx 直连 Token Plan API，绕过 litellm 模型名校验问题
- `agents/router.py`：接入 LLM 分类（`method: llm`），超时自动降级 keyword_fallback
- `agents/summarize.py`：接入 LLM 生成完整 RCA 报告（告别静态模板），超时降级模板回退
- 诊断并修复 qwen3.8-flash 模型调用失败问题（API Key / Base URL 配置，httpx 直连方案）
- `test_e2e.py`：一键测试脚本（自动启动服务、多场景测试、结果可视化）

**E2E 测试结果（2026-09-15，3 场景）：**

| 场景 | Router method | 报告生成方式 | 说明 |
|---|---|---|---|
| 场景1：CPU 高负载 | `llm` | 🤖 LLM生成 | LLM 全程正常，生成详细 RCA |
| 场景2：OOM 内存溢出 | `llm` | ⚠️ 模板回退 | Router LLM ✅，Summarize LLM ReadTimeout 降级 |
| 场景3：Pod CrashLoop | `keyword_fallback` | ⚠️ 模板回退 | Router LLM ReadTimeout 降级，Summarize LLM ReadTimeout 降级 |

> LLM API 偶发 ReadTimeout（约 30-40s），降级机制正常工作；场景1 完整 LLM 生成验证通过。

**A/B 评测结果（2026-09-15，10 场景，真实服务）：**

| 模式 | hit rate | avg 响应时间 | 说明 |
|---|---|---|---|
| Mode A (baseline，USE_MOCK=true) | 8/10 = **80%** | 1017 ms | 关键词分类兜底 |
| Mode B (full，USE_MOCK=false) | 8/10 = **80%** | 1021 ms | 工具链全开（Prometheus/K8s mock fallback） |

> dry-run 数字同上（0ms）；真实 avg 约 1s，两模式相同因 Prometheus/K8s 均为 mock fallback（无外部集群连接）。命中率 80%（8/10），2 个误分类场景待接真实集群后补查。

---

## 第 5 节点（2026-09-16）：深度完善 — 对话化 + MCP + 动态规划 + RAG 量化

**背景**：与同类项目对比后发现 4 项关键差距，本节点全部补齐。

### 5.1 实验室 K8s 真实接入 & ForensicsAgent

**完成事项（2026-09-16）：**
- VPN 连接实验室服务器 `cnic@10.10.140.2`
- `.env` 接入真实 `PROMETHEUS_URL=http://10.10.140.2:30090` 和 `KUBECONFIG`
- `tools/k8s_tools.py` 新增 `last_state` 字段：**退出码 + 错误信息 + 终止时间**
- 真实 e2e 验证：`vlb` Pod（restarts=4419，exit_code=128，StartError，containerd broken pipe）
- 修复全部 4 个废弃测试（`acompletion` → `llm_client.chat` monkeypatch），**10/10 passed**

**关键证据（对面试有用）：**
```
vlb Pod：exit_code=128, reason=StartError
message: failed to create containerd task: OCI runtime create failed:
         container_linux.go:370: starting container process caused:
         process_linux.go:369: sending config to init process caused:
         write init-p: broken pipe: unknown
```
这说明容器进程从未启动（broken pipe），因此 `--previous` 日志为空是正常的。
ForensicsAgent 将此 `last_state` 传给 LLM，使 LLM 能精确定位根因而非模糊推测。

---

### 5.2 四项架构升级（计划中，Codex 实现）

#### ① RAG Recall@3 量化评测 ✅ 已完成

**关键发现：区分两种评测场景**

| 评测类型 | 样本来源 | Recall@3 | MRR | 意义 |
|---------|---------|---------|-----|------|
| in-distribution（Codex 定制）| `eval/rag_eval_dataset.json`（20条） | **100%** | 0.79 | 循环评测，过于理想 |
| out-of-distribution（真实告警）| `eval/scenarios/S01-S10.json`（10条） | **70%** | 0.48 | 更真实，可写进简历 |

**3 个 miss 分析（知识库盲区）：**
- S04 `"Deployment replicas are zero"` → expected_ids 未覆盖 Prometheus Operator 的 Deployment 类 runbook
- S06 `"Image tag does not exist"` → ImagePullBackOff 专项 runbook 缺失
- S10 `"Required environment variable is missing"` → 配置错误类文档缺失

**新增文件：**
- `eval/rag_eval_dataset.json`：20 条定制评测集
- `eval/test_rag.py`：支持 --top-k --verbose 的量化评测脚本
- `eval/honest_rag_test.py`：用真实告警描述做 out-of-distribution 测试（更有意义）

**简历写法：**
> "设计双层 RAG 评测体系（in-dist Recall@3=100%，out-of-dist Recall@3=70% / MRR=0.48），识别出 ImagePullBackOff 和配置错误类知识盲区，具备改进方向"

#### ② 对话式 Chat + ReAct 多轮问答 ✅ 已完成

**架构**：ReAct 循环（think → execute_tool → think → ... → answer，最多10步）

**新增文件：**
- `agents/chat_agent.py`：ReAct 状态机，支持5个工具（K8s/Prometheus/Loki/RAG），内存多轮历史（最近20条）
- `api/routes/chat.py`：POST `/chat` + GET `/chat/{sid}/stream`（SSE推送）

**UI 升级：**
- `static/index.html` 右上角新增 🚨/💬 切换按钮
- 💬 对话面板：用户气泡（右/蓝）+ 助手气泡（左/灰）+ 工具调用气泡（monospace）
- 支持 Markdown 渲染、Enter 发送、新对话按钮

**e2e 验证**：
- 发送 `"我的vlb服务一直CrashLoopBackOff"` → LLM 自动调用 `get_pod_status(vlb)` → 连接实验室 K8s ✅
- 修复：工具调用加 `asyncio.wait_for(timeout=30s)` 超时保护（防 VPN 断开时无限卡死）

**测试**：10/10 passed

#### ③ 动态 Agent 选择（Planner 节点）✅ 已完成

**流水线升级**：
```
旧：Router → Metric → K8s → Forensics → Runbook → Summarize → FollowUp → Report
新：Router → PlannerAgent → [按计划执行] → Runbook → Summarize → FollowUp → Report
```

**PlannerAgent 逻辑**：
- 用 LLM（轻量 `LLM_MODEL_ROUTER`）分析 fault_type + alert description
- 输出 JSON 数组：`["K8sAgent", "ForensicsAgent"]`（仅调用必要的 Agent）
- LLM 失败时按规则 fallback：cpu/timeout 加 MetricAgent，crashloop/oom 加 ForensicsAgent

**Guard 检查**（防止 Planner 形同虚设）：
- `metric`/`k8s`/`forensics` 节点先检查 `s['plan']`，不在其中则直接 return 跳过
- `plan` 为空时默认执行（兜底保护）

**修复记录**：
- Codex 生成版本未在 metric/k8s/forensics 中加 guard 检查（Planner 有制定计划但下游无视），人工补充
- 测试断言由 `assert 'Runbook' in report` 改为兼容 LLM 中文输出（含"参考知识库"或"RCA"）
- **10/10 passed**

## 第 6 节点（2026-09-17）：实验室 GitLab + CI/CD

- 仓库：https://gitlab.fir.ac.cn/Dongziyu/oncall-rca-agent
- 远程：`origin`=GitHub，`gitlab`=实验室 GitLab
- 新增 `.gitlab-ci.yml`：`test`（pytest）+ `deploy_lab`（main 手动 SSH 部署）
- 新增 `scripts/deploy_lab.sh`；`DEPLOY.md` 改为实验室主路径


**新增文件：** `tools/mcp_server.py`  
将现有只读工具包装为 MCP Tool，不改底层实现：
- `prometheus_query`
- `kubernetes_pod_status` / `kubernetes_pod_logs` / `kubernetes_events`
- `loki_logs`

**接入方式：**
- 依赖：`mcp>=1.0,<2`（mcp 2.x 移除了 FastMCP，锁定 1.x）
- FastAPI 挂载：`/mcp`（Streamable HTTP）
- MCP 导入失败时打印警告，主服务仍可启动

**核对时修复的 3 个实际不可用问题：**
1. FastMCP 默认路径是 `/mcp`，再 mount 到 `/mcp` 会变成 `/mcp/mcp` → 改为 `streamable_http_path="/"`
2. FastAPI 不会自动启动子应用 lifespan，MCP 报 `Task group is not initialized` → 在 FastAPI `lifespan` 里 `async with mcp.session_manager.run()`
3. 默认 DNS rebinding 只允许 localhost，公网 IP / TestClient 会被拦 → 演示环境关闭该校验

**验证：** `initialize` + `tools/list` 返回 5 个工具，serverInfo.name = `oncall-rca-tools`

