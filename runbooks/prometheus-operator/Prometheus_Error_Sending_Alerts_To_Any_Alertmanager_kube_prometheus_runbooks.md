---
id: Prometheus_Error_Sending_Alerts_To_Any_Alertmanager_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheuserrorsendingalertstoanyalertmanager/
---

# Prometheus Error Sending Alerts To Any Alertmanager | kube-prometheus runbooks

Prometheus Error Sending Alerts To Any Alertmanager | kube-prometheus runbooks
Prometheus Error Sending Alerts To Any Alertmanager
PrometheusErrorSendingAlertsToAnyAlertmanager
#
Meaning
#
Prometheus has encountered errors sending alerts to a any Alertmanager.
Impact
#
All alerts may be lost.
Diagnosis
#
Check connectivity issues between Prometheus and AlertManager cluster.
Check NetworkPolicies, network saturation.
Check if AlertManager is not overloaded or has not enough resources.
Mitigation
#
Set multiple AlertManager instances, spread them across nodes.
