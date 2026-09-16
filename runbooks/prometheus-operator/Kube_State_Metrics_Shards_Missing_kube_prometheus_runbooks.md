---
id: Kube_State_Metrics_Shards_Missing_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/kube-state-metrics/kubestatemetricsshardsmissing/
---

# Kube State Metrics Shards Missing | kube-prometheus runbooks

Kube State Metrics Shards Missing | kube-prometheus runbooks
Kube State Metrics Shards Missing
KubeStateMetricsShardsMissing
#
Meaning
#
kube-state-metrics shards are missing.
Impact
#
Unable to get metrics for certain resources.
Some metrics can be unavailable.
Diagnosis
#
Check kube-state-metric container logs for each shard.
Check if certain pods were forcefully evicted.
Check service account token.
Check networking rules and network policies.
Mitigation
#
TODO
