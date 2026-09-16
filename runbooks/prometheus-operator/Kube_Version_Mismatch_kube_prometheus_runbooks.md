---
id: Kube_Version_Mismatch_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubeversionmismatch/
---

# Kube Version Mismatch | kube-prometheus runbooks

Kube Version Mismatch | kube-prometheus runbooks
Kube Version Mismatch
KubeVersionMismatch
#
Meaning
#
Different semantic versions of Kubernetes components running.
Usually happens during kubernetes cluster upgrade process.
Full context
Kubernetes control plane nodes or worker nodes use different versions.
This usually happens when kubernetes cluster is upgraded between minor and
major version.
Impact
#
Incompatible API versions between kubernetes components may have very
broad range of issues, influencing single containers, through app stability,
ending at whole cluster stability.
Diagnosis
#
Check existing kubernetes versions via
kubectl get nodes
and see
VERSION column
Check if there is ongoing kubernetes upgrade - especially in managed services
in the cloud
Mitigation
#
Drain affected nodes, then upgrade or replace them with newer ones,
see
Safely drain node
Ensure to set proper control plane version and node pool versions when
creating clusters.
Ensure auto cluster updates for control plane and node pools.
Set proper maintenance windows for the clusters.
