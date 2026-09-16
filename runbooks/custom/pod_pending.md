---
id: pod_pending
category: custom
fault_type: unknown
severity: warning
source: custom-oncall-rca
---
# Pod Pending 调度排查 / Scheduling Failure

执行 `kubectl describe pod` 查 Events、resources requests、taints/tolerations、nodeSelector、affinity 和 PVC。比较节点 allocatable 与 requested，确认 quota 和 LimitRange。判断是资源不足、存储未绑定还是调度约束。

Read scheduler events and fix the smallest constraint. Validate a new scheduling decision instead of adding capacity blindly.
