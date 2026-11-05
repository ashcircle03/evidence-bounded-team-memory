"""Expose full per-condition model outputs and exact in-document source validation."""
from pathlib import Path
from evaluation.decision_records.build import read,save,ROOT
from evaluation.contrast_review.score import card

HERE=Path(__file__).parent
OUT=ROOT/'results/context_review'

def run():
    inp={r['id']:r for r in read(HERE/'dev-inputs.json')}
    keys=read(HERE/'dev-key.json')
    result=read(OUT/'development.json')
    cards={};links={}
    for uid,row in result['results'].items():
        k=keys[uid];r=row['result'];spec=inp[uid]
        lines=[]
        for field in ('failure','condition'):
            value=r[field]['parsed']
            if value['status'] not in ('answered','unresolved'):
                lines.append(dict(field=field,status=value['status'],raw=r[field]['raw']))
                continue
            for w in value['answers']:
                text=next(p['quote'] for p in spec['passages'] if p['source_id']==w['source_id'] and p['start']==w['start'])
                assert text==w['quote']
                lines.append(dict(field=field,status=value['status'],answer=w['answer'],
                                  correct_document=w['source_id']==spec['report_id'],quote=w['quote']))
        cid=card(cards,'failure and condition',dict(behavior=k['behavior'],condition=k['condition']),
                 spec['passages'],dict(extractions=lines,rationale=r['rationale']))
        links[uid]=cid
    save(OUT/'dev-cards.json',dict(sorted(cards.items())))
    save(OUT/'dev-card-index.json',links)
    if (OUT/'dev-ratings.json').exists():
        ratings=read(OUT/'dev-ratings.json');assert set(cards)==set(ratings)
        save(OUT/'dev-scores.json',{uid:dict(keys[uid],score=ratings[cid]) for uid,cid in links.items()})

if __name__=='__main__':run()
