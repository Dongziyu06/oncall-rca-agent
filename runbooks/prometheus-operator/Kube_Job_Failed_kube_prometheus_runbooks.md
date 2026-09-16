---
id: Kube_Job_Failed_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubejobfailed/
---

# Kube Job Failed | kube-prometheus runbooks

Kube Job Failed | kube-prometheus runbooks
Kube Job Failed
KubeJobFailed
#
Meaning
#
Job failed complete.
Impact
#
Failure of processing of a scheduled task.
Diagnosis
#
Check job via
kubectl -n $NAMESPACE describe jobs $JOB
.
Check pod events via
kubectl -n $NAMESPACE describe pod $POD_FROM_JOB
.
Check pod logs via
kubectl -n $NAMESPACE log pod $POD_FROM_JOB
.
Mitigation
#
See
Debugging Pods
See
Job patterns
redesign job so that it is idempotent (can be re-run many times which will
always produce the same output even if input differs)
