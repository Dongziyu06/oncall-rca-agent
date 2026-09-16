from typing import Any,TypedDict
from langgraph.graph import StateGraph,END
from api.models import AlertRequest
from api.state import TASKS
from agents.router import classify_alert
from tools.prometheus_tools import query_metric
from tools.k8s_tools import get_pod_status
from agents.runbook_agent import runbook_agent
from agents.summarize import build_report
from agents.follow_up import generate_follow_up,format_follow_up
class RCAState(TypedDict,total=False): task_id:str;alert:dict[str,Any];route:dict;evidence:dict;report:str;follow_up:dict|None
async def _emit(t,n,s,**x): await TASKS[t]['queue'].put({'type':'progress','node':n,'status':s,**x})
async def run_workflow(task_id,payload:AlertRequest):
 a=payload.alerts[0] if payload.alerts else None; alert={'alertname':a.labels.alertname if a else 'NaturalLanguage','service':a.labels.service if a and a.labels.service else 'demo','description':a.annotations.get('description','') if a else (payload.description or '')}; baseline=getattr(payload,'baseline',False)
 async def router(s): await _emit(task_id,'Router','started');s['route']=(await classify_alert(alert['alertname'],alert['description']))['data'];await _emit(task_id,'Router','completed',result=s['route']);return s
 async def metric(s): await _emit(task_id,'MetricAgent','started');s.setdefault('evidence',{})['metric']=(await query_metric('up{job="rca-demo"}'))['data'];await _emit(task_id,'MetricAgent','completed');return s
 async def k8s(s): await _emit(task_id,'K8sAgent','started');s.setdefault('evidence',{})['k8s']=(await get_pod_status(alert['service']))['data'];await _emit(task_id,'K8sAgent','completed');return s
 async def runbook(s): await _emit(task_id,'RunbookAgent','started');s['evidence']['runbook']=(await runbook_agent(s['route']['fault_type'],alert['description']))['data'];await _emit(task_id,'RunbookAgent','completed');return s
 async def summarize(s): await _emit(task_id,'Summarize','started');s['report']=await build_report(s['route'],s['evidence']);await _emit(task_id,'Summarize','completed');return s
 async def followup(s):
  await _emit(task_id,'FollowUpAgent','started');s['follow_up']=await generate_follow_up(s['route']['fault_type'],s.get('evidence',{}),s['report']);
  if s['follow_up'].get('needs_follow_up'):s['report']+=format_follow_up(s['follow_up'])
  await _emit(task_id,'FollowUpAgent','completed',result=s['follow_up']);return s
 async def report(s): await _emit(task_id,'Report','started');TASKS[task_id]['report']=s['report'];await TASKS[task_id]['queue'].put({'type':'report','report':s['report']});return s
 async def baseline_summarize(s): await _emit(task_id,'Summarize','started');s['evidence']={};s['report']=await build_report(s['route'],s['evidence']);await _emit(task_id,'Summarize','completed');return s
 g=StateGraph(RCAState)
 if baseline:
  for n,f in [('router',router),('summarize',baseline_summarize),('report',report)]:g.add_node(n,f)
  g.set_entry_point('router');g.add_edge('router','summarize');g.add_edge('summarize','report');g.add_edge('report',END)
 else:
  for n,f in [('router',router),('metric',metric),('k8s',k8s),('runbook',runbook),('summarize',summarize),('followup',followup),('report',report)]:g.add_node(n,f)
  g.set_entry_point('router')
  for a,b in [('router','metric'),('metric','k8s'),('k8s','runbook'),('runbook','summarize'),('summarize','followup'),('followup','report'),('report',END)]:g.add_edge(a,b)
 await g.compile().ainvoke({'task_id':task_id,'alert':alert});TASKS[task_id]['done']=True
