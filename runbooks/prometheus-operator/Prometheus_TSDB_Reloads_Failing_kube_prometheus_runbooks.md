---
id: Prometheus_TSDB_Reloads_Failing_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheustsdbreloadsfailing/
---

# Prometheus TSDB Reloads Failing | kube-prometheus runbooks

Prometheus TSDB Reloads Failing | kube-prometheus runbooks
Prometheus TSDB Reloads Failing
PrometheusTSDBReloadsFailing
#
Meaning
#
Prometheus has issues reloading blocks from disk.
Impact
#
Metrics and alerts may be missing or inaccurate.
Diagnosis
#
Check storage used by the pod.
Mitigation
#
Increase Prometheus pod memory so that it caches more from disk.
Try expanding volumes if they are too small or too slow.
Change PVC storageClass to a more performant one.
