---
id: Prometheus_Operator_Node_Lookup_Errors_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/prometheus-operator/prometheusoperatornodelookuperrors/
---

# Prometheus Operator Node Lookup Errors | kube-prometheus runbooks

Prometheus Operator Node Lookup Errors | kube-prometheus runbooks
Prometheus Operator Node Lookup Errors
PrometheusOperatorNodeLookupErrors
#
Meaning
#
Errors while reconciling information about kubernetes nodes.
Impact
#
Prometheus Operator is not able to configure Prometheus scrape configuration.
Diagnosis
#
Check logs of Prometheus Operator pod.
Check kubelet Service managed by Prometheus Operator
$ kubelet describe Service -n kube-system -l app.kubernetes.io/managed-by
=
prometheus-operator
## Mitigation
TODO
