---
id: Info_Inhibitor_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/general/infoinhibitor/
---

# Info Inhibitor | kube-prometheus runbooks

Info Inhibitor | kube-prometheus runbooks
Info Inhibitor
InfoInhibitor
#
Meaning
#
This is an alert that is used to inhibit info alerts.
By themselves, the info-level alerts are sometimes very noisy,
but they are relevant when combined with other alerts.
Full context
More information about the alert and design considerations can be found in a
kube-prometheus issue
Impact
#
Alert does not have any impact and it is used only as a workaround to a missing feature in alertmanager.
Diagnosis
#
This alert fires whenever there’s a
severity="info"
alert,
and stops firing when another alert with severity of
warning
or
critical
starts firing on the same namespace.
Mitigation
#
This alert should be routed to a null receiver and configured to inhibit
alerts with
severity="info"
. Such configuration is available at
https://github.com/prometheus-operator/kube-prometheus/blob/main/manifests/alertmanager-secret.yaml
