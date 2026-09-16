---
id: Node_Network_Transmit_Errors_kube_prometheus_runbooks
category: kubernetes
fault_type: network
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/node/nodenetworktransmiterrs/
---

# Node Network Transmit Errors | kube-prometheus runbooks

Node Network Transmit Errors | kube-prometheus runbooks
Node Network Transmit Errors
NodeNetworkTransmitErrs
#
Meaning
#
Network interface is reporting many transmit errors.
Impact
#
Applications on the node may no longer be able to operate with other services.
Network attached storage performance issues or even data loss.
Diagnosis
#
Investigate networking issues on the node and to connected hardware.
Check network interface saturation.
Check CPU usage saturation.
Check physical cables, check networking firewall rules and so on.
Mitigation
#
In general mitigation landscape is quite vast, some suggestions:
Ensure some node capacity is left unallocated (cpu/memory) for handling
networking.
Increase TX queue length
Spread services to other nodes/pods.
Replace physical cables, change ports.
Look into introducting Quality of Service or other
TCP congestion avoidance algorithms
