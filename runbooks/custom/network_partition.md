---
id: network_partition
category: custom
fault_type: network
severity: warning
source: custom-oncall-rca
---
# 网络分区与 DNS 故障 / Network Partition

使用 `kubectl exec` 执行 `getent hosts`、`nslookup`、`curl -v`，检查 CoreDNS、Service endpoints、NetworkPolicy 和 CNI。对比同节点与跨节点连通，查 conntrack、丢包、重传和节点路由。

Separate DNS, TCP, TLS and application failures. Check CoreDNS saturation and CNI health. Do not change network policy blindly; preserve timestamps and packet evidence.
