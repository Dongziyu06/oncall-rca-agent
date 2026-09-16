import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from rag.retriever import retrieve
queries=['CPU throttling pod resource limits','OOMKilled exit code 137 memory','CrashLoopBackOff container restart','service timeout latency high','node not ready kubelet']
for q in queries:
 print(f'\nQUERY: {q}')
 for i,d in enumerate(retrieve(q,3),1):
  m=d.get('metadata',{}); print(f"{i}. id={d.get('id')} fault_type={m.get('fault_type','unknown')} score={d.get('score',d.get('rrf_score',0)):.4f}"); print(d.get('text','')[:200].replace('\n',' '))
