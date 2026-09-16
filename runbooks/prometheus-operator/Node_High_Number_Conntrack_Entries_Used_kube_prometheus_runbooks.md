---
id: Node_High_Number_Conntrack_Entries_Used_kube_prometheus_runbooks
category: kubernetes
fault_type: network
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/node/nodehighnumberconntrackentriesused/
---

# Node High Number Conntrack Entries Used | kube-prometheus runbooks

Node High Number Conntrack Entries Used | kube-prometheus runbooks
Node High Number Conntrack Entries Used
NodeHighNumberConntrackEntriesUsed
#
Meaning
#
Number of conntrack are getting close to the limit.
Impact
#
When reached the limit then some connections will be dropped, degrading service quality.
Diagnosis
#
Check current conntrack value on the node.
Check which apps are generating a lot of connections.
Mitigation
#
Migrate some pods to another nodes.
Bump conntrack limit directly on the node, remembering to make it persistent across node reboots.
