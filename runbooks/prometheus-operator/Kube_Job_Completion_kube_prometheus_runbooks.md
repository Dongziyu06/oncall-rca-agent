---
id: Kube_Job_Completion_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubejobcompletion/
---

# Kube Job Completion | kube-prometheus runbooks

Kube Job Completion | kube-prometheus runbooks
Kube Job Completion
KubeJobCompletion
#
Meaning
#
Job is taking more than 1h to complete.
Impact
#
Long processing of batch jobs.
Possible issues with scheduling next Job
Diagnosis
#
Check job via
kubectl -n $NAMESPACE describe jobs $JOB
.
Check pod events via
kubectl -n $NAMESPACE describe job $JOB
.
Mitigation
#
Give it more resources so it finishes faster, if applicable.
See
Job patterns
