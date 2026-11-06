"""Portable QA20 packet checks and explicit source-based rating aggregation.

Python standard library only. No inference, network, or automatic semantic judge.
Run `python evaluate.py --help` from any directory.
"""
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def read(path):
    return json.loads(Path(path).read_text(encoding='utf8'))


def lines(path):
    return [json.loads(line) for line in Path(path).read_text(encoding='utf8').splitlines() if line.strip()]


def dump(value):
    return json.dumps(value, ensure_ascii=False, indent=2)


def source_id(envelope):
    # Same canonical serialization as team_memory.store; frozen envelopes are
    # already normalized. Preserve all original whitespace and timestamps.
    return sha256((json.dumps(envelope, ensure_ascii=False, sort_keys=True, indent=2)+'\n').encode()).hexdigest()[:24]


def verify():
    manifest = read(ROOT/'manifest.json')
    for name, expected in manifest['files_sha256'].items():
        if sha256((ROOT/name).read_bytes()).hexdigest() != expected:
            raise ValueError('Packet hash mismatch: '+name)
    inputs = read(ROOT/'data/inputs.json')
    questions = lines(ROOT/'data/questions.jsonl')
    derived = [dict(id=c['id']+'/'+e['label'],history_id=c['id'],label=e['label'],question=e['question'])
               for c in inputs['cases'] for e in c['events'] if e['operation']=='ask']
    if questions != derived or len(questions) != 20 or len(inputs['cases']) != 7:
        raise ValueError('Question order or coverage mismatch')
    return inputs, questions


def predictions(path, questions):
    items = lines(path)
    ids = [q['id'] for q in questions]
    if len(items) != 20 or len({x['id'] for x in items}) != 20 or {x['id'] for x in items} != set(ids):
        raise ValueError('Exactly one prediction for each of the20 IDs is required')
    by_id = {x['id']: x for x in items}
    for item in items:
        if not isinstance(item.get('answer'), str) or not isinstance(item.get('citations'), list):
            raise ValueError('Each prediction needs answer:string and citations:list')
    return by_id


def check_citations(items, inputs):
    histories = {c['id']:{source_id(r):r for e in c['events'] for r in e.get('records',[])} for c in inputs['cases']}
    errors = []
    for cid, item in items.items():
        originals = histories[cid.rsplit('/',1)[0]]
        for w in item['citations']:
            src = originals.get(w.get('source_id'),{}).get('source',{})
            start,end = w.get('start'),w.get('end')
            valid = (type(start) is int and type(end) is int and
                     ('number' not in w or (type(w['number']) is int and w['number']>0)) and
                     isinstance(w.get('quote'),str) and bool(w['quote']) and
                     0 <= start < end <= len(src.get('text','')) and
                     src['text'][start:end] == w['quote'] and
                     all(w.get(k,src.get(k)) == src.get(k) for k in ('speaker','location')))
            if not valid: errors.append(dict(id=cid,source_id=w.get('source_id')))
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command',required=True)
    sub.add_parser('verify')
    p=sub.add_parser('requests');p.add_argument('--out',type=Path,required=True)
    p=sub.add_parser('collect');p.add_argument('--responses',type=Path,required=True)
    p=sub.add_parser('ratings');p.add_argument('--predictions',type=Path,required=True)
    p=sub.add_parser('score');p.add_argument('--predictions',type=Path,required=True);p.add_argument('--ratings',type=Path,required=True)
    args=parser.parse_args();inputs,questions=verify()
    if args.command=='verify':
        print(dump(dict(packet_valid=True,histories=7,questions=20,semantic_grading=False)));return
    if args.command=='requests':
        # Actor input contains no answer key or preselected evidence.
        args.out.mkdir(parents=True,exist_ok=False)
        for c in inputs['cases']:
            requests=[{k:v for k,v in e.items() if k!='label'} for e in c['events']]
            (args.out/(c['id']+'.jsonl')).write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in requests),encoding='utf8')
        print(dump(dict(histories=7,questions=20,output=str(args.out))));return
    if args.command=='collect':
        collected=[]
        for c in inputs['cases']:
            responses=lines(args.responses/(c['id']+'.jsonl'))
            if len(responses)!=len(c['events']):raise ValueError('Missing/extra response lines for '+c['id'])
            for event,result in zip(c['events'],responses):
                if event['operation']!='ask':continue
                citations=[]
                for answer in result.get('answers',[]):
                    for witness in answer.get('evidence',[]):
                        citation=dict(witness)
                        for number,source in enumerate(result.get('citation_sources',[]),1):
                            if all(source.get(k)==witness.get(k) for k in ('source_id','start','end','quote')):
                                citation['number']=number;break
                        citations.append(citation)
                collected.append(dict(id=c['id']+'/'+event['label'],answer=result.get('raw',''),
                    citations=citations,
                    status=result.get('status','unknown')))
        for item in collected:print(json.dumps(item,ensure_ascii=False))
        return
    items=predictions(args.predictions,questions)
    prediction_hash=sha256(args.predictions.read_bytes()).hexdigest()
    if args.command=='ratings':
        print(dump(dict(predictions_sha256=prediction_hash,evaluator='',
            ratings={q['id']:dict(answer_correct=None,citations_support_answer=None,
                unsupported_extra_claims=None,claim_level_citation_gap=None,reason='') for q in questions})))
        return
    ratings=read(args.ratings)
    if ratings.get('predictions_sha256')!=prediction_hash:raise ValueError('Ratings belong to different predictions')
    rs=ratings['ratings']
    if set(rs)!=set(items):raise ValueError('Rating IDs differ from predictions')
    key=read(ROOT/'evaluator/key.json')['cases'];counts={};total=0;gaps=[]
    invalid=check_citations(items,inputs);invalid_ids={w['id'] for w in invalid}
    for cid,r in rs.items():
        if any(type(r.get(k)) is not bool for k in ('answer_correct','citations_support_answer','unsupported_extra_claims')) or not r.get('reason','').strip():
            raise ValueError('Unrated case or missing explanation: '+cid)
        # Claim completeness is a separate diagnostic, not a change to the
        # historical required-answer rubric. Do not infer missing labels as false.
        passed = (r['answer_correct'] and r['citations_support_answer'] and not r['unsupported_extra_claims']
                  and bool(items[cid]['answer'].strip()) and bool(items[cid]['citations']) and cid not in invalid_ids
                  and items[cid].get('status') not in ('error','not_executed','needs_rebuild'))
        total+=int(passed)
        history,label=cid.rsplit('/',1);corpus=key[history]['questions'][label]['corpus']
        bucket=counts.setdefault(corpus,dict(correct=0,total=0));bucket['correct']+=int(passed);bucket['total']+=1
        if r.get('claim_level_citation_gap') is True:gaps.append(cid)
    print(dump(dict(answer_and_required_citation=total,total=20,by_corpus=counts,
        invalid_original_citations=invalid,known_extra_sentence_citation_gaps=gaps,
        gap_labels_provided=sum(type(r.get('claim_level_citation_gap')) is bool for r in rs.values()),
        statuses=dict(Counter(x.get('status','unspecified') for x in items.values())),
        predictions_sha256=prediction_hash,evaluator=ratings.get('evaluator','unspecified'),
        semantic_ratings_supplied_by_evaluator=True,automatic_semantic_judging=False)))


if __name__=='__main__':
    main()
