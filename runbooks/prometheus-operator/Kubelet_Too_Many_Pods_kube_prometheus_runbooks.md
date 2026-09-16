---
id: Kubelet_Too_Many_Pods_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubelettoomanypods/
---

# Kubelet Too Many Pods | kube-prometheus runbooks

Kubelet Too Many Pods | kube-prometheus runbooks
Kubelet Too Many Pods
KubeletTooManyPods
#
Meaning
#
The alert fires when a specific node is running >95% of its capacity of pods
(110 by default).
Full context
Kubelets have a configuration that limits how many Pods they can run.
The default value of this is 110 Pods per Kubelet, but it is configurable
(and this alert takes that configuration into account with the
kube_node_status_capacity_pods
metric).
Impact
#
Running many pods (more than 110) on a single node places a strain on the
Container Runtime Interface (CRI), Container Network Interface (CNI),
and the operating system itself. Approaching that limit may affect performance
and availability of that node.
Diagnosis
#
Check the number of pods on a given node by running:
kubectl get pods --all-namespaces --field-selector spec.nodeName
=
<node>
Mitigation
#
Since Kubernetes only officially supports
110 pods per node
,
you should preferably move pods onto other nodes or expand your cluster with more worker nodes.
If you’re certain the node can handle more pods, you can raise the max pods
per node limit by changing
maxPods
in your
KubeletConfiguration
(for kubeadm-based clusters) or changing the setting in your cloud provider’s
dashboard (if supported).
