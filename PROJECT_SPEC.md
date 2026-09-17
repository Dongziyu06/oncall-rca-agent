# OnCall 多 Agent RCA 助手 —— 项目说明书

> 面向：AI 编程助手（Cursor / Claude / Copilot 等）  
> 目的：按本说明书规划并实现该项目，供新人用于求职简历展示  
> 定位：演示/学习级别（toy project），不追求生产完备，追求**概念正确、流程完整、知识点可讲**

---

## 一、背景与问题

### 1.1 现实痛点

生产系统出故障时，on-call 工程师通常要：

1. 看告警，判断是不是误报
2. 打开 Grafana 看指标
3. `kubectl describe pod` / `kubectl logs` 看容器状态
4. 翻 Confluence / Notion 上的运维手册（Runbook）
5. 根据经验猜根因
6. 写故障复盘（Postmortem）

整个过程高度依赖个人经验、容易遗漏证据、新人根本不知道从哪下手，平均处置时间（MTTR）动辄 20-60 分钟。

### 1.2 解决思路

**用 LLM Agent 自动化「取证 → 对照手册 → 输出根因报告」这条链路。**

- 告警或人工描述进来 → Agent 自动选排查套路 → 调用只读工具查指标/日志/K8s → RAG 检索运维手册 → LLM 生成结构化 RCA 报告 → （可选）高风险操作需人工确认。
- 默认**只读**，不自动变更任何生产资源。

### 1.3 项目定位与边界

| 项目追求 | 项目不追求 |
|----------|------------|
| 流程完整、概念正确 | 生产级鲁棒、高并发 |
| 技术栈现代（LangGraph/RAG/MCP）| 接入真实生产集群 |
| 有对照实验、能量化 | SOTA 论文级别效果 |
| 简历能自圆其说、面试能讲清楚 | 商业部署 |

---

## 二、参考项目（必读）

在开始编码前，务必了解以下项目的设计思路（不需要全部读完，重点看架构图和核心模块）：

### 2.1 主要参考：Mutil-Rag-Agent

- **地址**：https://github.com/Kkkirito-123/Mutil-Rag-Agent
- **参考什么**：整体架构骨架
  - LangGraph 多 Agent 编排方式（fast/deep 双模式）
  - Skill 路由（先选排查套路，再收窄工具范围）
  - RAG 检索（Milvus + BM25）
  - FastAPI 接入层 + SSE 推进度
  - 权限/审批结构
  - Docker Compose 启动方式
- **注意**：该仓已停更，本项目在其基础上**做减法（去掉复杂部分）+ 做加法（接入可观测性工具）**

### 2.2 工具设计参考：HolmesGPT

- **地址**：https://github.com/HolmesGPT/holmesgpt
- **参考什么**：只读工具（toolset）的设计方式
  - 每个 toolset 如何定义（输入/输出格式、如何截断大返回值）
  - 如何从 Prometheus 查 PromQL
  - 如何从 Kubernetes API 拿 Pod 状态/日志/Event
  - 如何把工具挂载给 Agent 调用
- **注意**：不要整仓照抄，只学**工具接口的设计模式**，在本项目中自己实现

### 2.3 评测环境参考：AIOpsLab

- **地址**：https://github.com/microsoft/AIOpsLab
- **参考什么**：
  - 如何构造可复现的故障场景（kind 本地集群 + 故障注入）
  - 评测指标的设计思路（根因命中、步骤合理性）
  - Problem Registry 里的故障题格式
- **本项目做法**：参考其思路，自建 8-15 个轻量故障场景（不必完整搭 AIOpsLab 基础设施）

---

## 三、完整故事线（对外讲法）

> 这是面试时讲的版本，AI 助手在写注释/文档时也按这个逻辑保持一致。

**背景**：现有告警处置高度依赖人工经验，MTTR 长、知识难传承。

**我做了什么**：  
设计并实现了一个 **告警驱动的多 Agent 根因分析（RCA）助手**：

1. **接入告警**：支持 Alertmanager webhook 格式，也支持自然语言描述。
2. **Skill 路由**：Agent 先判断故障类型（CPU 飙高 / Pod CrashLoop / 依赖超时等），选对应的排查套路。
3. **多 Agent 并行取证**：MetricAgent 查 Prometheus、K8sAgent 查集群状态、LogAgent 查容器日志。
4. **RAG 检索**：从向量数据库检索相关 Runbook 和历史故障案例。
5. **LLM 汇总**：把所有证据交给 LLM 生成结构化 RCA（原因、置信度、证据链、建议）。
6. **人工门禁**：涉及变更的建议不自动执行，只输出审批请求。

**结果**：  
在本地 kind 集群上注入 10 个典型故障场景，与「仅喂告警文本、不查工具」基线对比，多 Agent+工具+RAG 方案 Top-1 根因命中从 X 提升到 Y，平均响应时长约 Z 秒。

---

## 四、技术架构（已实现，以代码为准）

### 4.1 整体流程图

**告警流水线（Plan-Execute）：**

```
[告警 / Web UI]
        ↓
[FastAPI POST /alert]  ←→  SSE 推进度
        ↓
[LangGraph Orchestrator]
  ├─ Router：LLM 分类 fault_type（失败 → 关键词兜底）
  ├─ PlannerAgent：动态选择 Metric / K8s / Forensics
  ├─ MetricAgent：Prometheus PromQL
  ├─ K8sAgent：Pod 状态 + lastState 退出码
  ├─ ForensicsAgent：crashloop/oom 时拉 logs + events
  ├─ RunbookAgent：Chroma + BM25 + RRF（147 文档）
  ├─ Summarize：多模型 LLM 生成中文 RCA
  ├─ FollowUpAgent：置信度 < 0.5 时输出下一步查询计划
  └─ Report：SSE 推送
```

**对话模式（ReAct）：** `POST /chat` → think → tool → think → answer（多轮 session）

**MCP：** 内部直接调 `tools/*.py`；另用 FastMCP 把同一批工具暴露为 `/mcp`（Streamable HTTP）

Mode A（baseline）：Router → Summarize → Report  
Mode B（full）：完整上图流水线

### 4.2 技术栈清单

| 层次 | 技术选型 | 说明 |
|------|----------|------|
| API 层 | **FastAPI** + Uvicorn + SSE | 告警、对话、任务流 |
| Agent 编排 | **LangGraph** | Plan-Execute 流水线 + ReAct 对话 |
| LLM | **阿里云 Token Plan**（httpx 直连） | Router/FollowUp/Summarize 多模型路由 |
| 向量检索 | **ChromaDB** | Runbook / Postmortem RAG |
| 稀疏检索 | **BM25** + **RRF** | 与向量召回融合 |
| 指标 | **Prometheus HTTP API** | PromQL |
| 集群 | **kubernetes Python client** | Pod/日志/Events/退出码 |
| 日志 | **Loki HTTP API** | 可选 |
| 工具协议 | **MCP（FastMCP 1.x）** | `/mcp` Streamable HTTP |
| 部署 | **Docker Compose** + 阿里云 ECS | 见 DEPLOY.md |
| 前端 | HTML + Tailwind + marked.js | 告警分析 + 对话分析 |

### 4.3 核心模块目录结构（建议）

```
oncall-rca-agent/
├── README.md                    # 项目说明、Quick Start
├── docker-compose.yml           # 一键启动
├── .env.example                 # 所有配置项说明
│
├── api/
│   ├── main.py                  # FastAPI 入口
│   ├── routes/
│   │   ├── alert.py             # POST /alert  接收 Alertmanager webhook
│   │   └── task.py              # GET /task/{id}/stream  SSE 进度
│   └── models.py                # Pydantic 数据模型
│
├── agents/
│   ├── orchestrator.py          # LangGraph 图定义（节点/边）
│   ├── router.py                # Skill Router：故障类型分类
│   ├── metric_agent.py          # 查 Prometheus
│   ├── k8s_agent.py             # 查 Kubernetes（只读）
│   ├── log_agent.py             # 查 Loki / kubectl logs
│   ├── runbook_agent.py         # RAG 检索 Runbook
│   └── rca_agent.py             # 汇总证据、调 LLM 出报告
│
├── tools/
│   ├── prometheus_tools.py      # query_metric(promql, time_range)
│   ├── k8s_tools.py             # get_pod_status / get_pod_logs / get_events
│   └── loki_tools.py            # query_logs(service, time_range, keyword)
│
├── rag/
│   ├── ingest.py                # 向量化 Runbook 文档入库
│   ├── retriever.py             # 混合召回（BM25 + Milvus），RRF 融合
│   └── runbooks/                # 放 Markdown 格式的运维手册
│       ├── cpu_high.md
│       ├── crashloop.md
│       └── ...
│
├── eval/
│   ├── scenarios/               # 故障场景定义（JSON）
│   │   ├── cpu_throttle.json
│   │   ├── oom_killed.json
│   │   └── ...
│   ├── inject_fault.sh          # 向 kind 集群注入故障的脚本
│   ├── run_eval.py              # 批量跑评测，输出命中率/耗时
│   └── results/                 # 评测结果存放
│
├── infra/
│   ├── kind-config.yaml         # kind 集群配置
│   ├── prometheus/              # Prometheus 配置
│   └── sample-app/              # 可注入故障的 Demo 微服务
│
└── tests/
    └── test_tools.py            # 工具函数单元测试
```

---

## 五、实现计划（3 周）

### 第 1 周：跑通骨架

**目标**：收到 mock 告警 → 走完全流程 → 输出报告（数据全是假的也无所谓）

- [ ] 初始化 FastAPI 项目，`POST /alert` 接收 Alertmanager 格式 JSON
- [ ] 集成 LangGraph，定义最简 4 节点图：Router → （MetricAgent/K8sAgent） → Summarize → Report
- [ ] Router 用 LLM 分类：根据告警名判断故障类型（CPU/OOM/CrashLoop/Timeout）
- [ ] MetricAgent / K8sAgent 先用 **mock 数据**（返回写死的 JSON），先跑通编排
- [ ] LLM 汇总节点：把 mock 证据拼成 prompt，调 DeepSeek API，输出 Markdown 报告
- [ ] SSE 接口：让每个节点完成时推进度
- [ ] 本地能跑通 demo，不需要 K8s

**验收**：`curl -X POST /alert -d '{"alertname":"HighCPU",...}'` → 控制台看到多 Agent 依次执行 → 得到一份 Markdown RCA

---

### 第 2 周：接真工具 + RAG

**目标**：工具查真实数据；RAG 能检索 Runbook

- [ ] 用 kind 搭本地 K8s，部署 Prometheus + 一个 Demo 微服务
- [ ] 实现 `prometheus_tools.py`：真实 PromQL 查询，返回截断后的指标摘要
- [ ] 实现 `k8s_tools.py`：只读调用 kubernetes client，查 Pod 状态/日志/Event
- [ ] 写 3-5 份 Runbook（Markdown），用 `ingest.py` 向量化存入 Milvus / Chroma
- [ ] 实现 `retriever.py`：BM25 + 向量混合召回，RRF 融合
- [ ] 把 mock 工具替换为真实工具；在 kind 集群里手动触发一次 CPU 飙高，走完全流程

**验收**：kind 集群里有一个 Pod CPU 飙高 → Prometheus 告警 → Agent 自动查指标/K8s/Runbook → 出 RCA 报告，报告里有真实指标数据和 Runbook 摘录

---

### 第 3 周：评测 + 收尾

**目标**：有对照实验数据；项目能给人看

- [ ] 在 `scenarios/` 里写 8-10 个故障场景（CPU飙高、OOM、CrashLoop、依赖超时等）
- [ ] 写 `inject_fault.sh`：能快速向 kind 注入对应故障
- [ ] 写 `run_eval.py`：批量跑，记录「Agent 猜的根因」vs「真实根因」，算 Top-1 命中率
- [ ] 设置基线对比：Mode A（只喂告警文本，不查工具）vs Mode B（全工具+RAG）
- [ ] 写 README：Quick Start（`docker compose up` 能跑）、架构图、评测结果表
- [ ] 可选：加一个极简 Web 页面看 SSE 进度和最终报告

**验收**：README 里有一张「基线 vs 多Agent」对比表（哪怕数字不好看，有数字就行）；`docker compose up` 能启动所有服务

---

## 六、评测方案（怎么说有提升）

### 6.1 对照实验设计

| 实验组 | 配置 | 目的 |
|--------|------|------|
| 基线（Mode A） | 只把告警文本喂给 LLM，让它直接猜根因 | 无工具的天花板 |
| 实验组（Mode B） | 多 Agent + 工具查询 + RAG 检索 | 本项目完整方案 |

### 6.2 评测指标

- **Top-1 根因命中率**：Agent 输出的根因 == 注入的真实根因
- **平均调查耗时**：从告警进来到报告输出的秒数
- **证据覆盖度**（可选）：报告里用到了几类工具的数据（指标/K8s/日志/Runbook）

### 6.3 故障场景覆盖

| 场景 ID | 故障类型 | 注入方式 | 真实根因 |
|---------|----------|----------|----------|
| S01 | Pod CPU 飙高 | stress-ng 注入 | CPU 资源无限制 |
| S02 | Pod OOMKilled | 内存泄漏模拟 | 内存 limit 过低 |
| S03 | CrashLoopBackOff | 错误镜像 Tag | 镜像拉取失败 |
| S04 | 服务响应慢 | 加 sleep 注入 | 依赖服务超时 |
| S05 | Deployment 副本为 0 | 手动 scale=0 | 误操作缩容 |
| S06-S10 | （自行补充） | ... | ... |

---

## 七、关键概念速查（面试被问到时的知识储备）

AI 助手在生成代码注释和文档时，也请帮助作者理解以下概念：

| 概念 | 一句话解释 |
|------|-----------|
| **MTTR** | Mean Time To Recovery，平均故障恢复时间 |
| **RCA** | Root Cause Analysis，根因分析 |
| **Alertmanager** | Prometheus 的告警路由组件，可以 webhook 推送告警 |
| **LangGraph** | LangChain 出的有状态 Agent 编排框架，用图（节点+边）描述工作流 |
| **RAG** | Retrieval-Augmented Generation，先检索文档再让 LLM 生成，减少幻觉 |
| **Toolset / Tool calling** | 给 LLM 挂上能调用外部系统的函数，LLM 决定何时调用 |
| **Runbook** | 运维手册，描述某类故障的标准排查步骤 |
| **BM25** | 传统关键词检索算法，和向量检索互补 |
| **RRF** | Reciprocal Rank Fusion，把多路检索结果融合排名 |
| **PromQL** | Prometheus 的查询语言 |
| **kind** | Kubernetes in Docker，本地跑假 K8s 集群用的工具 |
| **Human-in-the-loop** | 高风险操作需要人工确认，不让 Agent 自动执行 |
| **只读 Agent** | Agent 只能查、不能改，安全边界清晰 |

---

## 八、给 AI 助手的实现注意事项

> 以下是给编程 AI 的补充说明，请严格遵守：

1. **语言**：Python 3.11+，全部用 async/await
2. **依赖管理**：用 `requirements.txt`，不用 Poetry（新手友好）
3. **配置**：所有密钥/URL 走 `.env` 文件，用 `pydantic-settings` 读取，不要硬编码
4. **工具返回值必须截断**：Prometheus/K8s/Loki 的返回可能很大，每个工具函数最多返回 **2000 字符**，超出截断并加 `[TRUNCATED]` 标记
5. **只读原则**：`k8s_tools.py` 里只允许 GET 类操作，不允许 create/delete/patch
6. **错误处理**：每个工具调用都要 try/except，失败时返回 `{"error": "...", "data": null}`，不要让工具异常崩溃整个 Agent
7. **日志**：用 `structlog` 记录每次工具调用的入参/返回摘要，方便 debug
8. **Docker Compose**：必须包含 Prometheus + Milvus/Chroma + 本项目 API，一条命令能启动
9. **README**：Quick Start 要能让完全不懂的人按步骤跑通 demo
10. **不要过度工程**：这是演示项目，优先跑通流程，不需要分布式/高可用设计

---

## 九、简历用的三条 Bullet

> 项目做完后，简历上写这三句（括号里的数字等评测结果出来再填）：

1. 基于 LangGraph 设计多 Agent OnCall 诊断流水线，实现「告警接入 → Skill 路由 → 多工具并行取证 → RAG 检索 Runbook → LLM 生成 RCA 报告」完整链路，默认只读、高风险操作设人工审批门禁。

2. 集成 Prometheus / Kubernetes / Loki 三类只读工具，并使用 Milvus 向量检索 + BM25 混合召回运维手册，相比仅依赖告警文本直接推理的基线，Top-1 根因命中率从（X/10）提升至（Y/10）。

3. 基于 kind 搭建本地故障注入环境，覆盖 CPU 飙高、OOMKilled、CrashLoopBackOff 等 10 类典型 K8s 故障场景，提供可复现评测脚本，平均端到端响应时长约（Z）秒。

---

*最后更新：2026-09-15*  
*作者：新人求职简历项目，参考 HolmesGPT / Mutil-Rag-Agent / AIOpsLab*
