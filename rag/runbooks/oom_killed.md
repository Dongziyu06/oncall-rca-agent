# OOMKilled 排查
## 症状
容器退出码 137 或 Pod 出现 OOMKilled。
## 步骤
检查内存曲线、limit、堆快照和泄漏日志，谨慎调整 limit。
