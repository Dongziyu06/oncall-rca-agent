---
id: Node_RAID_Degraded_kube_prometheus_runbooks
category: kubernetes
fault_type: disk
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/node/noderaiddegraded/
---

# Node RAID Degraded | kube-prometheus runbooks

Node RAID Degraded | kube-prometheus runbooks
Node RAID Degraded
NodeRAIDDegraded
#
Meaning
#
RAID Array is degraded.
This alert is triggered when a node has a storage configuration with RAID array,
and the array is reporting as being in a degraded state due to one or more disk
failures.
Impact
#
The affected node could go offline at any moment if the RAID array fully fails
due to further issues with disks.
Diagnosis
#
You can open a shell on the node and use the standard Linux utilities to
diagnose the issue, but you may need to install additional software in the debug
container:
$ NODE_NAME
=
'<value of instance label from alert>'
$ oc debug
"node/
$NODE_NAME
"
$ cat /proc/mdstat
Mitigation
#
Cordon and drain node if possible, proceed to RAID recovery.
See the Red Hat Enterprise Linux [documentation][1] for potential steps.
1
