---
id: Kube_Client_Certificate_Expiration_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubeclientcertificateexpiration/
---

# Kube Client Certificate Expiration | kube-prometheus runbooks

Kube Client Certificate Expiration | kube-prometheus runbooks
Kube Client Certificate Expiration
KubeClientCertificateExpiration
#
Meaning
#
A client certificate used to authenticate to the apiserver is expiring in less than 7 days (warning alert) or 24 hours (critical alert).
Impact
#
Client will not be able to interact with the cluster.
In cluster services communicating with Kubernetes API may degrade or become unavailable.
Diagnosis
#
Check when certificate was issued and when it expires.
Check serviceAccounts and service account tokens.
Mitigation
#
Update client certificate.
For in-cluster clients recreate pods.
