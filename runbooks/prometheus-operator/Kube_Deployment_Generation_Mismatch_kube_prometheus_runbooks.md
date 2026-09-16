---
id: Kube_Deployment_Generation_Mismatch_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubedeploymentgenerationmismatch/
---

# Kube Deployment Generation Mismatch | kube-prometheus runbooks

Kube Deployment Generation Mismatch | kube-prometheus runbooks
Kube Deployment Generation Mismatch
KubeDeploymentGenerationMismatch
#
Meaning
#
Deployment generation mismatch due to possible roll-back.
Impact
#
Service degradation or unavailability.
Diagnosis
#
See
Kubernetes Docs - Failed Deployment
Check out rollout history
kubectl -n $NAMESPACE rollout history deployment $NAME
Check rollout status if it is not paused
Check deployment status via
kubectl -n $NAMESPACE describe deployment $NAME
.
Check how many replicas are there declared.
Investigate if new pods are not crashing.
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
Depending on the conditions usually adding new nodes solves the issue.
Otherwise probably deployment or HPA definition needs to be fixed.
If you can not add nodes then you can change rolling update strategy to
Recreate
.
Sometimes manually deleting pod helps :)
In rare cases roll back to previous version - see
Kubernetes Docs - Rolling Back
In extremely rare situations scale oldest ReplicaSets to 0 and delete them.
See
Debugging Pods
