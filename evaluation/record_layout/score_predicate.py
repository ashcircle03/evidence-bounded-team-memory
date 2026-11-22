"""Ground predicate-conditioned QA answers in frozen records; never infer a coreferent."""
import hashlib
import json
import re
import sys
from pathlib import Path

from evaluation.record_layout.score import edges

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'results/record-layout'
TOKEN=re.compile(r"\w+(?:['’]\w+)*|[^\w\s]")


def unique_span(text, answer):
    tokens=list(TOKEN.finditer(text))
    needle=TOKEN.findall(answer)
    words=[m.group() for m in tokens]
    matches=[(m.start(),tokens[i+len(needle)-1].end()) for i,m in enumerate(tokens)
             if needle and words[i:i+len(needle)]==needle]
    return matches[0] if len(matches)==1 else None


def project(question,answer):
    question=' '.join(question.lower().replace('_',' ').split())
    if re.match(r'^what (?:did|does|do|would|could|can|will|might|should) (?:someone|somebody|something) ',question):
        # A direct affected object, not an oblique argument such as "with what".
        if re.search(r'\b(?:to|for|from|about|at|with|in|on|by|of|as)\s*\?$',question):
            return None
        if answer.strip().lower() not in {'it','them','this','that','him','her','they'}:
            return 'subject'
    if question.startswith('when ') and re.match(r'^(?:if|when|unless|provided that|only if)\b',answer,re.I):
        return 'condition'
    return None


def attach(source,graph,row):
    units={u['id']:u for u in graph['units']}
    p,q=row['predicate']; actions=set()
    for claim in graph['claims']:
        for a in claim['assertions']:
            ids=a['unit_ids']; start,end=units[ids[0]]['start'],units[ids[-1]]['end']
            if start<=p<q<=end:
                actions.add((start,end))
    result=[]
    for qa in row['qas']:
        for answer in qa['answers']:
            span=unique_span(source,answer)
            role=project(qa['question'],answer)
            edge=None
            if role and span and len(actions)==1:
                edge=(*next(iter(actions)),*span,role)
            result.append(dict(question=qa['question'],answer=answer,span=span,role=role,edge=edge))
    return result


def main(job):
    freeze=json.loads((OUT/'predicate-pilot-freeze.json').read_text())
    panel=ROOT/'evaluation/record_layout'
    assert hashlib.sha256((panel/'key.json').read_bytes()).hexdigest()==freeze['key_sha256']
    assert hashlib.sha256((panel/'predicate_pilot.py').read_bytes()).hexdigest()==freeze['entry_sha256']
    cache=ROOT/'.cache/answer-versions'
    old=json.loads((cache/'versions-124840.json').read_text())['arms']['current']
    raw=json.loads((cache/f'versions-{job}.json').read_text())
    assert raw['job']==job and raw['status']=='complete' and raw['revision']==freeze['model']
    assert raw['input']==hashlib.sha256((panel/'inputs.json').read_bytes()).hexdigest()
    assert set(raw['rows'])==set(freeze['cases'])-set(freeze['unsupported'])
    gold={r['id']:set(map(tuple,r['edges'])) for r in json.loads((panel/'key.json').read_text())}
    docs={s['id']:s['text'] for s in json.loads((panel/'inputs.json').read_text())['documents']}
    result={}
    for iid in freeze['cases']:
        row=raw['rows'].get(iid)
        previous=set(edges(old[iid]['graph'],docs[iid]))
        predicted=attach(docs[iid],old[iid]['graph'],row) if row else []
        candidate={x['edge'] for x in predicted if x['edge']}
        result[iid]=dict(supported=row is not None,source=docs[iid],output=row,projected=predicted,
                         exact=sorted(candidate & gold[iid]),gained=sorted((candidate-previous)&gold[iid]),
                         newly_wrong=sorted(candidate-previous-gold[iid]),previous_exact=sorted(previous&gold[iid]))
    passed=any(r['gained'] for r in result.values()) and bool(result['meeting-08']['exact']) and not any(r['newly_wrong'] for r in result.values())
    (OUT/'predicate-pilot-score.json').write_text(json.dumps(dict(job=job,pass_gate=passed,cases=result),
                                                               indent=2,ensure_ascii=False)+'\n')
    for k,v in result.items():print(k,v['projected'],v['exact'],v['newly_wrong'])
    print('gate',passed)

if __name__=='__main__':main(sys.argv[1])
