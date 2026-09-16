---
id: Kube_Aggregated_API_Errors_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubeaggregatedapierrors/
---

# Kube Aggregated API Errors | kube-prometheus runbooks

Kube Aggregated API Errors | kube-prometheus runbooks
Kube Aggregated API Errors
KubeAggregatedAPIErrors
#
Meaning
#
Kubernetes aggregated API has reported errors.
It has appeared unavailable over 4 times averaged over the past 10m.
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
Investigate NetworkPolicies if prometheus/additional API was not filtered out.
Mitigation
#
TODO
See
APIServer aggregation
