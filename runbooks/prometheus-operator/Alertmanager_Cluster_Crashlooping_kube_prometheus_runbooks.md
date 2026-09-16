---
id: Alertmanager_Cluster_Crashlooping_kube_prometheus_runbooks
category: kubernetes
fault_type: crashloop
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/alertmanager/alertmanagerclustercrashlooping/
---

# Alertmanager Cluster Crashlooping | kube-prometheus runbooks

Alertmanager Cluster Crashlooping | kube-prometheus runbooks
Alertmanager Cluster Crashlooping
AlertmanagerClusterCrashlooping
#
Meaning
#
Half or more of the Alertmanager instances within the same cluster are crashlooping.
Impact
#
Alerts could be notified multiple time unless pods are crashing to fast and no alerts can be sent.
Diagnosis
#
kubectl get pod -l app
=
alertmanager

NAMESPACE   NAME                    READY   STATUS              RESTARTS    AGE
default     alertmanager-main-0     1/2     CrashLoopBackOff
37107
2d
default     alertmanager-main-1     2/2     Running
0
43d
default     alertmanager-main-2     2/2     Running
0
43d
Find the root cause by looking to events for a given pod/deployement
kubectl get events --field-selector involvedObject.name
=
alertmanager-main-0
Mitigation
#
Make sure pods have enough resources (CPU, MEM) to work correctly.
