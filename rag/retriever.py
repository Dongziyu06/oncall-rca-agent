from .ingest import load_documents,ingest

def retrieve(query,top_k=3,persist_dir='.chroma'):
 docs=load_documents(); terms=set(query.lower().split()); sparse=[]
 for d in docs:
  hay=d['text'].lower(); score=sum(hay.count(t) for t in terms); sparse.append((score,d))
 sparse.sort(key=lambda x:x[0],reverse=True); dense=[]
 try:
  import chromadb
  c=chromadb.PersistentClient(path=persist_dir); col=c.get_or_create_collection('runbooks'); r=col.query(query_texts=[query],n_results=min(top_k,len(docs)))
  ids=r.get('ids',[[]])[0]; texts=r.get('documents',[[]])[0]; metas=r.get('metadatas',[[]])[0]; distances=r.get('distances',[[]])[0]
  for i,(ident,text,meta,dist) in enumerate(zip(ids,texts,metas,distances)): dense.append({'id':ident,'text':text,'metadata':meta or {},'score':1/(1+float(dist)),'distance':dist})
 except Exception: pass
 scores={}; byid={d['id']:d for d in docs}
 for rank,(_,d) in enumerate(sparse): scores[d['id']]=scores.get(d['id'],0)+1/(60+rank+1)
 for rank,d in enumerate(dense): scores[d['id']]=scores.get(d['id'],0)+1/(60+rank+1); byid[d['id']]={**byid.get(d['id'],{}),'score':d['score'],'metadata':d['metadata']}
 return [{**byid[i],'rrf_score':s} for i,s in sorted(scores.items(),key=lambda x:x[1],reverse=True)[:top_k]]
