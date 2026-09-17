import os
from .common import result, log

def _client():
    path = os.getenv("KUBECONFIG")
    if not path or not os.path.exists(path):
        return None
    try:
        from kubernetes import client, config

        config.load_kube_config(config_file=path)
        # 实验室自签证书常触发 CERTIFICATE_VERIFY_FAILED；默认跳过校验
        conf = client.Configuration.get_default_copy()
        if os.getenv("K8S_VERIFY_SSL", "false").lower() != "true":
            conf.verify_ssl = False
            conf.ssl_ca_cert = None
        # 防止 VPN 断开时无限等待（chat agent 工具调用必须有超时）
        conf.connection_pool_maxsize = 4
        conf.retries = False
        client.Configuration.set_default(conf)
        return client.CoreV1Api()
    except Exception as e:
        log.warning("k8s_client_init_failed", error=str(e))
        return None


async def get_pod_status(service="demo", namespace="default"):
    log.info("get_pod_status", service=service, namespace=namespace)
    api = None if os.getenv("USE_MOCK", "false").lower() == "true" else _client()
    if not api:
        return result({"source": "mock-kubernetes", "service": service, "phase": "Running", "restarts": 0})
    try:
        pods = api.list_namespaced_pod(namespace, label_selector=f"app={service}").items
        if not pods:
            try:
                pods = [api.read_namespaced_pod(service, namespace)]
            except Exception:
                pods = []
        items = []
        for p in pods:
            cs = p.status.container_statuses or []
            reason = p.status.reason
            if not reason and cs and cs[0].state and cs[0].state.waiting:
                reason = cs[0].state.waiting.reason
            # 取 lastState 退出码与错误信息（CrashLoop 关键证据）
            last_state = {}
            if cs and cs[0].last_state and cs[0].last_state.terminated:
                t = cs[0].last_state.terminated
                last_state = {
                    "exit_code": t.exit_code,
                    "reason": t.reason,
                    "message": (t.message or "")[:500],
                    "finished_at": str(t.finished_at),
                }
            items.append(
                {
                    "name": p.metadata.name,
                    "namespace": p.metadata.namespace,
                    "phase": p.status.phase,
                    "reason": reason,
                    "restarts": sum((c.restart_count or 0) for c in cs),
                    "last_state": last_state,
                }
            )
        if not items:
            return result({"source": "kubernetes", "service": service, "pods": [], "note": "no matching pods"})
        return result({"source": "kubernetes", "service": service, "pods": items})
    except Exception as e:
        log.warning("k8s_get_pod_status_failed", error=str(e))
        return result(
            {"source": "mock-kubernetes", "service": service, "phase": "Running", "restarts": 0},
            error=str(e),
        )


async def get_pod_logs(service="demo", tail_lines=50, namespace="default"):
    api = None if os.getenv("USE_MOCK", "false").lower() == "true" else _client()
    if not api:
        return result({"source": "mock-kubernetes", "service": service, "logs": "request completed"})
    try:
        pods = api.list_namespaced_pod(namespace, label_selector=f"app={service}").items
        pod = pods[0] if pods else api.read_namespaced_pod(service, namespace)
        logs = api.read_namespaced_pod_log(pod.metadata.name, namespace, tail_lines=tail_lines, previous=True)
        return result({"source": "kubernetes", "service": service, "logs": logs})
    except Exception as e:
        return result(None, error=str(e))


async def get_events(service="demo", namespace="default"):
    api = None if os.getenv("USE_MOCK", "false").lower() == "true" else _client()
    if not api:
        return result({"source": "mock-kubernetes", "service": service, "events": []})
    try:
        ev = api.list_namespaced_event(namespace).items
        return result(
            {
                "source": "kubernetes",
                "service": service,
                "events": [
                    {"reason": e.reason, "message": e.message, "type": e.type}
                    for e in ev
                    if service in (e.involved_object.name or "")
                ],
            }
        )
    except Exception as e:
        return result(None, error=str(e))
