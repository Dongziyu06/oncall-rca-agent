import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import asyncio
from tools.k8s_tools import get_pod_status
from tools.prometheus_tools import query_metric
async def main():
 k=await get_pod_status('vlb'); p=await query_metric('up'); print('k8s_source=',k.get('data',{}).get('source') if isinstance(k.get('data'),dict) else 'unknown'); print('k8s_data=',k.get('data')); print('prometheus_source=',p.get('data',{}).get('source') if isinstance(p.get('data'),dict) else 'unknown'); print('prometheus_data=',p.get('data'))
asyncio.run(main())

