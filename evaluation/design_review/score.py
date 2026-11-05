"""Source validation, method-blinded semantic cards, and paired panel summaries."""
from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path
from .build import ROOT,HERE,write

OUT=ROOT/'results/design_review'

def collect():
 inputs={r['id']:r for r in json.loads((HERE/'inputs.json').read_text())}
 keys=json.loads((HERE/'key.json').read_text())
 results={}
 for model,file in [('3b','small.json'),('14b','large.json'),('14b','large-factorial.json')]:
  if not (OUT/file).exists():continue
  data=json.loads((OUT/file).read_text())
  for uid,r in data['results'].items():results[model+'/'+uid]=dict(r,model=model)
 repair=json.loads((OUT/'oracle-repair.json').read_text())
 for uid,r in repair['results'].items():
  if r['method']=='direct-oracle':results['3b/'+uid]=dict(r,model='3b',input_repair=True)
 cards={};rows={}
 for uid,r in results.items():
  k=keys[r['case']];inp=inputs[r['case']];pred=r['result'];action=pred['action'];opened=action in ('reassess','retest')
  docs={d['source']['location']:d for d in inp['prior']+[inp['incoming']]}
  old=pred.get('previous',[]);new=pred.get('incoming',[])
  if isinstance(old,dict):old=[old]
  if isinstance(new,dict):new=[new]
  valid=bool(old and new)
  for w in old+new:
   src=docs.get(w.get('location'),{}).get('source',{})
   text=src.get('text','');ok=bool(w.get('quote') and w['quote'] in text and w.get('speaker')==src.get('speaker'))
   if 'start' in w:ok=ok and text[w['start']:w['end']]==w['quote']
   valid=valid and ok
  target=bool(old) and all(w['location']==k['earlier'] for w in old)
  new_source=bool(new) and all(w['location']==k['report'] for w in new)
  card_id=None
  if k['expected']=='review' and opened and target and new_source and valid:
   card=dict(criterion=k['rubric'],old=[w['quote'] for w in old],new=[w['quote'] for w in new],reason=pred.get('rationale',''))
   card_id=sha256(json.dumps(card,sort_keys=True,ensure_ascii=False).encode()).hexdigest()[:12]
   cards[card_id]=card
  rows[uid]=dict(model=r['model'],case=r['case'],topic=k['topic'],view=k['view'],scenario=k['scenario'],method=r['method'],
        expected=k['expected'],action=action,opened=opened,target=target,citations_valid=valid,new_source=new_source,card_id=card_id,
        result=pred,input_tokens=r['input_tokens'],output_tokens=r['output_tokens'],calls=len(r['calls']),seconds=r['seconds'])
 OUT.mkdir(exist_ok=True);write(OUT/'blind-cards.json',dict(sorted(cards.items())));write(OUT/'rows.json',rows)
 print('semantic cards',len(cards),'rows',len(rows))
 return rows,cards

def aggregate():
 rows,cards=collect();ratings=json.loads((OUT/'ratings.json').read_text());assert set(ratings)==set(cards)
 counts=defaultdict(lambda:dict(n=0,positive=0,negative=0,grounded=0,proposed=0,false_positive=0,correct_keep=0,invalid=0,target=0,input_tokens=0,output_tokens=0,calls=0,seconds=0,successes=[]))
 for uid,r in rows.items():
  r['grounded']=bool(r['card_id'] and ratings[r['card_id']]['ok'])
  group='/'.join([r['model'],r['view'],r['method']]);g=counts[group]
  g['n']+=1;g['positive' if r['expected']=='review' else 'negative']+=1
  g['proposed']+=r['opened'];g['grounded']+=r['grounded'];g['target']+=r['opened'] and r['target']
  g['false_positive']+=r['expected']=='keep' and r['opened']
  g['correct_keep']+=r['expected']=='keep' and r['action']=='keep'
  g['invalid']+=r['action'] in ('invalid_output','execution_error')
  for name in ['input_tokens','output_tokens','calls','seconds']:g[name]+=r[name]
  if r['grounded']:g['successes'].append(r['topic'])
 write(OUT/'rows.json',rows);write(OUT/'counts.json',dict(counts))
 paired={}
 for topic in sorted({r['topic'] for r in rows.values()}):
  paired[topic]={}
  for uid,r in rows.items():
   if r['topic']==topic:paired[topic]['/'.join([r['model'],r['view'],r['scenario'],r['method']])]=dict(action=r['action'],grounded=r['grounded'],card=r['card_id'])
 write(OUT/'paired.json',paired)
 for k,v in counts.items():print(k, {f:v[f] for f in ('n','grounded','false_positive','correct_keep','invalid','calls','input_tokens')})

if __name__=='__main__':
 import sys
 if sys.argv[-1]=='collect':collect()
 else:aggregate()
