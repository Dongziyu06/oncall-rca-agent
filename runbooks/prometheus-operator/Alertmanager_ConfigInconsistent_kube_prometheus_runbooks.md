---
id: Alertmanager_ConfigInconsistent_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/alertmanager/alertmanagerconfiginconsistent/
---

# Alertmanager ConfigInconsistent | kube-prometheus runbooks

Alertmanager ConfigInconsistent | kube-prometheus runbooks
Alertmanager ConfigInconsistent
AlertmanagerConfigInconsistent
#
Meaning
#
The configuration between instances inside a cluster is inconsistent.
Impact
#
Configuration inconsistency can be multiple and impact is hard to predict.
Nevertheless, in most cases the alert might be lost or routed to the incorrect integration.
Diagnosis
#
Run a
diff
tool between all
alertmanager.yml
that are deployed to find what is wrong.
You could run a job within your CI to avoid this issue in the future.
Mitigation
#
Delete the incorrect secret and deploy the correct one.
