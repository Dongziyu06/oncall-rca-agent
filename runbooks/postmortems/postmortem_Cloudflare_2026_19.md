---
id: postmortem_Cloudflare_2026_19
category: postmortem
fault_type: unknown
source: danluu-postmortems
company: Cloudflare
year: 2026
source_url: https://blog.cloudflare.com/route-leak-incident-january-22-2026/
---
# Cloudflare 2026 Incident Postmortem

## Incident details
Route leak incident on January 22, 2026 | Cloudflare Blog
Skip to content
BGP
Post Mortem
January 23, 2026
Route leak incident on January 22, 2026
Bryton Herdes
and
Tom Strickx
7 minute read
COPY URL
On January 22, 2026, an automated routing policy configuration error caused us to leak some
Border Gateway Protocol (BGP)
prefixes unintentionally from a router at our data center in Miami, Florida. While the route leak caused some impact to Cloudflare customers, multiple external parties were also affected because their traffic was accidentally funnelled through our Miami data center location.
The route leak lasted 25 minutes, causing congestion on some of our backbone infrastructure in Miami, elevated loss for some Cloudflare customer traffic, and higher latency for traffic across these links. Additionally, some traffic was discarded by firewall filters on our routers that are designed to only accept traffic for Cloudflare services and our customers.
While we’ve written about route leaks before, we rarely find ourselves causing them. This route leak was the result of an accidental misconfiguration on a router in Cloudflare’s network, and only affected IPv6 traffic. We sincerely apologize to the users, customers, and networks we impacted yesterday as a result of this BGP route leak.
BGP route leaks
We have
written multiple times
about
BGP route leaks
, and we even record
route leak events
on Cloudflare Radar for anyone to view and learn from. To get a fuller understanding of what route leaks are, you can refer to this
detailed background section
, or refer to the formal definition within
RFC7908
.
Essentially, a route leak occurs when a network tells the broader Internet to send it traffic that it's not supposed to forward. Technically, a route leak occurs when a network, or Autonomous System (AS), appears unexpectedly in an AS path. An AS path is what BGP uses to determine the path across the Internet to a final destination. An example of an anomalous AS path indicative of a route leak would be finding a network sending routes received from a peer to a provider.
During this type of route leak, the rules of
valley-free routing
are violated, as BGP updates are sent from AS64501 to their peer (AS64502), and then unexpectedly up to a provider (AS64503). Oftentimes the leaker, in this case AS64502, is not prepared to handle the amount of traffic they are going to receive and may not even have firewall filters configured to accept all of the traffic coming in their direction. In simple terms, once a route update is sent to a peer or provider, it should only be sent further to customers and not to another peer or provider AS.
During the incident on January 22, we caused a similar kind of route leak, in which we took routes from some of our peers and redistributed them in Miami to some of our peers and providers. According to the route leak definitions in RFC7908, we caused a mixture of Type 3 and Type 4 route leaks on the Internet.
Timeline
Time (UTC)
Event
2026-01-22 19:52 UTC
A change that ultimately triggers the routing policy bug is merged in our network automation code repository
2026-01-22 20:25 UTC
Automation is run on single Miami edge-router resulting in unexpected advertisements to BGP transit providers and peersIMPACT START
2026-01-22 20:40 UTC
Network team begins investigating unintended route advertisements from Miami
2026-01-22 20:44 UTC
Incident is raised to coordinate response
2026-01-22 20:50 UTC
The bad configuration change is manually reverted by a network operator, and automation is paused for the router, so it cannot run againIMPACT STOP
2026-01-22 21:47 UTC
The change that triggered the leak is reverted from our code repository
2026-01-22 22:07 UTC
Automation is confirmed by operators to be healthy to run again on the Miami router, without the routing policy bug
2026-01-22 22:40 UTC
Automation is unpaused on the single router in Miami
What happened: the configuration error
On January 22, 2026, at 20:25 UTC, we pushed a change via our policy automation platform to remove the BGP announcements from Miami for one of our data centers in Bogotá, Colombia. This was purposeful, as we previously forwarded some IPv6 traffic through Miami toward the Bogotá data center, but recent infrastructure upgrades removed the need for us to do so.
This change generated the following diff (a program that
compares
configuration files in order to determine how or whether they differ):
[edit policy
-
options policy
-
statement
6
-
COGENT
-
ACCEPT
-
EXPORT
term
ADV
-
SITELOCAL
-
GRE
-
RECEIVER
from]
-
prefix
-
list
6
-
BOG04
-
SITE
-
LOCAL
;
[edit policy
-
options policy
-
statement
6
-
COMCAST
-
ACCEPT
-
EXPORT
term
ADV
-
SITELOCAL
-
GRE
-
RECEIVER
from]
-
prefix
-
list
6
-
BOG04
-
SITE
-
LOCAL
;
[edit policy
-
options policy
-
statement
6
-
GTT
-
ACCEPT
-
EXPORT
term
ADV
-
SITELOCAL
-
GRE
-
RECEIVER
from]
-
prefix
-
list
6
-
BOG04
-
SITE
-
LOCAL
;
[edit policy
-
options policy
-
statement
6
-
LEVEL3
-
ACCEPT
-
EXPORT
term
ADV
-
SITELOCAL
-
GRE
-
RECEIVER
from]
-
prefix
-

## Source
https://blog.cloudflare.com/route-leak-incident-january-22-2026/
