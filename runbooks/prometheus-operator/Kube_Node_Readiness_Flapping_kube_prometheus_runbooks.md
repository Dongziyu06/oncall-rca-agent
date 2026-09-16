---
id: Kube_Node_Readiness_Flapping_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubenodereadinessflapping/
---

# Kube Node Readiness Flapping | kube-prometheus runbooks

Kube Node Readiness Flapping | kube-prometheus runbooks
Kube Node Readiness Flapping
KubeNodeReadinessFlapping
#
Meaning
#
The readiness status of node  has changed few times in the last 15 minutes.
Impact
#
The performance of the cluster deployments is affected, depending on the overall
workload and the type of the node.
Diagnosis
#
The notification details should list the node that’s not reachable. For Example:
- alertname = KubeNodeUnreachable
...
 - node = node1.example.com
...
Login to the cluster. Check the status of that node:
$ kubectl get node $NODE -o yaml
The output should describe why the node is not reachable.
Common failure scenarios:
disruptive software upgrades
network patitioning due to hardware failures
firewall rules
virtual machines suspended due to storage area network problems
system crashes / freezes due to software or hardware malfunctions
Mitigation
#
In case of maintenance ensure to
cordon and drain node
.
In other cases ensure storage and networking redundancy if applicable.
See
KubeNode
See
node problem detector
See
Watchdog timer
