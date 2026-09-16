import os, structlog
from .common import result, log

def _client():
    try:
        from kubernetes import client, config
        config.load_kube_config(config_file=os.getenv('KUBECONFIG') or None)
        return client.CoreV1Api()
    except Exception:
        return None

async def get_pod_status(service='demo'):
    log.info('get_pod_status', service=service)
    api = None if os.getenv('USE_MOCK','false').lower()=='true' else _client()
    if not api: return result({'source':'mock-kubernetes','service':service,'phase':'Running','restarts':0})
    try:
        pods = api.list_pod_for_all_namespaces(label_selector=f'app={service}')
        items=[{'name':p.metadata.name,'phase':p.status.phase,'restarts':sum((c.restart_count or 0) for c in (p.status.container_statuses or []))} for p in pods.items]
        return result({'source':'kubernetes','service':service,'pods':items})
    except Exception as exc:
        return result({'source':'mock-kubernetes','service':service,'phase':'Running','restarts':0}, error=str(exc))

async def get_pod_logs(service='demo', tail_lines=50):
    api=None if os.getenv('USE_MOCK','false').lower()=='true' else _client()
    if not api: return result({'source':'mock-kubernetes','service':service,'logs':'request completed'})
    try:
        pod=api.list_pod_for_all_namespaces(label_selector=f'app={service}').items[0]
        logs=api.read_namespaced_pod_log(pod.metadata.name,pod.metadata.namespace,tail_lines=tail_lines)
        return result({'source':'kubernetes','service':service,'logs':logs})
    except Exception as exc: return result(None,error=str(exc))

async def get_events(service='demo'):
    api=None if os.getenv('USE_MOCK','false').lower()=='true' else _client()
    if not api: return result({'source':'mock-kubernetes','service':service,'events':[]})
    try:
        events=api.list_event_for_all_namespaces().items
        return result({'source':'kubernetes','service':service,'events':[e.message for e in events if service in (e.message or '')]})
    except Exception as exc: return result(None,error=str(exc))

