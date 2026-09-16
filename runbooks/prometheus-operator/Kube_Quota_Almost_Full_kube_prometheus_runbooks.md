---
id: Kube_Quota_Almost_Full_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubequotaalmostfull/
---

# Kube Quota Almost Full | kube-prometheus runbooks

Kube Quota Almost Full | kube-prometheus runbooks
Kube Quota Almost Full
KubeQuotaAlmostFull
#
Meaning
#
Cluster reaches to the allowed limits for given namespace.
Impact
#
In the future deployments may not be possbile.
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
