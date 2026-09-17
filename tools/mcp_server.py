"""MCP server exposing the project's read-only observability tools."""
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

from tools.prometheus_tools import query_metric
from tools.k8s_tools import get_pod_status, get_pod_logs, get_events
from tools.loki_tools import query_logs

# streamable_http_path="/"：外层 FastAPI 已 mount 到 /mcp，避免实际路径变成 /mcp/mcp
# 关闭 DNS rebinding 校验：演示环境会从公网 IP / TestClient(testserver) 访问
mcp = FastMCP(
    "oncall-rca-tools",
    streamable_http_path="/",
    transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
)

@mcp.tool()
async def prometheus_query(promql: str) -> dict:
    """查询 Prometheus 指标。输入 PromQL 表达式，返回查询结果。"""
    result = await query_metric(promql)
    return result.get("data", {})

@mcp.tool()
async def kubernetes_pod_status(service: str, namespace: str = "default") -> dict:
    """获取 Kubernetes Pod 状态、重启次数和最近退出信息。"""
    result = await get_pod_status(service, namespace=namespace)
    return result.get("data", {})

@mcp.tool()
async def kubernetes_pod_logs(service: str, tail_lines: int = 50, namespace: str = "default") -> dict:
    """获取容器日志（包括上次崩溃的 previous 日志）。"""
    result = await get_pod_logs(service, tail_lines=tail_lines, namespace=namespace)
    return result.get("data", {})

@mcp.tool()
async def kubernetes_events(service: str, namespace: str = "default") -> dict:
    """获取与服务相关的 Kubernetes Events（OOMKilled、探针失败等）。"""
    result = await get_events(service, namespace=namespace)
    return result.get("data", {})

@mcp.tool()
async def loki_logs(service: str, minutes: int = 30) -> dict:
    """从 Loki 查询应用日志。"""
    result = await query_logs(service, time_range=f"{minutes}m")
    return result.get("data", {})
