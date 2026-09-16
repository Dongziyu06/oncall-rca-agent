---
id: disk_pressure
category: custom
fault_type: disk
severity: warning
source: custom-oncall-rca
---
# 磁盘压力 / Disk Pressure

检查 `df -h`、`df -i`、kubelet eviction 事件以及容器 writable layer。用 PromQL 查节点文件系统使用率和 inode。定位日志、临时文件、镜像缓存或 PVC 增长，只清理可重建数据。

Check capacity, inodes, evictions, logs and image caches. Apply retention and rotation policies. Never delete unknown paths during an incident without approval and backup validation.
