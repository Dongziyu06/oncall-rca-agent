---
id: Config_Reloader_Sidecar_Errors_kube_prometheus_runbooks
category: kubernetes
fault_type: unknown
severity: warning
source: prometheus-operator-runbooks
source_url: https://runbooks.prometheus-operator.dev/runbooks/prometheus-operator/configreloadersidecarerrors/
---

# Config Reloader Sidecar Errors | kube-prometheus runbooks

Config Reloader Sidecar Errors | kube-prometheus runbooks
Config Reloader Sidecar Errors
ConfigReloaderSidecarErrors
#
Meaning
#
Errors encountered while the config-reloader sidecar attempts to sync
configuration in a given namespace.
Impact
#
As a result, configuration for services such as prometheus or alertmanager maybe
stale and cannot be automatically updated.'
Diagnosis
#
Check config-reloader logs and the configuration which it tries to reload.
Mitigation
#
Usually means new config was rejected by the controlled app because it contains
errors such as unknown configuration sections or bad resource definitions.
You can prevent such issues with better config testing tools in CI/CD systems
such as:
yamllint
yamale
promtool
jq
yq (notice there is python and golang versions)
conftest
some apps have syntax checking command switch
