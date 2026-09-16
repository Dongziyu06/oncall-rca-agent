---
id: Kube_API_Error_Budget_Burn_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubeapierrorbudgetburn/
---

# Kube API Error Budget Burn | kube-prometheus runbooks

Kube API Error Budget Burn | kube-prometheus runbooks
Kube API Error Budget Burn
KubeAPIErrorBudgetBurn
#
Impact
#
The overall availability of your Kubernetes cluster isn’t guaranteed any more.
There may be
too many errors
returned by the APIServer and/or
responses take too long
for guarantee proper reconciliation.
This is always important; the only deciding factor is how urgent it is at the current rate
Full context
This alert essentially means that a higher-than-expected percentage of the operations kube-apiserver is performing are erroring. Since random errors are inevitable, kube-apiserver has a “budget” of errors that it is allowed to make before triggering this alert.
Learn more about Multiple Burn Rate Alerts in the
SRE Workbook Chapter 5
.
Critical
#
First check the labels
long
and
short
.
long: 1h
and
short: 5m
: less than
~2 days
– You should fix the problem as soon as possible!
long: 6h
and
short: 30m
: less than
~5 days
– Track this down now but no immediate fix required.
Warning
#
First check the labels
long
and
short
.
long: 1d
and
short: 2h
: less than
~10 days
– This is problematic in the long run. You should take a look in the next 24-48 hours.
long: 3d
and
short: 6h
: less than
~30 days
– (the entire window of the error budget) at this rate. This means that at the end of the next 30 days there won’t be any error budget left at this rate. It’s fine to leave this over the weekend and have someone take a look in the coming days at working hours.
Example: If you have a 99% availability target this means that at the end of 30 days you’re going to be below 99% at this rate.
Runbook
#
Take a look at the APIServer Grafana dashboard.
At the very top check your current availability and how much percent of error budget is left. This should indicate the severity too.
Do you see an elevated error rate in reads or writes?
Do you see too many slow requests in reads or writes?
Check the logs for kube-apiserver using the following Loki query:
{component="kube-apiserver"}
Run debugging queries in Prometheus or Grafana Explore to dig deeper.
If you don’t see anything obvious with the error rates, it might be too many slow requests.
Check the queries below!
Maybe it’s some dependency of the APIServer? etcd?
Example Queries for slow requests
#
Change the rate window according to your
long
label from the alert.
Make sure to update the alert threshold too, like
> 0.01
to
> 14.4 * 0.01
for example.
Slow Read Requests
#
If you don’t get any results back then there aren’t too many slow requests - that’s good.
If you get results than you know what type of requests are too slow.
Cluster scoped:
(
sum
(
rate
(
apiserver_request_duration_seconds_bucket{job
=
"
apiserver
",le
=
"
40
",scope
=
"
cluster
",verb
=~
"
LIST|GET
"}[
3d
]
))
-
sum
(
rate
(
apiserver_request_duration_seconds_count{job
=
"
apiserver
",verb
=~
"
LIST|GET
"}[
3d
]
))
)
/
sum
(
rate
(
apiserver_request_total{job
=
"
apiserver
",verb
=~
"
LIST|GET
"}[
3d
]
))
>
0.01
Namespace scoped:
(
sum
(
rate
(
apiserver_request_duration_seconds_bucket{job
=
"
apiserver
",le
=
"
5
",scope
=
"
namespace
",verb
=~
"
LIST|GET
"}[
3d
]
))
-
sum
(
rate
(
apiserver_request_duration_seconds_count{job
=
"
apiserver
",verb
=~
"
LIST|GET
"}[
3d
]
))
)
/
sum
(
rate
(
apiserver_request_total{job
=
"
apiserver
",verb
=~
"
LIST|GET
"}[
3d
]
))
>
0.01
Resource scoped:
(
sum
(
rate
(
apiserver_request_duration_seconds_bucket{job
=
"
apiserver
",le
=
"
1
",scope
=~
"
resource|
",verb
=~
"
LIST|GET
"}[
3d
]
))
or
vector
(
0
)
-
sum
(
rate
(
apiserver_request_duration_seconds_count{job
=
"
apiserver
",verb
=~
"
LIST|GET
"}[
3d
]
))
)
/
sum
(
rate
(
apiserver_request_total{job
=
"
apiserver
",verb
=~
"
LIST|GET
"}[
3d
]
))
>
0.01
Slow Write Requests
#
(
sum
(
rate
(
apiserver_request_duration_seconds_count{job
=
"
apiserver
",verb
=~
"
POST|PUT|PATCH|DELETE
"}[
3d
]
))
-
sum
(
rate
(
apiserver_request_duration_seconds_bucket{job
=
"
apiserver
",le
=
"
1
",verb
=~
"
POST|PUT|PATCH|DELETE
"}[
3d
]
))
)
/
sum
(
rate
(
apiserver_request_total{job
=
"
apiserver
",verb
=~
"
POST|PUT|PATCH|DELETE
"}[
3d
]
))
>
0.01
