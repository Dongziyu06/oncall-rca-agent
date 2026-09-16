---
id: Prometheus_Operator_Rejected_Resources_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/prometheus-operator/prometheusoperatorrejectedresources/
---

# Prometheus Operator Rejected Resources | kube-prometheus runbooks

Prometheus Operator Rejected Resources | kube-prometheus runbooks
Prometheus Operator Rejected Resources
PrometheusOperatorRejectedResources
#
Meaning
#
Custom Resources managed by Prometheus Operator were rejected and not propagated to operands (prometheus, alertmanager).
Impact
#
Custom Resource won’t be used by prometheus-operator and thus configuration it carries won’t be translated to prometheus or alertmanager configuration.
Diagnosis
#
Check newly created Custom Resources like Prometheus, Alertmanager, Rules, Probes, ServiceMonitors, and others that have a CRD used by Prometheus Operator.
Check logs of Prometheus Operator pod.
Mitigation
#
Fix newly created Custom Resource to conform to the schema defined in a CRD and reapply it to the cluster.
Consider using a tool like
kubeconform
to validate newly created resources. You can check
kube-prometheus integration of such a tool in the CI pipeline
.
