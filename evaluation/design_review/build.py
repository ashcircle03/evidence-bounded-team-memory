"""Freeze a paired diagnostic panel from pre-existing cases; no new-test claim."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import random

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).parent
# Zero-based original paragraphs inspected before any design-audit model outputs.
WINDOWS={
 'patch-search':([1],[2,3,4,5]),'asan-preload':([1,2],[1,2,3,4]),
 'email-priority':([1,2],[1,2,5]),'commit-permissions':([1],[1,2,3]),
 'help-spacing':([1],[1,7]),'http-index':([1,4],[1,2,7,9]),
 'make-info':([1,2,6],[1,3,6,7,8,9]),'freebsd-cwd':([1],[1,3]),
 'fsck-empty':([1],[1,2,3]),'dir-diff':([1,2],[1,3]),
 'hook':([2,4],[1,2]),'header':([1,2],[1,2,3,4]),
 'reflog':([2,3],[0,1,2]),'prompt':([1],[1,2]),'range':([1,2,3],[1,2])}

def write(path,x):path.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')

def build():
 rows=[];keys={};oracle={};audit=[]
 for folder in ['context_review','role_review','contrast_review/validation']:
  source=ROOT/'evaluation'/folder
  data=json.loads((source/'inputs.json').read_text());labels=json.loads((source/'key.json').read_text())
  for item in data:
   key=labels[item['id']]
   if key['scenario'] not in ('mixed','no-match'):continue
   row=deepcopy(item);row.pop('check_order',None)
   uid=key['topic']+'/'+key['scenario']+'/'+key['view'];row['id']=uid
   rows.append(row);keys[uid]=dict(key,origin=str(source.relative_to(ROOT)),origin_id=item['id'])
   if key['view']!='hidden':continue
   old_idx,new_idx=WINDOWS[key['topic']]
   chosen={}
   for i,doc in enumerate(row['prior']):
    text=doc['source']['text'];paras=text.split('\n\n')
    if doc['source']['location']==key['earlier']:indices=old_idx
    elif doc['source']['location']==key['alternative']:
     indices=[j for j,p in enumerate(paras) if any(p.strip()==q.strip() for q in key['foil']) and j>0]
     if not indices:indices=list(range(1,min(4,len(paras))))
    else:indices=list(range(1,min(4,len(paras))))
    if not indices:indices=[0] # Some genuine Git records consist only of a subject.
    chosen['P'+str(i)]=indices
   chosen['N']=new_idx;oracle[uid]=chosen
   audit.append(dict(id=uid,criterion=key['rubric'],documents=[
    dict(id='P'+str(i),location=d['source']['location'],paragraphs={str(j):d['source']['text'].split('\n\n')[j] for j in chosen['P'+str(i)]}) for i,d in enumerate(row['prior'])]+
    [dict(id='N',location=row['incoming']['source']['location'],paragraphs={str(j):row['incoming']['source']['text'].split('\n\n')[j] for j in new_idx})]))
 random.Random(91073).shuffle(rows)
 assert len(rows)==60 and len(oracle)==30 and len(WINDOWS)==15
 write(HERE/'inputs.json',rows);write(HERE/'key.json',keys);write(HERE/'oracle-windows.json',oracle)
 write(HERE/'oracle-audit.json',audit)

def freeze():
 paths=list((ROOT/'team_memory').glob('*.py'))+list(HERE.glob('*.py'))
 paths += [HERE/n for n in ['inputs.json','key.json','oracle-windows.json','oracle-audit.json','PROTOCOL.md']]
 write(HERE/'freeze.json',{'files':{str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}})

if __name__=='__main__':build()
