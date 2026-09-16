---
id: Prometheus_Operator_List_Errors_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/prometheus-operator/prometheusoperatorlisterrors/
---

# Prometheus Operator List Errors | kube-prometheus runbooks

Prometheus Operator List Errors | kube-prometheus runbooks
Prometheus Operator List Errors
PrometheusOperatorListErrors
#
Meaning
#
Errors while performing list operations in controller.
Impact
#
Prometheus Operator has troubles in managing its operands and Custom Resources.
Diagnosis
#
Check logs of Prometheus Operator pod.
Check service account tokens.
Check Prometheus Operator RBAC configuration.
Mitigation
#
