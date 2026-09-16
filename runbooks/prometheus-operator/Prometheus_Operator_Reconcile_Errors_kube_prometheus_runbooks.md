---
id: Prometheus_Operator_Reconcile_Errors_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/prometheus-operator/prometheusoperatorreconcileerrors/
---

# Prometheus Operator Reconcile Errors | kube-prometheus runbooks

Prometheus Operator Reconcile Errors | kube-prometheus runbooks
Prometheus Operator Reconcile Errors
PrometheusOperatorReconcileErrors
#
Meaning
#
Errors while reconciling controller.
Impact
#
Prometheus Operator will not be able to manage Prometheuses/Alertmanagers.
Diagnosis
#
Check logs of Prometheus Operator pod.
Check service account tokens.
Mitigation
#
