---
id: hpa_flapping
category: custom
fault_type: cpu
severity: warning
source: custom-oncall-rca
---
# HPA 频繁扩缩容 / HPA Flapping

检查 HPA desired/current replicas、指标窗口、target 和 stabilizationWindowSeconds。对比 CPU 利用率、请求速率和冷启动时间，确认 metrics-server 数据是否抖动。

Inspect desired versus current replicas and tune stabilization only after validating capacity. Do not disable autoscaling to hide saturation.
