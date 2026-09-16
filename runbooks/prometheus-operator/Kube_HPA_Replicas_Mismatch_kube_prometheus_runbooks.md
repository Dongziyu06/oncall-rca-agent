---
id: Kube_HPA_Replicas_Mismatch_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubehpareplicasmismatch/
---

# Kube HPA  Replicas Mismatch | kube-prometheus runbooks

Kube HPA  Replicas Mismatch | kube-prometheus runbooks
Kube HPA  Replicas Mismatch
KubeHpaReplicasMismatch
#
Meaning
#
Horizontal Pod Autoscaler has not matched the desired number of replicas for
longer than 15 minutes.
Impact
#
HPA was unable to schedule desired number of pods.
Diagnosis
#
Check why HPA was unable to scale:
not enough nodes in the cluster
hitting resource quotas in the cluster
pods evicted due to pod priority
Mitigation
#
In case of cluster-autoscaler you may need to set up preemtive pod pools to
ensure nodes are created on time.
