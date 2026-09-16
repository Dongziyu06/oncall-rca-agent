---
id: Alertmanager_Failed_To_Send_Alerts_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/alertmanager/alertmanagerfailedtosendalerts/
---

# Alertmanager Failed To Send Alerts | kube-prometheus runbooks

Alertmanager Failed To Send Alerts | kube-prometheus runbooks
Alertmanager Failed To Send Alerts
AlertmanagerFailedToSendAlerts
#
Meaning
#
At least one instance is unable to routed alert to the corresponding integration.
Impact
#
No impact since another instance should be able to send the notification,
unless
AlertmanagerClusterFailedToSendAlerts
is also triggerd for the same integration.
Diagnosis
#
Verify the amount of failed notification per alert-manager-[instance] for
a specific integration.
You can look metrics exposed in prometheus console using promQL.
For exemple the following query will display the number of failed
notifications per instance for pager duty integration.
We have 3 instances involved in the example bellow.
rate
(
alertmanager_notifications_total{integration
=
"
pagerduty
"}[
5m
]
)
Mitigation
#
Depending on the integration, you can have a look to alert-manager logs and act (network, authorization token, firewall…)
Depending on the integration, you can have a look to alert-manager logs
and act (network, authorization token, firewall…)
kubectl -n monitoring logs -l
'alertmanager=main'
-c alertmanager
