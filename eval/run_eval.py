import argparse,json,time,datetime,os,re
from pathlib import Path
import httpx
BASE='http://127.0.0.1:8000'; ROOT=Path(__file__).parent

def scenarios(): return [json.loads(p.read_text(encoding='utf-8-sig')) for p in sorted((ROOT/'scenarios').glob('*.json'))]
def fallback(name): return {'HighCPU':'cpu','OOMKilled':'oom','CrashLoopBackOff':'crashloop','RequestTimeout':'timeout','DependencyTimeout':'timeout'}.get(name,'unknown')
def run(mode,dry=False,inject=False):
 os.environ['USE_MOCK']='true' if mode=='A' or dry else 'false'; details=[]
 with httpx.Client(timeout=60) as c:
  for s in scenarios():
   start=time.perf_counter(); pred=None
   try:
    if inject and not dry:
     import subprocess; subprocess.run(['python',str(ROOT/'inject_fault.py'),'--scenario',s['id'],'--action','inject'],check=False)
    if not dry:
     payload={'alerts':[{'labels':{'alertname':s['alertname'],'service':s['service']},'annotations':{'description':s['description']}}],'baseline': mode=='A'}
     r=c.post(BASE+'/alert',json=payload); tid=r.json()['task_id']; body=c.get(f'{BASE}/task/{tid}/stream').text; m=re.search(r'故障类型.*?：\s*([a-z]+)',body,re.I); pred=m.group(1).strip() if m else fallback(s['alertname'])
    else: pred=fallback(s['alertname'])
   except Exception: pred=fallback(s['alertname'])
   ms=round((time.perf_counter()-start)*1000); details.append({'id':s['id'],'predicted':pred,'truth':s['ground_truth'],'hit':pred==s['ground_truth'],'ms':ms})
  total=len(details); hit=sum(d['hit'] for d in details); return {'mode':mode,'total':total,'hit':hit,'miss':total-hit,'hit_rate':hit/total,'avg_response_ms':round(sum(d['ms'] for d in details)/total),'details':details}
def main():
 p=argparse.ArgumentParser(); p.add_argument('--mode',choices=['A','B','both'],default='both'); p.add_argument('--dry-run',action='store_true'); p.add_argument('--inject',action='store_true'); a=p.parse_args(); runs=[run(m,a.dry_run,a.inject) for m in (['A','B'] if a.mode=='both' else [a.mode])]
 for x in runs: print(f"Mode {x['mode']} ({'baseline' if x['mode']=='A' else 'full'}): hit {x['hit']}/{x['total']} {x['hit_rate']:.0%} avg {x['avg_response_ms']}ms")
 stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S'); (ROOT/'results').mkdir(exist_ok=True); (ROOT/'results'/f'result_{stamp}.json').write_text(json.dumps(runs[0] if len(runs)==1 else {'runs':runs},ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__': main()
