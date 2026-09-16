---
id: node_not_ready
category: custom
fault_type: network
severity: warning
source: custom-oncall-rca
---
# Node NotReady 节点未就绪

查看 `kubectl describe node`、Conditions、Lease、kubelet 日志和节点磁盘/内存压力。检查容器运行时、CNI、证书和 API Server 连通。若需 cordon/drain，先确认 Pod 分布和中断风险。

Inspect node conditions, leases, runtime, kubelet, certificates and CNI. Decide whether the node is transiently unhealthy or must be replaced; cordon and drain require approval.
