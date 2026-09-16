import os, structlog, httpx
from .common import result, log, bounded

async def query_metric(promql: str, time_range: str = '5m'):
    url = os.getenv('PROMETHEUS_URL')
    log.info('query_metric', promql=promql, time_range=time_range, backend='prometheus' if url else 'mock')
    if os.getenv('USE_MOCK','false').lower()=='true' or not url:
        return result({'source':'mock-prometheus','promql':promql,'value':92.4,'unit':'%'})
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(f'{url.rstrip("/")}/api/v1/query', params={'query':promql})
            response.raise_for_status()
            return result({'source':'prometheus','promql':promql,'result':response.json().get('data', {})})
    except Exception as exc:
        log.warning('prometheus_fallback', error=str(exc)); return result({'source':'mock-prometheus','promql':promql,'value':92.4,'unit':'%'}, error=str(exc))

