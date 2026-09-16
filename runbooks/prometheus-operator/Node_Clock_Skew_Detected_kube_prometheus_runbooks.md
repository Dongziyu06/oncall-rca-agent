---
id: Node_Clock_Skew_Detected_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/node/nodeclockskewdetected/
---

# Node Clock Skew Detected | kube-prometheus runbooks

Node Clock Skew Detected | kube-prometheus runbooks
Node Clock Skew Detected
NodeClockSkewDetected
#
Meaning
#
Clock skew detected.
Impact
#
Time is skewed on the node. This can cause issues with handling TLS as well as problems with other time-sensitive applications.
Diagnosis
#
TODO
Mitigation
#
Ensure time synchronization service is running.
Set proper time servers.
Esure to sync time on server start, especially when using
low power mode or hibernation.
Some resource consuming process can cause issues on given hardware,
so move it to different servers.
On physical servers check if on-board battery requires replacement.
Check for hardware errors.
Check for firmware updates.
Ensure to use newer hardware (like server mainboard and so on).
