---
id: Prometheus_Target_Sync_Failure_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheustargetsyncfailure/
---

# Prometheus Target Sync Failure | kube-prometheus runbooks

Prometheus Target Sync Failure | kube-prometheus runbooks
Prometheus Target Sync Failure
PrometheusTargetSyncFailure
#
Meaning
#
This alert is triggered when at least one of the Prometheus instances has
consistently failed to sync its configuration.
Impact
#
Metrics and alerts may be missing or inaccurate.
Diagnosis
#
Determine whether the alert is for the cluster or user workload Prometheus by
inspecting the alert’s
namespace
label.
Check the logs for the appropriate Prometheus instance:
$ NAMESPACE
=
'<value of namespace label from alert>'
$ oc -n $NAMESPACE logs -l
'app=prometheus'
level
=
error ... msg
=
"Creating target failed"
...
Mitigation
#
If the logs indicate a syntax or other configuration error, correct the
corresponding
ServiceMonitor
,
PodMonitor
, or other configuration
resource. In most all cases, the operator should prevent this from happening.
