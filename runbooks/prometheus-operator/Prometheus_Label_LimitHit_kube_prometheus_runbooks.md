---
id: Prometheus_Label_LimitHit_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheuslabellimithit/
---

# Prometheus Label LimitHit | kube-prometheus runbooks

Prometheus Label LimitHit | kube-prometheus runbooks
Prometheus Label LimitHit
PrometheusLabelLimitHit
#
Meaning
#
Prometheus has dropped targets because some scrape configs have exceeded the labels limit.
Impact
#
Metrics and alerts may be missing or inaccurate.
Diagnosis
#
Mitigation
#
Start thinking about sharding prometheus.
Increase scrape times to perform it less frequently.
