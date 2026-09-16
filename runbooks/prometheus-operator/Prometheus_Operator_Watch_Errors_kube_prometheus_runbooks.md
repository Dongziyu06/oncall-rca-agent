---
id: Prometheus_Operator_Watch_Errors_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/prometheus-operator/prometheusoperatorwatcherrors/
---

# Prometheus Operator Watch Errors | kube-prometheus runbooks

Prometheus Operator Watch Errors | kube-prometheus runbooks
Prometheus Operator Watch Errors
PrometheusOperatorWatchErrors
#
Meaning
#
Errors while performing watch operations in controller.
Impact
#
Prometheus Operator will not be able to manage Prometheuses/Alertmanagers.
Diagnosis
#
Check logs of Prometheus Operator pod.
Check service account tokens.
Mitigation
#
