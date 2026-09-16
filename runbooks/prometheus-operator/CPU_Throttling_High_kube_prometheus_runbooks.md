---
id: CPU_Throttling_High_kube_prometheus_runbooks
category: kubernetes
fault_type: cpu
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/kubernetes/cputhrottlinghigh/
---

# CPU Throttling High | kube-prometheus runbooks

CPU Throttling High | kube-prometheus runbooks
CPU Throttling High
CPU Throttling High
#
Meaning
#
Processes experience elevated CPU throttling.
Impact
#
The alert is purely informative and unless there is some other issue with
the application, it can be skipped.
Diagnosis
#
Check if application is performing normally
Check if CPU resource requests are adjusted accordingly to the app usage
Check kernel version in the node
Mitigation
#
Notice
:
User shouldn’t increase CPU limits unless the application is behaving
erratically (another alert firing).
For this particular reason, the alert is inhibited by default in
kube-prometheus and can be sent only if another alert in the same namespace
is firing.
When mixed with other alerts
:
Give specific container in the pod more CPU limits. Requests can stay the same.
In specific cases kubernetes node has too old kernel which is known to have
issues with assigning CPU resources to the process
see here
In certain scenarios ensure to use CPU Pinning and isolation - in short give
to the container full CPU cores.
Also ensure to update app so that it is aware it runs in cgroups,
or explicitly set number of CPU it can use, or limit number of threads.
Longer and more detailed info -
PDF from Intel
