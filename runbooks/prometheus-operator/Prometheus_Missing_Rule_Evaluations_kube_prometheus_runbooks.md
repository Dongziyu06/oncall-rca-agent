---
id: Prometheus_Missing_Rule_Evaluations_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheusmissingruleevaluations/
---

# Prometheus Missing Rule Evaluations | kube-prometheus runbooks

Prometheus Missing Rule Evaluations | kube-prometheus runbooks
Prometheus Missing Rule Evaluations
PrometheusMissingRuleEvaluations
#
Meaning
#
Prometheus is missing rule evaluations due to slow rule group evaluation.
Impact
#
Metrics and alerts may be missing or inaccurate.
Diagnosis
#
Check which rules fail, try to calcuate them differently.
Mitigation
#
Sometimes giving more CPU is the only way to fix it.
