---
id: Kube_Memory_Quota_Overcommit_kube_prometheus_runbooks
category: kubernetes
fault_type: oom
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubememoryquotaovercommit/
---

# Kube Memory Quota Overcommit | kube-prometheus runbooks

Kube Memory Quota Overcommit | kube-prometheus runbooks
Kube Memory Quota Overcommit
KubeMemoryQuotaOvercommit
#
Meaning
#
Cluster has overcommitted memory resource requests for Namespaces.
Impact
#
Various services degradation or unavailability in case of single node failure.
Diagnosis
#
Check if Memory resource requests are adjusted to the app usage
Check if some nodes are available and not cordoned
Check if cluster-autoscaler has issues with adding new nodes
Check if the given namespace usage grows in time more than expected
Mitigation
#
Review existing quota for given namespace and adjust it accordingly.
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
