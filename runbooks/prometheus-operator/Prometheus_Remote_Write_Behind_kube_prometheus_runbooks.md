---
id: Prometheus_Remote_Write_Behind_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheusremotewritebehind/
---

# Prometheus Remote Write Behind | kube-prometheus runbooks

Prometheus Remote Write Behind | kube-prometheus runbooks
Prometheus Remote Write Behind
PrometheusRemoteStorageFailures
#
Meaning
#
Prometheus remote write is behind.
Impact
#
Metrics and alerts may be missing or inaccurate.
Increased data lag between locations.
Diagnosis
#
Check prometheus logs and remote storage logs.
Investigate network issues.
Check configs and credentials.
Mitigation
#
Probbaly amout of data sent to remote system is too high
for given network connectivity speed.
You may need to limit which metrics to send to minimize transfers.
See
Prometheus Remote Storage Failures
