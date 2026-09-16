from pathlib import Path
import re,os,json
ROOT=Path(__file__).resolve().parent.parent/'runbooks'
def parse_frontmatter(text):
 meta={}
 if text.startswith('---'):
  end=text.find('---',3)
  if end>=0:
   for line in text[3:end].splitlines():
    if ':' in line:
     k,v=line.split(':',1);meta[k.strip()]=v.strip().strip('"\'')
 return meta
def load_documents(root=ROOT):
 docs=[]
 for path in root.rglob('*.md'):
  text=path.read_text(encoding='utf-8-sig'); meta=parse_frontmatter(text); docs.append({'id':meta.get('id',path.stem),'text':text,'metadata':{**meta,'path':str(path.relative_to(root))}})
 return docs
def ingest(persist_dir='.chroma'):
 docs=load_documents();
 try:
  import chromadb
  client=chromadb.PersistentClient(path=persist_dir); col=client.get_or_create_collection('runbooks')
  if docs: col.upsert(ids=[d['id'] for d in docs],documents=[d['text'] for d in docs],metadatas=[d['metadata'] for d in docs])
  return len(docs)
 except Exception as exc:
  print('Chroma unavailable:',exc); return len(docs)
if __name__=='__main__': print('indexed',ingest(os.getenv('CHROMA_PERSIST_DIR','.chroma')))
