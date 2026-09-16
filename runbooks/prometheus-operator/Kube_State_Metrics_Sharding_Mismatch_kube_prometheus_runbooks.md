---
id: Kube_State_Metrics_Sharding_Mismatch_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/kube-state-metrics/kubestatemetricsshardingmismatch/
---

# Kube State Metrics Sharding Mismatch | kube-prometheus runbooks

Kube State Metrics Sharding Mismatch | kube-prometheus runbooks
Kube State Metrics Sharding Mismatch
KubeStateMetricsShardingMismatch
#
Meaning
#
kube-state-metrics sharding is misconfigured.
Impact
#
Unable to get metrics for certain resources.
Some metrics can be unavailable.
Diagnosis
#
Check kube-state-metric container logs for each shard.
Check service account token.
Check networking rules and network policies.
Mitigation
#
TODO
