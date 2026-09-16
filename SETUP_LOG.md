# 环境搭建记录

> 记录本项目从零开始搭建本地开发环境的完整过程，供复现和面试讲解使用。

---

## 一、前置环境

| 工具 | 版本 | 安装方式 |
|------|------|----------|
| Docker Desktop | 已装（需手动启动） | 官网安装包 |
| kubectl | Docker Desktop 自带 | — |
| kind | v0.23.0 | `curl.exe -Lo C:\Windows\System32\kind.exe https://kind.sigs.k8s.io/dl/v0.23.0/kind-windows-amd64` |
| helm | v4.3.0 | `winget install Helm.Helm` |
| Python | 3.11+ | — |

---

## 二、本地 K8s 集群搭建（kind）

```powershell
# 创建集群
kind create cluster --name rca-demo

# 验证
kubectl cluster-info --context kind-rca-demo
kubectl get nodes
# 预期：一个 Ready 节点
```

---

## 三、部署 Prometheus 监控栈

```powershell
# 添加 Helm 仓库
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# 安装（禁用 Grafana，保留 Alertmanager）
helm install prometheus prometheus-community/kube-prometheus-stack `
  --namespace monitoring --create-namespace `
  --set grafana.enabled=false

# 等待所有 Pod Running（约 2-3 分钟）
kubectl get pods -n monitoring
```

最终状态（全部 Running 才算完成）：

```
alertmanager-prometheus-kube-prometheus-alertmanager-0   2/2   Running
prometheus-kube-prometheus-operator-xxx                  1/1   Running
prometheus-kube-state-metrics-xxx                        1/1   Running
prometheus-prometheus-kube-prometheus-prometheus-0       2/2   Running
prometheus-prometheus-node-exporter-xxx                  1/1   Running
```

---

## 四、暴露 Prometheus 到本地

> 每次重启电脑后需要重新执行此步骤。

```powershell
# 新开一个 PowerShell 窗口，保持运行
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090
```

验证：浏览器打开 `http://localhost:9090`，能看到 Prometheus Query 界面即成功。

---

## 五、部署 Demo 微服务（被监控的靶场）

```powershell
kubectl apply -f infra/sample-app/deployment.yaml
kubectl get pods -n default
```

---

## 六、配置 RCA 助手

```powershell
# 复制配置文件
cp .env.example .env

# 编辑 .env，至少配置：
# PROMETHEUS_URL=http://localhost:9090
# KUBECONFIG=~/.kube/config
# （可选）OPENAI_API_KEY 或 DEEPSEEK_API_KEY
```

---

## 七、启动 RCA 助手

```powershell
cd D:\aiops\oncall-rca-agent
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn api.main:app --reload --port 8000
```

---

## 八、验证完整链路

```powershell
# 1. 发送告警
curl.exe -X POST http://127.0.0.1:8000/alert `
  -H "Content-Type: application/json" `
  -d "{\"alerts\":[{\"labels\":{\"alertname\":\"HighCPU\",\"service\":\"demo\"},\"annotations\":{\"description\":\"CPU usage is high\"}}]}"

# 返回示例：{"task_id": "xxx-yyy-zzz"}

# 2. 订阅 SSE 查看调查进度和报告
curl.exe -N http://127.0.0.1:8000/task/<task_id>/stream
```

预期 SSE 事件顺序：
```
Router → MetricAgent → K8sAgent → RunbookAgent → Summarize → Report
```

---

## 九、常用运维命令

```powershell
# 查看集群状态
kubectl get nodes
kubectl get pods -n monitoring
kubectl get pods -n default

# 重新暴露 Prometheus（每次重启后）
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090

# 删除集群（不用时清理资源）
kind delete cluster --name rca-demo

# 重建集群
kind create cluster --name rca-demo
```

---

## 十、注意事项

- Docker Desktop **必须先启动**，kind 才能工作
- `port-forward` 窗口关掉后 9090 就断了，需要重开
- 无 kind/Prometheus 时，RCA 助手自动 mock 回退，仍可演示
- 所有工具只读，不会修改集群资源

---

*创建时间：2026-09-15*
