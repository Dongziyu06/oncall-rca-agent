---
id: Alertmanager_Cluster_Failed_To_Send_Alerts_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/alertmanager/alertmanagerclusterfailedtosendalerts/
---

# Alertmanager Cluster Failed To Send Alerts | kube-prometheus runbooks

Alertmanager Cluster Failed To Send Alerts | kube-prometheus runbooks
Alertmanager Cluster Failed To Send Alerts
AlertmanagerClusterFailedToSendAlerts
#
Meaning
#
All instances failed to send notification to an integration.
Impact
#
You will not receive a notification when an alert is raised.
Diagnosis
#
No alerts are received at the integration level from the cluster.
Mitigation
#
Depending on the integration, correct the integration with the faulty instance (network, authorization token, firewall…)
