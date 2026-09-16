---
id: service_timeout
category: custom
fault_type: timeout
severity: warning
source: custom-oncall-rca
---
# 服务超时与高延迟 / Service Timeout

从网关、应用到依赖逐段测量 latency、error rate 和 saturation。PromQL `histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))` 查 P99。检查连接池、DNS、retry 与 timeout 配置，避免重试风暴。

Measure every hop and distinguish client, proxy and server timeouts. Correlate traces with dependency health. Do not only increase timeouts because queueing can amplify a cascade.
