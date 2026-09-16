---
id: Kube_Persistent_Volume_Errors_kube_prometheus_runbooks
category: kubernetes
fault_type: disk
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubepersistentvolumeerrors/
---

# Kube Persistent Volume Errors | kube-prometheus runbooks

Kube Persistent Volume Errors | kube-prometheus runbooks
Kube Persistent Volume Errors
KubePersistentVolumeErrors
#
Meaning
#
PersistentVolume is having issues with provisioning.
Impact
#
Volue may be unavailable or have data erors (corrupted storage).
Service degradation, data loss.
Diagnosis
#
Check PV events via
kubectl describe pv $PV
.
Check storage provider for logs.
Check storage quotas in the cloud.
Mitigation
#
In happy scenario storage is just not provisioned as fast as expected.
In worst scenario there is data corruption or data loss. Restore from backup.
