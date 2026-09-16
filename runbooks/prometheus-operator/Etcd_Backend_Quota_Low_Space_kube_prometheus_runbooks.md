---
id: Etcd_Backend_Quota_Low_Space_kube_prometheus_runbooks
category: kubernetes
fault_type: disk
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/etcd/etcdbackendquotalowspace/
---

# Etcd Backend Quota Low Space | kube-prometheus runbooks

Etcd Backend Quota Low Space | kube-prometheus runbooks
Etcd Backend Quota Low Space
etcdBackendQuotaLowSpace
#
Meaning
#
This alert fires when the total existing DB size exceeds 95% of the maximum
DB quota. The consumed space is in Prometheus represented by the metric
etcd_mvcc_db_total_size_in_bytes
, and the DB quota size is defined by
etcd_server_quota_backend_bytes
.
Impact
#
In case the DB size exceeds the DB quota, no writes can be performed anymore on
the etcd cluster. This further prevents any updates in the cluster, such as the
creation of pods.
Diagnosis
#
The following two approaches can be used for the diagnosis.
CLI Checks
#
To run
etcdctl
commands, we need to
rsh
into the
etcdctl
container of any
etcd pod.
$ NAMESPACE
=
"kube-etcd"
$ kubectl rsh -c etcdctl -n $NAMESPACE
$(
kubectl get po -l app
=
etcd -oname -n $NAMESPACE | awk -F
"/"
'NR==1{ print $2 }'
)
Validate that the
etcdctl
command is available:
$ etcdctl version
etcdctl
can be used to fetch the DB size of the etcd endpoints.
$ etcdctl endpoint status -w table
PromQL queries
#
Check the percentage consumption of etcd DB with the following query in the
metrics console:
(
etcd_mvcc_db_total_size_in_bytes
/
etcd_server_quota_backend_bytes
)
*
100
Check the DB size in MB that can be reduced after defragmentation:
(
etcd_mvcc_db_total_size_in_bytes
-
etcd_mvcc_db_total_size_in_use_in_bytes
)/
1024
/
1024
Mitigation
#
Capacity planning
#
If the
etcd_mvcc_db_total_size_in_bytes
shows that you are growing close to
the
etcd_server_quota_backend_bytes
, etcd almost reached max capacity and it’s
start planning for new cluster.
In the meantime before migration happens, you can use defrag to gain some time.
Defrag
#
When the etcd DB size increases, we can defragment existing etcd DB to optimize
DB consumption as described in
etcdDefragmentation
.
Run the following command in all etcd pods.
$ etcdctl defrag
As validation, check the endpoint status of etcd members to know the reduced
size of etcd DB. Use for this purpose the same diagnostic approaches as listed
above. More space should be available now.
