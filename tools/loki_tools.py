import os, httpx
from .common import result, log
async def query_logs(service, time_range='5m', keyword=None):
    url=os.getenv('LOKI_URL'); log.info('query_logs',service=service,time_range=time_range,keyword=keyword,backend='loki' if url else 'mock')
    if os.getenv('USE_MOCK','false').lower()=='true' or not url: return result({'source':'mock-loki','service':service,'keyword':keyword,'logs':[]})
    try:
        query=f'{{app="{service}"}}' + (f' |= `{keyword}`' if keyword else '')
        async with httpx.AsyncClient(timeout=5) as client:
            r=await client.get(f'{url.rstrip("/")}/loki/api/v1/query_range',params={'query':query,'limit':50}); r.raise_for_status()
            return result({'source':'loki','service':service,'result':r.json().get('data',{})})
    except Exception as exc: return result({'source':'mock-loki','service':service,'keyword':keyword,'logs':[]},error=str(exc))

