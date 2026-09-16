---
id: high_cpu_load
category: custom
fault_type: cpu
severity: warning
source: custom-oncall-rca
---
# CPU 高负载排查 / High CPU Load

检查 Pod 的 CPU 使用率、throttling、requests/limits 和热点线程。使用 PromQL `sum(rate(container_cpu_usage_seconds_total{container!=""}[5m])) by (pod)` 和 `rate(container_cpu_cfs_throttled_seconds_total[5m])`定位受限 Pod。执行 `kubectl top pod -A`、`kubectl describe pod` 和进程分析，关联发布、流量与 HPA 变化。不要盲目提高 limit 掩盖死循环。

Check saturation, throttling, limits, hot threads, deployment and traffic timelines. Capture query results and timestamps. Validate application behavior before changing resources, and require approval for production changes.
