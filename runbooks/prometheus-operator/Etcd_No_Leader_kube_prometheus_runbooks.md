---
id: Etcd_No_Leader_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/etcd/etcdnoleader/
---

# Etcd No Leader | kube-prometheus runbooks

Etcd No Leader | kube-prometheus runbooks
Etcd No Leader
etcdNoLeader
#
Meaning
#
This alert is triggered when etcd cluster does not have a leader for more than 1
minute.
This can happen if nodes from the cluster are orphaned - they were part of the cluster
but now they are in minority and thus can not form a cluster,
for example due to network partition.
Impact
#
When there is no leader, Kubernetes API will not be able to work
as expected and cluster cannot process any writes or reads, and any write
requests are queued for processing until a new leader is elected. Operations
that preserve the health of the workloads cannot be performed.
In general loosing quorum will switch etcd to read only, which effectively renders k8s api read only.
It is possible to read the current state, but not possible to update it.
Diagnosis
#
Control plane nodes issue
#
This can occur multiple control plane nodes are powered off or are unable to
connect each other via the network. Check that all control plane nodes are
powered and that network connections between each machine are functional.
Slow disk issue
#
Another potential cause could be slow disk, inspect the
Disk Sync Duration
dashboard, as well as the
Total Leader Elections Per Day
to get more
insight and help with diagnosis.
Other
#
Check the logs of etcd containers to see any further information and to verify
that etcd does not have leader.
Logs should contain something like
etcdserver: no leader
.
Mitigation
#
Disaster and recovery
#
Follow the steps described in the
disaster-recovery
