---
id: Kube_HPA_Maxed_Out_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubehpamaxedout/
---

# Kube HPA Maxed Out | kube-prometheus runbooks

Kube HPA Maxed Out | kube-prometheus runbooks
Kube HPA Maxed Out
KubeHpaMaxedOut
#
Meaning
#
Horizontal Pod Autoscaler has been running at max replicas for longer
than 15 minutes.
Impact
#
Horizontal Pod Autoscaler won’t be able to add new pods and thus scale application.
Notice
for some services maximizing HPA is in fact desired.
Diagnosis
#
Check why HPA was unable to scale:
max replicas too low
too low value for requests such as CPU?
Mitigation
#
If using basic metrics like CPU/Memory then ensure to set proper values for
requests
.
For memory based scaling ensure there are no memory leaks.
If using custom metrics then fine-tune how app scales accordingly to it.
Use performance tests to see how the app scales.
