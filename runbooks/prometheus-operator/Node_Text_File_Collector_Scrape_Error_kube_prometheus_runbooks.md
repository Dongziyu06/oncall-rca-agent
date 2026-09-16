---
id: Node_Text_File_Collector_Scrape_Error_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/node/nodetextfilecollectorscrapeerror/
---

# Node Text File Collector Scrape Error | kube-prometheus runbooks

Node Text File Collector Scrape Error | kube-prometheus runbooks
Node Text File Collector Scrape Error
NodeTextFileCollectorScrapeError
#
Meaning
#
Node Exporter text file collector failed to scrape.
Impact
#
Missing metrics from additional scripts.
Diagnosis
#
Check node_exporter logs
Check script supervisor (like systemd or cron) for more information about failed script execution
Mitigation
#
Check if provided configuration is valid, if files were not renamed during upgrades.
