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

