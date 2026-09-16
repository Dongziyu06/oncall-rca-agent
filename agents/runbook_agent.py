from rag.retriever import retrieve
async def runbook_agent(fault_type, description=''):
    return {'error':None,'data':retrieve(f'{fault_type} {description}')}
