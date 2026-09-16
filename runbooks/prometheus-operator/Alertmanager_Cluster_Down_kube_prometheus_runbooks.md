---
id: Alertmanager_Cluster_Down_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/alertmanager/alertmanagerclusterdown/
---

# Alertmanager Cluster Down | kube-prometheus runbooks

Alertmanager Cluster Down | kube-prometheus runbooks
Alertmanager Cluster Down
AlertmanagerClusterDown
#
Meaning
#
Half or more of the Alertmanager instances within the same cluster are down.
Impact
#
You have an unstable cluster, if everything goes wrong you will lose the whole cluster.
Diagnosis
#
Verify why pods are not running.
You can get a big picture with
events
.
$ kubectl get events --field-selector involvedObject.kind
=
Pod | grep alertmanager
Mitigation
#
There are no cheap options to mitigate this risk.
Verifying any new changes in preprod before production environment should improve stability.
