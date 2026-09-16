---
id: Kubelet_Server_Certificate_Expiration_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubeletservercertificateexpiration/
---

# Kubelet Server Certificate Expiration | kube-prometheus runbooks

Kubelet Server Certificate Expiration | kube-prometheus runbooks
Kubelet Server Certificate Expiration
KubeletServerCertificateExpiration
#
Meaning
#
Server certificate for Kubelet on node expires soon or already expired.
Impact
#
Critical
- Cluster will be in inoperable state.
Diagnosis
#
Check when certificate was issued and when it expires.
Mitigation
#
Update certificates in the cluster control nodes and the worker nodes.
Refer to the documentation of the tool used to create cluster.
Another option is to delete node if it affects only one,
In extreme situations recreate cluster.
