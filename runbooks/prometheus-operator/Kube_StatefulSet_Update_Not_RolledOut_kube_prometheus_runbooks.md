---
id: Kube_StatefulSet_Update_Not_RolledOut_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubestatefulsetupdatenotrolledout/
---

# Kube StatefulSet Update Not RolledOut | kube-prometheus runbooks

Kube StatefulSet Update Not RolledOut | kube-prometheus runbooks
Kube StatefulSet Update Not RolledOut
KubeStatefulSetUpdateNotRolledOut
#
Meaning
#
StatefulSet update has not been rolled out.
Impact
#
Service degradation or unavailability.
Diagnosis
#
Check statefulset via
kubectl -n $NAMESPACE describe statefulset $NAME
.
Check if statefuls update was not paused manually (see status)
Check how many replicas are there declared.
Check the status of the pods which belong to the replica sets under the
statefulset.
Check pod template parameters such as:
pod priority - maybe it was evicted by other more importand pods
resources - maybe it tries to use unavailabe resource, such as GPU but
there is limited number of nodes with GPU
affinity rules - maybe due to affinities and not enough nodes it is
not possible to schedule pods
pod termination grace period - if too long then pods may be for too long
in terminating state
Check if there are issues with attaching disks to statefulset - for example
disk was in Zone A, but pod is scheduled in Zone B.
Check if Horizontal Pod Autoscaler (HPA) is not triggered due to untested
values (requests values).
Check if cluster-autoscaler is able to create new nodes - see its logs or
cluster-autoscaler status configmap.
Mitigation
#
TODO
See
Debugging Pods
