---
id: Prometheus_Not_Connected_To_Alertmanagers_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheusnotconnectedtoalertmanagers/
---

# Prometheus Not Connected To Alertmanagers | kube-prometheus runbooks

Prometheus Not Connected To Alertmanagers | kube-prometheus runbooks
Prometheus Not Connected To Alertmanagers
PrometheusNotConnectedToAlertmanagers
#
Meaning
#
Prometheus is not connected to any Alertmanagers.
Impact
#
Sending alerts is not possible.
Diagnosis
#
Check connectivity issues between Prometheus and AlertManager.
Check NetworkPolicies, network saturation.
Check if AlertManager is not overloaded or has not enough resources.
Mitigation
#
Set multiple AlertManager instances, spread them across nodes.
