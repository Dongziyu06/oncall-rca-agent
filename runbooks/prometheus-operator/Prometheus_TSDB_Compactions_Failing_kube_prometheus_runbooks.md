---
id: Prometheus_TSDB_Compactions_Failing_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheustsdbcompactionsfailing/
---

# Prometheus TSDB Compactions Failing | kube-prometheus runbooks

Prometheus TSDB Compactions Failing | kube-prometheus runbooks
Prometheus TSDB Compactions Failing
PrometheusTSDBCompactionsFailing
#
Meaning
#
Prometheus has issues compacting blocks.
Impact
#
Metrics and alerts may be missing or inaccurate.
Diagnosis
#
Check storage used by the pod.
This can happen if there is a lot of going on in the cluster and
prometheus did not manage to compact data.
Mitigation
#
At first just wait, it may fix itself after some time.
Increase Prometheus pod memory so that it caches more from disk.
Try expanding volumes if they are too small or too slow.
Change PVC storageClass to a more performant one.
