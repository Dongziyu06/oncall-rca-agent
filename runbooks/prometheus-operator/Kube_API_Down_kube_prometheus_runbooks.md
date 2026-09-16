---
id: Kube_API_Down_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubeapidown/
---

# Kube API Down | kube-prometheus runbooks

Kube API Down | kube-prometheus runbooks
Kube API Down
KubeAPIDown
#
Meaning
#
The
KubeAPIDown
alert is triggered when all Kubernetes API servers have not
been reachable by the monitoring system for more than 15 minutes.
Impact
#
This is a critical alert. The Kubernetes API is not responding. The
cluster may partially or fully non-functional.
Applications, which do not use kubernetes API directly, will continue to work. Changing kubernetes resources is not possible.
in the cluster.
Services using Kubernetes API directly will start to behave erratically.
Diagnosis
#
Check the status of the API server targets in the Prometheus UI.
Then, confirm whether the API is also unresponsive for you:
$ kubectl cluster-info
If you can still reach the API server, there may be a network issue between the
Prometheus instances and the API server pods. Check the status of the API server
pods.
$ kubectl -n kube-system get pods
$ kubectl -n kube-system logs -l
'component=kube-apiserver'
Check networking on the node.
Check firewall on the node.
Investigate kube proxy logs.
Investigate NetworkPolicies if prometheus/kubeApi was not filtered out.
Mitigation
#
If you can still reach the API server intermittently, you may be able treat this
like any other failing deployment. If not, it’s possible you may have to refer
to the disaster recovery documentation.
