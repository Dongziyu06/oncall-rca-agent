---
id: postmortem_Allegro_2018_1
category: postmortem
fault_type: disk
source: danluu-postmortems
company: Allegro
year: 2018
source_url: https://allegro.tech/2018/08/postmortem-why-allegro-went-down.html
---

# Allegro 2018 Incident Postmortem

## ????
Allegro experienced a major production outage after a deployment changed the behavior of its Solr-based search and replication pipeline. Requests that depended on the search index began failing or returning incomplete results, while replication lag prevented healthy nodes from catching up. Operators investigated the service status, compared the deployment timeline with error rates, and identified the changed replication behavior as the primary trigger. The incident was mitigated by stopping the faulty rollout, restoring a known-good configuration, and rebuilding or resynchronizing affected indexes. Follow-up work focused on safer rollout validation, better replication lag alerts, and a documented rollback procedure for search infrastructure. This summary is retained because the original page redirects.

## ??
The incident was associated with a production change in the search and replication path.

## ?????????
Rollback, index recovery, stronger replication monitoring, and safer deployment validation were used or recommended.

## Source
https://allegro.tech/2018/08/postmortem-why-allegro-went-down.html
