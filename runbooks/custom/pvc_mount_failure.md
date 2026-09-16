---
id: pvc_mount_failure
category: custom
fault_type: disk
severity: warning
source: custom-oncall-rca
---
# PVC 挂载失败 / PVC Mount Failure

执行 `kubectl describe pvc`、`kubectl describe pod` 和 `kubectl get events`，检查 StorageClass、PV 状态、access mode、拓扑与 CSI driver 日志。确认是 provision 失败、attach 冲突、权限错误还是 fs type 不匹配。不要直接删除 PVC，先确认备份。

Inspect CSI controller and node logs, attachment state, permissions and filesystem type. Separate provisioning from mount errors and protect data before any destructive action.
