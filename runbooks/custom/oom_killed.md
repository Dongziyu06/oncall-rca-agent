---
id: oom_killed
category: custom
fault_type: oom
severity: warning
source: custom-oncall-rca
---
# OOMKilled 内存耗尽 / Memory Exhaustion

通过 `kubectl describe pod` 确认 Last State、退出码 137 和 kubelet 事件。对比 `container_memory_working_set_bytes`、RSS 与 memory limit，查看 `kubectl logs --previous`、heap dump 和 pprof。区分 cgroup OOM 与节点 MemoryPressure，检查漏洞、批次大小与并发数。

Confirm exit code 137 and correlate memory curves with releases. Reducing concurrency may mitigate the incident, but increasing limits alone is not a root-cause fix. Preserve logs and heap evidence.
