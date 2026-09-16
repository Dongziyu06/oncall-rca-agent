import argparse,json,subprocess,time
from pathlib import Path
ROOT=Path(__file__).parent/'scenarios'
def main():
 p=argparse.ArgumentParser(); p.add_argument('--scenario',required=True); p.add_argument('--action',choices=['inject','cleanup'],required=True); p.add_argument('--wait',type=int,default=10); a=p.parse_args(); s=json.loads((ROOT/f'{a.scenario.lower()}.json').read_text(encoding='utf-8-sig')); cmd=s[a.action+'_cmd'];
 try: subprocess.run(cmd,shell=True,check=False); print(f'{a.action}: {s["id"]}')
 except Exception as e: print(f'kubectl skipped: {e}')
 if a.action=='inject' and a.wait: time.sleep(a.wait)
if __name__=='__main__': main()
