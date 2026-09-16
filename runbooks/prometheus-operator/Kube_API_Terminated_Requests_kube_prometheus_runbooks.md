---
id: Kube_API_Terminated_Requests_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubeapiterminatedrequests/
---

# Kube API Terminated Requests | kube-prometheus runbooks

Kube API Terminated Requests | kube-prometheus runbooks
Kube API Terminated Requests
KubeAPITerminatedRequests
#
Meaning
#
The apiserver has terminated over 20% of its incoming requests.
Impact
#
Client will not be able to interact with the cluster.
Some in-cluster services this may degrade or make service unavailable.
Diagnosis
#
Use the
apiserver_flowcontrol_rejected_requests_total
metric to determine
which flow schema is throttling the traffic to the API Server.
The flow schema also provides information on the affected resources and subjects.
Mitigation
#
TODO
