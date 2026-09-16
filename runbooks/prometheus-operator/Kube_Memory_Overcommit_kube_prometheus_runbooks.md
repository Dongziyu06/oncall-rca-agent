---
id: Kube_Memory_Overcommit_kube_prometheus_runbooks
category: kubernetes
fault_type: oom
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubememoryovercommit/
---

# Kube Memory Overcommit | kube-prometheus runbooks

Kube Memory Overcommit | kube-prometheus runbooks
Kube Memory Overcommit
KubeMemoryOvercommit
#
Meaning
#
Cluster has overcommitted Memory resource requests for Pods
and cannot tolerate node failure.
Full context
Total number of Memory requests for pods exceeds cluster capacity.
In case of node failure some pods will not fit in the remaining nodes.
Impact
#
The cluster cannot tolerate node failure. In the event of a node failure,
some Pods will be in
Pending
state.
Diagnosis
#
Check if Memory resource requests are adjusted to the app usage
Check if some nodes are available and not cordoned
Check if cluster-autoscaler has issues with adding new nodes
Mitigation
#
Add more nodes to the cluster - usually it is better to have more smaller
nodes, than few bigger.
Add different node pools with different instance types to avoid problem
when using only one instance type in the cloud.
Use pod priorities to avoid important services from losing performance,
see
pod priority and preemption
Fine tune settings for special pods used with
cluster-autoscaler
Prepare performance tests for the expected workload, plan cluster capacity
accordingly.
