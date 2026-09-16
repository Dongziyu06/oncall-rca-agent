---
id: Kube_Quota_Exceeded_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubequotaexceeded/
---

# Kube Quota Exceeded | kube-prometheus runbooks

Kube Quota Exceeded | kube-prometheus runbooks
Kube Quota Exceeded
KubeQuotaExceeded
#
Meaning
#
Cluster reaches to the allowed hard limits for given namespace.
Impact
#
Inability to create resources in kubernetes.
Diagnosis
#
Check resource usage for the namespace in given time span
Mitigation
#
Review existing quota for given namespace and adjust it accordingly.
Review resources used by the quota and fine tune them.
Continue with standard capacity planning procedures.
See
Quotas
