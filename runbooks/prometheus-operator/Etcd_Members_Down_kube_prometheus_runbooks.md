---
id: Etcd_Members_Down_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/etcd/etcdmembersdown/
---

# Etcd Members Down | kube-prometheus runbooks

Etcd Members Down | kube-prometheus runbooks
Etcd Members Down
etcdMembersDown
#
Meaning
#
This alert fires when one or more etcd member goes down and evaluates the
number of etcd members that are currently down. Often, this alert was observed
as part of a cluster upgrade when a master node is being upgraded and requires a
reboot.
Impact
#
In etcd a majority of (n/2)+1 has to agree on membership changes or key-value
upgrade proposals. With this approach, a split-brain inconsistency can be
avoided. In the case that only one member is down in a 3-member cluster, it
still can make forward progress. Due to the fact that the quorum is 2 and 2
members are still alive. However, when more members are down, the cluster
becomes unrecoverable.
Diagnosis
#
Login to the cluster. Check health of master nodes if any of them is in
NotReady
state or not.
$ kubectl get nodes -l node-role.kubernetes.io/master
=
In case there is no upgrade going on, but there is a change in the
machineconfig
for the master pool causing a rolling reboot of each master
node, this alert can be triggered as well. We can check if the
machineconfiguration.openshift.io/state : Working
annotation is set for any of
the master nodes. This is the case when the
machine-config-operator
(MCO)
is working on it.
$ kubectl get nodes -l node-role.kubernetes.io/master
=
-o template --template
=
'{{range .items}}{{"===> node:> "}}{{.metadata.name}}{{"\n"}}{{range $k, $v := .metadata.annotations}}{{println $k ":" $v}}{{end}}{{"\n"}}{{end}}'
General etcd health
#
To run
etcdctl
commands, we need to
exec
into the
etcdctl
container of any
etcd pod.
$ kubectl exec -c etcdctl -n openshift-etcd
$(
kubectl get po -l app
=
etcd -oname -n openshift-etcd | awk -F
"/"
'NR==1{ print $2 }'
)
Validate that the
etcdctl
command is available:
$ etcdctl version
Run the following command to get the health of etcd:
$ etcdctl endpoint health -w table
Mitigation
#
If an upgrade is in progress, the alert may automatically resolve in some time
when the master node comes up again. If MCO is not working on the master node,
check the cloud provider to verify if the master node instances are running or not.
In the case when you are running on AWS, the AWS instance retirement might need
a manual reboot of the master node.
