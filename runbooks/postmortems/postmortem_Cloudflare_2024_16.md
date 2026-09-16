---
id: postmortem_Cloudflare_2024_16
category: postmortem
fault_type: disk
source: danluu-postmortems
company: Cloudflare
year: 2024
source_url: https://blog.cloudflare.com/cloudflare-incident-on-june-20-2024/
---
# Cloudflare 2024 Incident Postmortem

## Incident details
Cloudflare incident on June 20, 2024 | Cloudflare Blog
Skip to content
Outage
Post Mortem
June 26, 2024
Cloudflare incident on June 20, 2024
Lloyd Wallis
,
Julien Desgats
,
and
Manish Arora
14 minute read
COPY URL
This post is also available in
日本語
,
한국어
,
繁體中文
,
and
简体中文
.
On Thursday, June 20, 2024, two independent events caused an increase in latency and error rates for Internet properties and Cloudflare services that lasted 114 minutes. During the 30-minute peak of the impact, we saw that 1.4 - 2.1% of HTTP requests to our CDN received a generic error page, and observed a 3x increase for the 99th percentile Time To First Byte (TTFB) latency.
These events occurred because:
Automated network monitoring
detected performance degradation, re-routing traffic suboptimally and
causing backbone congestion between 17:33 and 17:50 UTC
A new Distributed Denial-of-Service (DDoS) mitigation mechanism deployed between 14:14 and 17:06 UTC triggered a latent bug in our rate limiting system that allowed a specific form of HTTP request to cause a process handling it to enter an infinite loop
between 17:47 and 19:27 UTC
Impact from these events were observed in many Cloudflare data centers around the world.
With respect to the backbone congestion event, we were already working on expanding backbone capacity in the affected data centers, and improving our network mitigations to use more information about the available capacity on alternative network paths when taking action. In the remainder of this blog post, we will go into more detail on the second and more impactful of these events.
As part of routine updates to our protection mechanisms, we created a new DDoS rule to prevent a specific type of abuse that we observed on our infrastructure. This DDoS rule worked as expected, however in a specific suspect traffic case it exposed a latent bug in our existing rate-limiting component. To be absolutely clear, we have no reason to believe this suspect traffic was intentionally exploiting this bug, and there is no evidence of a breach of any kind.
We are sorry for the impact and have already made changes to help prevent these problems from occurring again.
Background
Rate-limiting suspicious traffic
Depending on the profile of an HTTP request and the configuration of the requested Internet property, Cloudflare may protect our network and our customer’s origins by applying a limit to the number of requests a visitor can make within a certain time window. These
rate limits
can activate through customer configuration or in response to DDoS rules detecting suspicious activity.
Usually, these rate limits will be applied based on the IP address of the visitor. As many institutions and Internet Service Providers (ISPs) can have
many devices and individual users behind a single IP address
, rate limiting based on the IP address is a broad brush that can unintentionally block legitimate traffic.
Balancing traffic across our network
Cloudflare has several systems that together provide continuous real-time capacity monitoring and rebalancing to ensure we serve as much traffic as we can as quickly and efficiently as we can.
The first of these is
Unimog, Cloudflare’s edge load balancer
. Every packet that reaches our anycast network passes through Unimog, which delivers it to an appropriate server to process that packet. That server may be in a different location from where the packet originally arrived into our network, depending on the availability of compute capacity. Within each data center, Unimog aims to keep the CPU load uniform across all active servers.
For a global view of our network, we rely on
Traffic Manager
. Across all of our data center locations, it takes in a variety of signals, such as overall CPU utilization, HTTP request latency, and bandwidth utilization to instruct rebalancing decisions. It has built-in safety limits to prevent causing outsized traffic shifts, and also considers the expected resulting load in destination locations when making any decisions.
Incident timeline and impact
All timestamps are UTC on 2024-06-20.
14:14 DDoS rule gradual deployment starts
17:06 DDoS rule deployed globally
17:47 First HTTP request handling process is poisoned
18:04 Incident declared automatically based on detected high CPU load
18:34 Service restart shown to recover on a server, full restart tested in one data center
18:44 CPU load normalized in data center after service restart
18:51 Continual global reloads of all servers with many stuck processes begin
19:05 Global eyeball HTTP error rate peaks at 2.1% service unavailable / 3.45% total
19:05 First Traffic Manager actions recovering service
19:11 Global eyeball HTTP error rate halved to 1% service unavailable / 1.96% total
19:27 Global eyeball HTTP error rate reduced to baseline levels
19:29 DDoS rule deployment identified as likely cause of process poisoning
19:34 DDoS rule is fully disabled
19:43 Engineers stop routine restarts of services on servers with many stuck processes
20:16 Incident response stood down
Below, we provide a view of the impact from some of Cloudflare’s internal metrics. The first graph illustrates the percentage of all eyeball (inbound from external devices) HTTP requests that were served an error response because the service suffering poisoning could not be reached. We saw an initial increase to 0.5% of requests, and then later a larger one reaching as much as 2.1% before recovery started due to our service reloads.
For a broader view of errors, we can see all 5xx responses our network returned to eyeballs during the same window, including those from origin servers. These peaked at 3.45%, and you can more clearly see the gradual recovery between 19:25 and 20:00 UTC as Traffic Manager finished its re-routing activities. The dip at 19:25 UTC aligns with the last large reload, with the error increase afterwards primarily consisting of upstream DNS timeouts and connection limits which are consistent with high and unbalanced load.
And here’s what our TTFB measurements looked like at the 50th, 90th and 99th percentiles, showing an almost 3x increase in latency at p99:
Technical description of the error and how it happened
Global percentage of HTTP Request handling processes that were using excessive CPU during the event
Earlier on June 20, between 14:14 - 17:06 UTC, we gradually activated a new DDoS rule on our network. Cloudflare has recently been building a new way of mitigating HTTP DDoS attacks. This method is using a combination of rate-limits and cookies in order to allow legitimate clients that were falsely identified as being part of an attack to proceed anyway.
With this new method, an HTTP request that is considered suspicious runs through these key steps:
Check for the presence of a valid cookie, otherwise block the request
If a valid cookie is found, add a rate-limit rule based on the cookie value to be evaluated at a later point
Once all the currently applied DDoS mitigation are run, apply rate-limit rules
We use this "asynchronous" workflow because it is more efficient to block a request without a rate-limit rule, so it gives a chance for other rule types to be applied.
So overall, the flow can be summarized with this pseudocode:
for
(
rule
in
active_mitigations
) {
//
...
(ignore
other
rule
types
)
if
(
rule.match_current_request
()) {
if
(
!
has_valid_cookie
()) {
//
no
cookie:
serve
error
page
return
serve_error_page
();
}
else
{
//
add
a
rate-limit
rule
to
be
evaluated
later
add_rate_limit_rule(rule
);
}
}
}
evaluate_rate_limit_rules
();
When evaluating rate-limit rules, we need to make a
key
for each client that is used to look up the correct counter and compare it with the target rate. Typically, this key is the client IP address, but other options are available, such as the value of a cookie as used here. We actually reused an existing portion of the rate-limit logic to achieve this. In pseudocode, it looks like:
function
get_cookie_key
() {
//
Validate
that
the
cookie
is
valid
before
taking
its
value.
//
Here
the
cookie
has
been
checked
before
already,
but
this
code
is
//
also
used
for
"standalone"
rate-limit
rules.
if
(
!
has_valid_cookie_broken
()) {
//
more
on
the
"broken"
part
later
return

## Source
https://blog.cloudflare.com/cloudflare-incident-on-june-20-2024/
