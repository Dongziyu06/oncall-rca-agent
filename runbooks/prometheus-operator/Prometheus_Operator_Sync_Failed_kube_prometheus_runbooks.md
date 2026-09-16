---
id: Prometheus_Operator_Sync_Failed_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/prometheus-operator/prometheusoperatorsyncfailed/
---

# Prometheus Operator Sync Failed | kube-prometheus runbooks

Prometheus Operator Sync Failed | kube-prometheus runbooks
Prometheus Operator Sync Failed
PrometheusOperatorSyncFailed
#
Meaning
#
Last controller reconciliation failed
Impact
#
Prometheus Operator will not be able to manage Prometheuses/Alertmanagers.
Diagnosis
#
Check logs of Prometheus Operator pod.
Check service account tokens.
Mitigation
#
