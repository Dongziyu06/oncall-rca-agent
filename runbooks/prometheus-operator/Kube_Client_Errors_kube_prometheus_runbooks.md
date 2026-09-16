---
id: Kube_Client_Errors_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubeclienterrors/
---

# Kube Client Errors | kube-prometheus runbooks

Kube Client Errors | kube-prometheus runbooks
Kube Client Errors
KubeClientErrors
#
Meaning
#
Kubernetes API server client is experiencing over 1% error rate in the last 15 minutes.
Impact
#
Specific kubernetes client may malfunction. Service degradation.
Diagnosis
#
Usual issues:
networking errors
too low resources to perform given API calls (usually too low CPU/memory requests)
wrong api client (old libraries)
investigate if the app does not request more data than it really requires
from kubernetes API, for example it has too wide permissions and scans for
resources in all namespaces.
Check logs from client side (sometimes app logs).
Mitigation
#
TODO
