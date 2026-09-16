---
id: Node_File_Descriptor_Limit_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/node/nodefiledescriptorlimit/
---

# Node File Descriptor Limit | kube-prometheus runbooks

Node File Descriptor Limit | kube-prometheus runbooks
Node File Descriptor Limit
NodeFileDescriptorLimit
#
Meaning
#
This alert is triggered when a node’s kernel is found to be running out of
available file descriptors – a
warning
level alert at greater than 70% usage
and a
critical
level alert at greater than 90% usage.
Impact
#
Applications on the node may no longer be able to open and operate on
files. This is likely to have severe consequences for anything scheduled on this
node.
Diagnosis
#
You can open a shell on the node and use the standard Linux utilities to
diagnose the issue:
$ NODE_NAME
=
'<value of instance label from alert>'
$ oc debug
"node/
$NODE_NAME
"
# sysctl -a | grep 'fs.file-'
fs.file-max
=
1597016
fs.file-nr
=
7104
0
1597016
# lsof -n
Mitigation
#
Reduce the number of files opened simultaneously by either adjusting application
configuration or by moving some applications to other nodes.
