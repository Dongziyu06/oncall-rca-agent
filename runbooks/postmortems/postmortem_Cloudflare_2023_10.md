---
id: postmortem_Cloudflare_2023_10
category: postmortem
fault_type: timeout
source: danluu-postmortems
company: Cloudflare
year: 2023
source_url: https://blog.cloudflare.com/1-1-1-1-lookup-failures-on-october-4th-2023/
---
# Cloudflare 2023 Incident Postmortem

## Incident details
1.1.1.1 lookup failures on  October 4, 2023 | Cloudflare Blog
Skip to content
1.1.1.1
Outage
Post Mortem
October 4, 2023
1.1.1.1 lookup failures on  October 4, 2023
Ólafur Guðmundsson
10 minute read
COPY URL
This post is also available in
Deutsch
,
Español
,
Français
,
日本語
,
한국어
,
繁體中文
,
and
简体中文
.
On 4 October 2023, Cloudflare experienced DNS resolution problems starting at 07:00 UTC and ending at 11:00 UTC. Some users of 1.1.1.1 or products like WARP, Zero Trust, or third party DNS resolvers which use 1.1.1.1 may have received SERVFAIL DNS responses to valid queries. We’re very sorry for this outage. This outage was an internal software error and not the result of an attack. In this blog, we’re going to talk about what the failure was, why it occurred, and what we’re doing to make sure this doesn’t happen again.
Background
In the
Domain Name System (DNS)
, every domain name exists within a DNS zone. The zone is a collection of
domain names
and host names that are controlled together. For example, Cloudflare is responsible for the domain name cloudflare.com, which we say is in the “cloudflare.com” zone. The .com top-level domain (TLD) is owned by a third party and is in the “com” zone. It gives directions on how to reach cloudflare.com. Above all of the TLDs is
the root zone
, which gives
directions on how to reach TLDs
. This means that the root zone is important in being able to resolve all other domain names. Like other important parts of the DNS,
the root zone is signed with DNSSEC
, which means the root zone itself contains cryptographic signatures.
The root zone is published on
the root servers
, but it is also common for DNS operators to
retrieve and retain a copy of the root zone automatically
so that in the event that the root servers cannot be reached, the information in the root zone is still available. Cloudflare’s recursive DNS infrastructure takes this approach as it also makes the resolution process faster. New versions of the root zone are normally published twice a day. 1.1.1.1 has a
WebAssembly app
called static_zone running on top of the main DNS logic that serves those new versions when they are available.
What happened
On 21 September, as part of
a known and planned change in root zone management
, a new resource record type was included in the root zones for the first time. The new resource record is named
ZONEMD
, and is in effect a checksum for the contents of the root zone.
The root zone is retrieved by software running in Cloudflare’s core network. It is subsequently redistributed to Cloudflare’s data centers around the world. After the change, the root zone containing the ZONEMD record continued to be retrieved and distributed as normal. However, the 1.1.1.1 resolver systems that make use of that data had problems parsing the ZONEMD record. Because zones must be loaded and served in their entirety, the system’s failure to parse ZONEMD meant the new versions of the root zone were not used in Cloudflare’s resolver systems. Some of the servers hosting Cloudflare's resolver infrastructure failed over to querying the DNS root servers directly on a request-by-request basis when they did not receive the new root zone. However, others continued to rely on the known working version of the root zone still available in their memory cache, which was the version pulled on 21 September before the change.
On 4 October 2023 at 07:00 UTC, the DNSSEC signatures in the version of the root zone from 21 September expired. Because there was no newer version that the Cloudflare resolver systems were able to use, some of Cloudflare’s resolver systems stopped being able to validate DNSSEC signatures and as a result started sending error responses (SERVFAIL). The rate at which Cloudflare resolvers generated SERVFAIL responses grew by 12%. The diagrams below illustrate the progression of the failure and how it became visible to users.
Incident timeline and impact
21 September 6:30 UTC
: Last successful pull of the root zone.
4 October 7:00 UTC
: DNSSEC signatures in the root zone obtained on 21 September expired causing an increase in SERVFAIL responses to client queries.
7:57
: First external reports of unexpected SERVFAILs started coming in.
8:03
: Internal Cloudflare incident declared.
8:50
: Initial attempt made at stopping 1.1.1.1 from serving responses using the stale root zone file with an override rule.
10:30
: Stopped 1.1.1.1 from preloading the root zone file entirely.
10:32
: Responses returned to normal.
11:02
: Incident closed.
This below chart shows the timeline of impact along with the percentage of DNS queries that returned with a SERVFAIL error:
We expect a baseline volume of SERVFAIL errors for regular traffic during normal operation. Usually that percentage sits at around 3%. These SERVFAILs can be caused by legitimate issues in the DNSSEC chain, failures to connect to authoritative servers, authoritative servers taking too long to respond,
and many others
. During the incident the amount of SERVFAILs peaked at 15% of total queries, although the impact was not evenly distributed around the world and was mainly concentrated in our larger data centers like Ashburn, Virginia; Frankfurt, Germany; and Singapore.
Why this incident happened
Why parsing the ZONEMD record failed
DNS has a binary format for storing resource records. In this binary format the type of the resource record (TYPE)  is stored as a 16-bit integer. The type of resource record determines how the resource data (RDATA) is parsed. When the record type is 1, this means it is an A record, and the RDATA can be parsed as an IPv4 address. Record type 28 is an AAAA record, whose RDATA can be parsed as an IPv6 address instead. When a parser runs into an unknown resource type it won’t know how to parse its RDATA, but fortunately it doesn’t have to: the RDLENGTH field indicates how long the RDATA field is, allowing the parser to treat it as an opaque data element.
1
1
1
1
1
1
0
1
2
3
4
5
6
7
8
9
0
1
2
3
4
5
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|
|
/
/
/
NAME
/
|
|
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|
TYPE
|
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|
CLASS
|
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|
TTL
|
|
|
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|
RDLENGTH
|
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--
|
/
RDATA
/
/
/
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
RFC 1035
The reason static_zone didn’t support the new ZONEMD record is because up until now we had chosen to distribute the root zone internally in its presentation format, rather than in the binary format. When looking at the text representation for a few resource records we can see there is a lot more variation in how different records are presented.
.
86400
IN
SOA
a.root-servers.net.
nstld.verisign-grs.com.
2023100400
1800
900
604800
86400
.
86400
IN
RRSIG
SOA
8
0
86400
20231017050000
20231004040000
46780
.
J5lVTygIkJHDBt6HHm1QLx7S0EItynbBijgNlcKs/W8FIkPBfCQmw5BsUTZAPVxKj7r2iNLRddwRcM/1sL49jV9Jtctn8OLLc9wtouBmg3LH94M0utW86dKSGEKtzGzWbi5hjVBlkroB8XVQxBphAUqGxNDxdE6AIAvh/eSSb3uSQrarxLnKWvHIHm5PORIOftkIRZ2kcA7Qtou9NqPCSE8fOM5EdXxussKChGthmN5AR5S2EruXIGGRd1vvEYBrRPv55BAWKKRERkaXhgAp7VikYzXesiRLdqVlTQd+fwy2tm/MTw+v3Un48wXPg1lRPlQXmQsuBwqg74Ts5r8w8w==
.
518400
IN
NS
a.root-servers.net.
.
86400
IN
ZONEMD
2023100400
1
241
E375B158DAEE6141E1F784FDB66620CC4412EDE47C8892B975C90C6A102E97443678CCA4115E27195B468E33ABD9F78C
Example records taken from
https://www.internic.net/domain/root.zone
When we run into an unknown resource record it’s not always easy to know how to handle it. Because of this, the library we use to parse the root zone at the edge does not make an attempt at doing so, and instead returns a parser error.
Why a stale version of the root zone was used
The static_zone app, tasked with loading and parsing the root zone for the purpose of serving the root zone locally (

## Source
https://blog.cloudflare.com/1-1-1-1-lookup-failures-on-october-4th-2023/
