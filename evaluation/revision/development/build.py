import sys, json
from pathlib import Path
from evaluation.team_pilot.pilot import envelope, write, dev_sources
from evaluation.revision.run import build
import argparse
ap=argparse.ArgumentParser(description="Reconstruct the development inputs with the January EverMem source file")
ap.add_argument("ever",type=Path)
ap.add_argument("output",type=Path)
args=ap.parse_args()
aim=Path(__file__).resolve().parent
sys.path.insert(0,str(aim))
from cases import cases as aimers
docs={}; cases=[]
for label,goal,hist,new in aimers(aim):
    history=[]
    for j,e in enumerate(hist):
        k=f'{label}-{j}'; docs[k]=e;history.append(k)
    docs[label]=new
    cases.append(dict(id=label,goal=goal,task='review',history=history,incoming=label,as_of=new['observed_at'],arms=['simple','premise']))
ever=dev_sources(args.ever)
docs.update({k:r[0] for k,r in ever.items()})
old=json.loads((aim/'ever-questions.json').read_text())
for d in old['answers']:
    cases.append(dict(id=d['id'],question=d['question'],task='qa',history=list(ever),as_of='2025-02-01T00:00:00Z',arms=['simple','premise']))
for i,(s,t,q) in enumerate([
    ('For Atlas, the approved inspection interval is at least 14 days.','For Atlas, the approved inspection interval is at least 28 days.','What is the approved inspection interval for Atlas?'),
    ('In the coastal installation, the Delta controller samples every 45 seconds.','In the inland installation, the Delta controller samples every 75 seconds.','How frequently does the Delta controller sample at the installations?'),
    ('The Harbor parser uses UTF-8 as the default wire encoding.','The Harbor parser switched to weekly bug triage.','What is the default wire encoding of the Harbor parser?')]):
    ks=[]
    for j,txt in enumerate((s,t,'The Vega project held an afternoon meeting.')):
        k=f'probe{i}-{j}';docs[k]=envelope(txt,'notes/'+k,['Sam','Joe','Ada'][j]);ks.append(k)
    for tag,hh in [('joint',ks),('first',[ks[0]]),('second',[ks[1]])]:
        cases.append(dict(id=f'probe{i}-{tag}',task='qa',history=hh,as_of='2026-11-04T00:00:00Z',question=q,arms=['simple','premise']))
data=dict(documents=docs,cases=cases)
write(args.output,data)
