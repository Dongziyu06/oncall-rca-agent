---
id: postmortem_Facebook_unknown_24
category: postmortem
fault_type: unknown
source: danluu-postmortems
company: Facebook
year: unknown
source_url: https://blog.thousandeyes.com/facebook-outage-deep-dive/
---
# Facebook unknown Incident Postmortem

## Incident details
Facebook Outage Deep Dive | ThousandEyes
NEW BLOG
Cisco ThousandEyes Comes to Cisco Cloud Control
READ BLOG →
SEARCH
en us
Login
Product
Solutions
Learn
About
Login
EN US
Language
AMERICAS
Brazil
(Português)
Canada
(Français)
Mexico
(Español)
United States
(English)
EUROPE
France
(Français)
Germany
(Deutsch)
Italy
(Italiano)
Spain
(Español)
ASIA
Japan
(日本語)
Korea
(한국어)
Mainland China
(简体中文)
Product
Platform
Platform Overview
Endpoint Experience
Network and Application Synthetics
Internet Insights
™
WAN Insights
Cloud Insights
Traffic Insights
Connected Devices
Assurance
Innovations
Integrations
Developers
Global Vantage Points
Solution Comparison
Pricing
Getting Started
Tutorials
Services
Solutions
Solutions
Overview
Assurance for AgenticOps
Enterprise Digital Experience
Customer Digital Experience
Workforce Digital Experience
Industries
Carriers & Hosting
Consumer Web
Education
Financial Services
Government
Healthcare
Sports, Media & Entertainment
Retail
Learn
Blog
Outage Analyses
Internet Outages Map
The Internet Report Podcast
Research
Resource Center
Customers
Industry Events
Webinars
Tutorials
Cisco U. Courses
Getting Started
Support Community
ThousandEyes Certification
About
About Us
Customers
Newsroom
Careers
Partners
Contact Us
Demo
Start Free Trial
Outage Analyses
Facebook Outage Deep Dive
By
Nick Kephart
|
| 7 min read
Summary
In the late evening of January 26th, Facebook had its largest outage in more than four years. For approximately an hour both Facebook and Instagram (owned by Facebook) were completely down, along with numerous other affected sites such as Tinder and HipChat.
Facebook’s
own post mortem
and
statements
suggested the outage occurred “after we introduced a change that affected our configuration systems."
Now, three days later
a lot has been written
about the outage, much of it only partially accurate. Let’s take the Facebook post mortem as a starting point and see how the outage unfolded. Follow along the blog post with the interactive data set using this
share link
of the event. You’ll want to take a look at the HTTP Server and Path Visualization views.
Facebook Data Center and Network Architecture
Facebook maintains data centers in Prineville OR, Forest City NC and Luleå, Sweden (with Altoona IA ramping up).
DNS-based global load balancing
, based on “internet topology, user latency, user bandwidth, compute cluster load/availability/performance,” distributes traffic from visitors around the world to these data centers. Traffic is served by Facebook’s fiber network which spans East Asia, Australia, U.S. and Western Europe as well as transit providers for traffic from other locations, such as Africa, South America and India.
Under normal conditions, traffic to Facebook looks like Figure 1. Two primary data center clusters are visible, with Prineville OR in the top topology and Forest City NC in the bottom topology.
Figure 1: HTTPS traffic paths to Facebook before the outage, with Prineville OR data center above and Forest City NC below.
Figure 2: ‘4-post’ architecture in Forest City NC.
In addition, you can see Facebook’s network in light green, flowing through their backbone to aggregation switches, cluster switches and through the rack (the white interfaces) to the servers on the right. You can read more about the ‘4-post’ architecture used at the Forest City data center in this paper on
Facebook’s Data Center Network Architecture
. Facebook’s next generation architecture, called
Fabric
, will be rolled out in Altoona IA, though we don’t currently see any customer-facing production traffic flowing there yet.
Facebook also has several other services with distinct architectures. Instagram is served primarily from Amazon Web Services US-East region. WhatsApp utilizes a SoftLayer data center in Northern Virginia. We’ll touch on these services below.
The January 26th Facebook Outage
At 10:10pm Pacific on January 26th, TCP connections to Facebook timed out, as their engineering team likely shut off traffic. In Figures 3 and 4 you can see the drop in availability caused by TCP connection problems and the near complete packet loss. Only our Denver agent was still able to reach a web server.
Figure 3: Timeline of the Facebook outage with a one hour drop in availability due primarily to TCP connection errors.
Figure 4: Packet loss to Facebook is greater than 80% as TCP connections are terminated in the Facebook data centers.
During the outage, packets were dropped within Facebook’s network, likely by an update to their Access Control List (ACL). Figure 5 shows the path trace with traffic timing out at the aggregation switches inside Prineville, before ever reaching the racks. At approximately 11:05pm, Facebook began allowing TCP connections again, with full service restored around 11:20pm.
Figure 5: Traffic terminates in the Prineville data center (red nodes), with Facebook’s network highlighted in yellow.
How Instagram Fared
Instagram, another Facebook-owned service affected by the outage, had a somewhat different experience. Although the service was unavailable, throwing 503 ‘service unavailable’ errors, TCP connections were completed to the web servers. This is likely due to the fact that Instagram is hosted on Amazon Web Services and did not require the same sort of network isolation to tackle the configuration issues. Figures 6 and 7 show the availability drop for Instagram, even while the network paths look healthy.
Figure 6: Instagram did not terminate TCP connections, instead it replied with 503 errors.
Figure 7: Path visualization to Instagram (hosted on AWS) during the outage, showing no network issues at all.
Monitoring Outages
Hopefully you were able to follow along with the interactive data in the
share link
. Interested in other outages? Check out previous analysis of the
Craigslist DNS hijack
,
Time Warner Cable outage
and a
GitHub DDoS
.
If you’d like to see a live data set of Facebook, or track the availability of other major cloud services such as Twitter and Salesforce,
sign up for a free ThousandEyes trial
.
Published On
Nick Kephart
Sr. Director, Product Management
Categories:
Outage Analyses
Share This!
Back to ThousandEyes Blog
Stay Connected
Subscribe to the Internet and Cloud Intelligence Blog!
Subscribe
Stay Connected
Subscribe to the Internet and Cloud Intelligence Blog!
Subscribe
related blogs
Claude Outage Analysis: June 23, 2026
On June 23, ThousandEyes observed a degradation of service affecting Anthropic's Claude. See how the outage unfolded in this analysis—more updates will be added as we have them.
By Internet Research Team
23 Jun 2026
Application Experience
Artificial Intelligence (AI)
Internet Outages
Meta Outage Analysis: June 12, 2026
On June 12, ThousandEyes detected response errors and timeouts across multiple Meta services. See how the outage unfolded in this analysis—more updates will be added as we have them.
By Internet Research Team
12 Jun 2026
Internet Outages

## Source
https://blog.thousandeyes.com/facebook-outage-deep-dive/
