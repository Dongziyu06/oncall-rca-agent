---
id: Kube_Aggregated_API_Down_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubeaggregatedapidown/
---

# Kube Aggregated API Down | kube-prometheus runbooks

Kube Aggregated API Down | kube-prometheus runbooks
Kube Aggregated API Down
KubeAggregatedAPIDown
#
Meaning
#
Kubernetes aggregated API has reported errors.
It has appeared unavailable X times averaged over the past 10m.
Impact
#
From minor such as inability to see cluster metrics to more severe such as
unable to use custom metrics to scale or even unable to use cluster.
Diagnosis
#
Check networking on the node.
Check firewall on the node.
Investigate additional API logs.
Investigate NetworkPolicies if kubeApi - additional API was not filtered out.
Investigate NetworkPolicies if prometheus/additional api was not filtered out.
Mitigation
#
TODO
See
APIServer aggregation
