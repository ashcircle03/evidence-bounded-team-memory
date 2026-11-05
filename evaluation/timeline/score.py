"""Separate mechanical checks from source-based semantic review of each proposal."""
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import re
from .build import HERE,ROOT,write


def norm(text):return re.sub(r'\s+',' ',text.casefold()).strip().rstrip('.')


def contains_answer(text,alias):
    text,alias=norm(text),norm(alias)
    return bool(re.search(r'(?<![\w.])'+re.escape(alias)+r'(?![\w.%])',text))


def grade_qa(answer,key):
    got=answer.get('answers',[]);expected=key['answers'];errors=[]
    if answer['kind']!=key['kind']:errors.append('kind')
    if len(got)!=len(expected):errors.append('answer_count')
    for gold in expected:
        a=next((a for a in got if a['source_id']==gold['source_id']),None)
        if not a:errors.append('source');continue
        if not any(contains_answer(a['answer'],alias) for alias in gold['aliases']):errors.append('answer')
        if any(contains_answer(a['answer'],alias) for other in expected if other['source_id']!=gold['source_id']
               for alias in other['aliases'] if alias not in gold['aliases']):errors.append('mixed_answer_values')
        if a['status']!=gold['status']:errors.append('review_status')
        condition=(a.get('condition') or {}).get('quote','')+' '+a['quote']
        if gold['condition'] and norm(gold['condition']) not in norm(condition):errors.append('condition')
    return dict(correct=not errors,errors=errors)


def collect(source,keyfile,out):
    data=json.loads(source.read_text());keys=json.loads(keyfile.read_text());rows={};cards={}
    for uid,s in data['streams'].items():
        key=keys[s['id']];qa={};alerts=[];relations=[];errors=[]
        for step in s['steps']:
            r=step['result']
            if step['op']=='ask':qa[step['id']]=dict(**grade_qa(r,key['qa'][step['id']]),answer=r)
            elif step['op']=='ingest':
                errors.extend(r['errors'])
                for p in r['relations']:
                    pair=(p['previous']['source_id'],p['incoming']['source_id'])
                    target=pair==(key['old'],key['new'])
                    correct_kind=p['kind']==key['expected_relation']
                    valid=target and correct_kind
                    card=None
                    if valid:
                        body=dict(kind=p['kind'],old=p['previous']['quote'],new=p['incoming']['quote'],reason=p['reason'],
                                  old_source=key['old_text'],new_source=key['new_text'])
                        card=sha256(json.dumps(body,ensure_ascii=False,sort_keys=True).encode()).hexdigest()[:12]
                        cards[card]=body
                    item=dict(proposal=p,expected_target=target,expected_kind=correct_kind,card=card)
                    relations.append(item)
                    if p['kind'] in ('reconsider','conflict','correction'):alerts.append(item)
        natural_ids=[x for x in qa if x.startswith('natural_')]
        rows[uid]=dict(id=s['id'],mode=s['mode'],type=key['kind'],expected_review=key['expected_review'],
            qa=qa,qa_correct=sum(q['correct'] for q in qa.values()),qa_total=len(qa),
            natural_correct=sum(qa[x]['correct'] for x in natural_ids),natural_total=len(natural_ids),
            alerts=alerts,relations=relations,errors=errors,calls=len(s['calls']),
            input_tokens=s['input_tokens'],output_tokens=s['output_tokens'],seconds=s['seconds'])
    out.mkdir(exist_ok=True);write(out/'rows.json',rows);write(out/'blind-cards.json',cards)
    return rows,cards


def aggregate(out):
    rows=json.loads((out/'rows.json').read_text());ratings=json.loads((out/'ratings.json').read_text());summary={}
    for uid,r in rows.items():
        for group in ('alerts','relations'):
            for item in r[group]:item['grounded']=bool(item['card'] and ratings[item['card']]['ok'])
        r['grounded_review']=r['expected_review'] and any(a['grounded'] for a in r['alerts'])
        r['unsupported_alerts']=sum(not a['grounded'] for a in r['alerts'])
        r['correct_relation']=any(a['grounded'] for a in r['relations']) if r['type']!='irrelevant' else not r['relations']
    for mode in ('direct','indexed'):
        rs=[r for r in rows.values() if r['mode']==mode]
        summary[mode]=dict(streams=len(rs),required_review=sum(r['expected_review'] for r in rs),
            grounded_reviews=sum(r['grounded_review'] for r in rs),unsupported_alerts=sum(r['unsupported_alerts'] for r in rs),
            no_review_streams_with_alert=sum(not r['expected_review'] and bool(r['alerts']) for r in rs),
            relation_correct=sum(r['correct_relation'] for r in rs),qa_correct=sum(r['qa_correct'] for r in rs),qa_total=sum(r['qa_total'] for r in rs),
            natural_qa_correct=sum(r['natural_correct'] for r in rs),natural_qa_total=sum(r['natural_total'] for r in rs),
            parser_errors=sum(len(r['errors']) for r in rs),calls=sum(r['calls'] for r in rs),
            input_tokens=sum(r['input_tokens'] for r in rs),output_tokens=sum(r['output_tokens'] for r in rs),seconds=sum(r['seconds'] for r in rs))
    write(out/'rows.json',rows);write(out/'summary.json',summary);print(json.dumps(summary,indent=2))


if __name__=='__main__':
    import sys
    out=Path(sys.argv[3]);collect(Path(sys.argv[1]),Path(sys.argv[2]),out)
    if (out/'ratings.json').exists():aggregate(out)
