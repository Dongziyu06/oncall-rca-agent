import json, structlog
log=structlog.get_logger()
def bounded(value,limit=2000):
 text=value if isinstance(value,str) else json.dumps(value,ensure_ascii=False,default=str); marker='[TRUNCATED]'; return text if len(text)<=limit else text[:limit-len(marker)]+marker
def result(data=None,error=None):
 if data is None:return {'error':error,'data':None}
 encoded=json.dumps(data,ensure_ascii=False,default=str); return {'error':error,'data':data if len(encoded)<=2000 else bounded(encoded)}
