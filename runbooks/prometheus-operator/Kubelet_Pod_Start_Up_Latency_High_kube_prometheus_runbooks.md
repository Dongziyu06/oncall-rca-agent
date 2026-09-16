---
id: Kubelet_Pod_Start_Up_Latency_High_kube_prometheus_runbooks
category: kubernetes
fault_type: timeout
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubeletpodstartuplatencyhigh/
---

# Kubelet Pod Start Up Latency High | kube-prometheus runbooks

Kubelet Pod Start Up Latency High | kube-prometheus runbooks
Kubelet Pod Start Up Latency High
KubeletPodStartUpLatencyHigh
#
Meaning
#
Kubelet Pod startup 99th percentile latency is XX seconds on node.
Impact
#
Slow pod starts.
Diagnosis
#
Usually exhaused IOPS for node storage.
Mitigation
#
Cordon and drain node
and delete it.
If issue persists look into the node logs.
