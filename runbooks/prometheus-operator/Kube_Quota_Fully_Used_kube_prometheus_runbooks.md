---
id: Kube_Quota_Fully_Used_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubequotafullyused/
---

# Kube Quota Fully Used | kube-prometheus runbooks

Kube Quota Fully Used | kube-prometheus runbooks
Kube Quota Fully Used
KubeQuotaFullyUsed
#
Meaning
#
Cluster reached allowed limits for given namespace.
Impact
#
New app installations may not be possible.
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
