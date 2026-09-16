---
id: Kube_DaemonSet_MisScheduled_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubedaemonsetmisscheduled/
---

# Kube DaemonSet MisScheduled | kube-prometheus runbooks

Kube DaemonSet MisScheduled | kube-prometheus runbooks
Kube DaemonSet MisScheduled
KubeDaemonSetMisScheduled
#
Meaning
#
A number of pods of daemonset are running where they are not supposed to run.
Impact
#
Service degradation or unavailability.
Excessive resource usage where they could be used by other apps.
Diagnosis
#
Usually happens when specifying wrong pod nodeSelector/taints/affinities or
node (node pools) were tainted and existing pods were not scheduled for eviction.
Check daemonset status via
kubectl -n $NAMESPACE describe daemonset $NAME
.
Check
DaemonSet update strategy
Check the status of the pods which belong to the replica sets under the deployment.
Check pod template parameters such as:
pod priority - maybe it was evicted by other more important pods
affinity rules - maybe due to affinities and not enough nodes it is not
possible to schedule pods
Check node taints and labels
Check logs for
node-feature-discovery
and other supporting tools such as gpu-feature-discovery
Mitigation
#
Update DaemonSet and apply change, delete pods manually.
