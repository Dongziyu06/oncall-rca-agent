---
id: Prometheus_Notification_Queue_Running_Full_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheusnotificationqueuerunningfull/
---

# Prometheus Notification Queue Running Full | kube-prometheus runbooks

Prometheus Notification Queue Running Full | kube-prometheus runbooks
Prometheus Notification Queue Running Full
PrometheusNotificationQueueRunningFull
#
Meaning
#
Prometheus alert notification queue predicted to run full in less than 30m.
Impact
#
Fail to send alerts.
Diagnosis
#
Check prometheus container logs for an explanation of which part of the
configuration is problematic.
Mitigation
#
Remove conflicting configuration option.
Check if there is an option to decrease number of alerts firing,
for example by sharding prometheus.
