---
id: Kube_Container_Waiting_kube_prometheus_runbooks
category: kubernetes
fault_type: crashloop
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubecontainerwaiting/
---

# Kube Container Waiting | kube-prometheus runbooks

Kube Container Waiting | kube-prometheus runbooks
Kube Container Waiting
KubeContainerWaiting
#
Meaning
#
Container in pod is in Waiting state for too long.
Impact
#
Service degradation or unavailability.
Diagnosis
#
Check pod events via
kubectl -n $NAMESPACE describe pod $POD
.
Check pod logs via
kubectl -n $NAMESPACE logs $POD -c $CONTAINER
Check for missing files such as configmaps/secrets/volumes
Check for pod requests, especially special ones such as GPU.
Check for node taints and capabilities.
Mitigation
#
See
Container waiting
