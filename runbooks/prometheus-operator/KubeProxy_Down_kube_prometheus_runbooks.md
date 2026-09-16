---
id: KubeProxy_Down_kube_prometheus_runbooks
category: kubernetes
fault_type: network
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubeproxydown/
---

# KubeProxy Down | kube-prometheus runbooks

KubeProxy Down | kube-prometheus runbooks
KubeProxy Down
KubeProxyDown
#
Meaning
#
The
KubeProxyDown
alert is triggered when all Kubernetes Proxy instances have not
been reachable by the monitoring system for more than 15 minutes.
Impact
#
kube-proxy is a network proxy that runs on each node in your cluster,
implementing part of the Kubernetes Service concept.
kube-proxy maintains network rules on nodes.
These network rules allow network communication to your Pods
from network sessions inside or outside of your cluster.
kube-proxy uses the operating system packet filtering layer if
there is one and it’s available. Otherwise, kube-proxy forwards the traffic
itself.
Diagnosis
#
Check the status of the
kube-proxy
daemon sets in the
kube-system
namespace.
kubectl get pods -l k8s-app=kube-proxy -n kube-system
Check the specific daemon-set for logs with the following command:
kubectl logs -n kube-system kube-proxy-b9g23
Mitigation
#
AWS EKS
#
If you are running AWS EKS cluster and you find that the
kube-proxy
pods are all running normally, make sure to update the
kube-proxy-config
cm as shown below.
kubectl edit cm -n kube-system kube-proxy-config
...
metricsBindAddress: 0.0.0.0:10249
...
This setting configures the IP address with port for the metrics server to serve on (set to ‘0.0.0.0:10249’ for all IPv4 interfaces and ‘[::]:10249’ for all IPv6 interfaces). More information on the
documentation page
Then just go delete
kube-proxy
pods and new ones will be created automatically.
kubectl delete pod -l k8s-app=kube-proxy -n kube-system
