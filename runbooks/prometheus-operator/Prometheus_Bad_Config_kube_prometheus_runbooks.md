---
id: Prometheus_Bad_Config_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheusbadconfig/
---

# Prometheus Bad Config | kube-prometheus runbooks

Prometheus Bad Config | kube-prometheus runbooks
Prometheus Bad Config
PrometheusBadConfig
#
Meaning
#
Alert fires when Prometheus cannot successfully reload the configuration file
due to the file having incorrect content.
Impact
#
Configuration cannot be reloaded and prometheus operates with last known good
configuration.
Configuration changes in any of Prometheus, Probe, PodMonitor,
or ServiceMonitor objects may not be picked up by prometheus server.
Diagnosis
#
Check prometheus container logs for an explanation of which part of the
configuration is problematic.
Usually this can occur when ServiceMonitors or
PodMonitors share the same job label.
Mitigation
#
Remove conflicting configuration option.
