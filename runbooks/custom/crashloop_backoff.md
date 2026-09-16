---
id: crashloop_backoff
category: custom
fault_type: crashloop
severity: warning
source: custom-oncall-rca
---
# CrashLoopBackOff 崩溃循环 / Restart Loop

执行 `kubectl get pod`、`kubectl describe pod` 和 `kubectl logs --previous`，重点查看退出码、启动参数、探针和 ConfigMap/Secret。检查镜像 tag、工作目录、文件权限和最近 rollout。区分进程立即退出与探针失败，恢复已知良好版本前先保留证据。

Inspect exit codes, previous logs, probes and image compatibility. A crash loop is a symptom; use rollout history and approve rollback explicitly.
