"""Exact source positions and role; no text normalization or model judging."""
import json
import sys
from pathlib import Path


def edges(graph,text):
    units={u['id']:u for u in graph['units']}
    found={}
    for c in graph['claims']:
        assertions=c.get('assertions') or [dict(unit_ids=c['claim'])]
        for role in ('subject','condition'):
            runs=[]
            for uid in c[role]:
                u=units[uid]
                if runs and not text[runs[-1][1]:u['start']].strip():
                    runs[-1][1]=u['end']
                else:runs.append([u['start'],u['end']])
            for assertion in assertions:
                ids=assertion['unit_ids']
                for a,b in runs:
                    e=(units[ids[0]]['start'],units[ids[-1]]['end'],a,b,role)
                    found.setdefault(e,set()).add(c['id'])
    return found


def main(result_file):
    root=Path(__file__).resolve().parent
    raw=json.loads(Path(result_file).read_text())
    assert raw['status']=='complete'
    texts={s['id']:s['text'] for s in json.loads((root/'inputs.json').read_text())['documents']}
    rows=[]
    for item in json.loads((root/'key.json').read_text()):
        iid=item['id'];gold=set(map(tuple,item['edges']))
        row=dict(id=iid,split=item['split'],kind=item['kind'],arms={})
        for arm,results in raw['arms'].items():
            r=results[iid];pred=edges(r['graph'],texts[iid]);correct=gold & pred.keys()
            covered={e for e in correct if any(h['source_id']==iid and h['start']<=min(e[0],e[2])
                        and max(e[1],e[3])<=h['end'] for h in r['hits'])}
            views={v['claim_id'] for v in r['views'] if v['source_id']==iid}
            delivered={e for e in covered if views & pred[e]}
            row['arms'][arm]=dict(tp=sorted(correct),fp=sorted(pred.keys()-gold),fn=sorted(gold-correct),
                                  retrieval_loss=sorted(correct-covered),view_loss=sorted(covered-delivered))
        rows.append(row)
    totals={}
    for split in ('dev','test'):
        totals[split]={}
        for arm in raw['arms']:
            selected=[r['arms'][arm] for r in rows if r['split']==split]
            t={k:sum(len(r[k]) for r in selected) for k in selected[0]}
            t['micro_f1']=2*t['tp']/(2*t['tp']+t['fn']+t['fp'])
            totals[split][arm]=t
    report=dict(job=raw['job'],totals=totals,rows=rows)
    dest=Path('results/record-layout/score.json')
    dest.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(totals,indent=2))

if __name__=='__main__':main(sys.argv[1])
