---
id: Kube_StatefulSet_Generation_Mismatch_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubestatefulsetgenerationmismatch/
---

# Kube StatefulSet Generation Mismatch | kube-prometheus runbooks

Kube StatefulSet Generation Mismatch | kube-prometheus runbooks
Kube StatefulSet Generation Mismatch
KubeStatefulSetGenerationMismatch
#
Meaning
#
StatefulSet generation mismatch due to possible roll-back.
Impact
#
Service degradation or unavailability.
Diagnosis
#
See
Kubernetes Docs - Failed Deployment
which can be also applied to StatefulSets to some extent
Check out rollout history
kubectl -n $NAMESPACE rollout history statefulset $NAME
Check rollout status if it is not paused
Check deployment status via
kubectl -n $NAMESPACE describe statefulset $NAME
.
Check how many replicas are there declared.
Investigate if new pods are not crashing.
Look at the issues with PersistentVolumes attached to StatefulSets.
Check the status of the pods which belong to the replica sets under the deployment.
Check pod template parameters such as:
pod priority - maybe it was evicted by other more important pods
resources - maybe it tries to use unavailable resource, such as GPU
but there is limited number of nodes with GPU
affinity rules - maybe due to affinities and not enough nodes it is
not possible to schedule pods
pod termination grace period - if too long then pods may be for too long
in terminating state
Check if Horizontal Pod Autoscaler (HPA) is not triggered due to untested
values (requests values).
Check if cluster-autoscaler is able to create new nodes - see its logs or
cluster-autoscaler status configmap.
Mitigation
#
Statefulsets are quite specific, and usually have special scripts on pod termination.
See if there are special commands executed such as data migration, which may significantly slow down the progress.
In case of scale out usually adding new nodes solves the issue.
Otherwise probably statefulset definition needs to be fixed.
In rare cases roll back to previous version - see
Kubernetes Docs - Rolling Back
In extremely rare situations it may be better to delete problematic pods.
See
Debugging Pods
