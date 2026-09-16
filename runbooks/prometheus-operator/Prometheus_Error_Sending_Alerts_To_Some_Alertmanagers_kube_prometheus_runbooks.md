---
id: Prometheus_Error_Sending_Alerts_To_Some_Alertmanagers_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheuserrorsendingalertstosomealertmanagers/
---

# Prometheus Error Sending Alerts To Some Alertmanagers | kube-prometheus runbooks

Prometheus Error Sending Alerts To Some Alertmanagers | kube-prometheus runbooks
Prometheus Error Sending Alerts To Some Alertmanagers
PrometheusErrorSendingAlertsToSomeAlertmanagers
#
Meaning
#
Prometheus has encountered more than 1% errors sending alerts to a specific Alertmanager.
Impact
#
Some alerts may be lost.
Diagnosis
#
Check connectivity issues between Prometheus and AlertManager.
Check NetworkPolicies, network saturation.
Check if AlertManager is not overloaded or has not enough resources.
Mitigation
#
Set multiple AlertManager instances, spread them across nodes.
