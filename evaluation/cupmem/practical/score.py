"""Aggregate explicit source-based ratings; never use aliases as semantic judges."""
from collections import Counter, defaultdict
from hashlib import sha256
import gzip
import json
from pathlib import Path
import statistics

from team_memory.store import digest, source_envelope
from team_memory.timeline import valid_witness
from .prepare import write

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
OUT=ROOT/'results/cupmem/practical'
LEGACY=['legacy-pep-v1','legacy-git-a-v1','legacy-git-b-v1','legacy-ever-v1',
        'legacy-pep-rest-a-v1','legacy-pep-rest-b-v1']
TRANSFER=['transfer-a-v1','transfer-b-v1']


def read(path):return json.loads(path.read_text())


def success(rating):
    return rating['answer_correct'] is True and rating['citations_support_answer'] is True and not rating['unsupported_extra_claims']


def entries(name):
    folder=OUT/name;cards=read(folder/'cards.json');ratings=read(folder/'ratings.json')['ratings']
    assert set(ratings)==set(cards['cards']),name+' missing or extra ratings'
    for cid,meta in cards['mapping'].items():
        rating=ratings[cid];assert rating.get('reason','').strip()
        yield dict(**meta,card_id=cid,card=cards['cards'][cid],rating=rating,run=name)


def evaluate():
    # The final audit exports the reconciled goal subset so a public checkout
    # can reproduce this report without the operator's private campaign folder.
    bundled=OUT/'goal-accounting.json'
    ledger=read(bundled if bundled.exists() else ROOT.parent/'campaigns/speakermem-dev/campaign-dispatch.json')
    jobs={v:j for v,j in ledger['jobs'].items() if v.startswith('cup-practical-')}
    terminal={'COMPLETED','FAILED','TIMEOUT','OUT_OF_MEMORY','CANCELLED'}
    assert all(j['state'] in terminal for j in jobs.values()),'Reconcile all live jobs before final score'
    freeze=read(HERE/'final-runtime-freeze.json')
    assert all(sha256((ROOT/p).read_bytes()).hexdigest()==v for p,v in freeze['files_sha256'].items())
    data=read(HERE/'final-data-freeze.json')
    assert all(sha256((HERE/p).read_bytes()).hexdigest()==v for p,v in data['files_sha256'].items())
    legacy={}
    for name in LEGACY:
        for row in entries(name):
            assert row['operation']=='ask'
            key=(row['case_id'],row['arm'],row['label'])
            if key in legacy:
                assert legacy[key]['card']['status']=='not_executed','Never replace an observed failure with a retry'
            legacy[key]=row
    assert len(legacy)==40
    transfer=[r for name in TRANSFER for r in entries(name)]
    assert len(transfer)==80
    summary=dict(scope='Fixed practical CUPMem adaptation assessment; local Qwen3-8B; not original CUPMem/SpeakerMem performance',
        frozen_runtime=True,frozen_data=True,legacy={},transfer={},cost={},limitations=[
            'One AI evaluator, also involved in development; semantic ratings are not independent human validation.',
            '20 transfer histories are paired constructions from10 independent real Git follow-ups, with only2 prior sources per history.',
            'Some source commits explicitly name the earlier commit.',
            'Auxiliary end-of-options QA has date-versus-condition wording ambiguity; frozen key retained and not credited.',
            'Windows documentation update admits correction/reconsideration label-boundary uncertainty; frozen reconsideration gate retained.',
            'An interrupted import is an operational failure, not evidence of a correct abstention or preserved QA.',
            'First-attempt failures and incomplete physical captures remain in artifacts and allocated GPU cost.'])
    for arm in ('simple','cupmem'):
        rows=[r for r in legacy.values() if r['arm']==arm]
        by_corpus=defaultdict(lambda:dict(total=0,answer_correct=0,answer_and_citation=0))
        for r in rows:
            s=by_corpus[r['card']['expected']['corpus']];s['total']+=1
            s['answer_correct']+=r['rating']['answer_correct'] is True;s['answer_and_citation']+=success(r['rating'])
        summary['legacy'][arm]=dict(planned=20,answer_correct=sum(r['rating']['answer_correct'] is True for r in rows),
            answer_and_citation=sum(success(r['rating']) for r in rows),statuses=dict(Counter(r['card']['status'] for r in rows)),
            by_corpus=dict(by_corpus))
        reviews=[r for r in transfer if r['arm']==arm and r['operation']=='ingest']
        positive=[r for r in reviews if r['card']['expected']['positive']]
        negative=[r for r in reviews if not r['card']['expected']['positive']]
        qas=[r for r in transfer if r['arm']==arm and r['operation']=='ask']
        assert len(positive)==len(negative)==10 and len(qas)==20
        summary['transfer'][arm]=dict(positive_total=10,
            supported_reconsiderations=sum(r['rating']['supported_reconsideration'] is True for r in positive),
            correct_target_and_reconsider_kind=sum(any(p['kind']=='reconsider' and p['previous']['source_id']==r['card']['expected']['actual_target'] for p in r['card']['proposals']) for r in positive),
            positive_proposals_not_meeting_full_rubric=sum(len(r['card']['proposals'])-int(r['rating']['supported_reconsideration']) for r in positive),
            wrong_target_or_kind=sum(r['rating']['wrong_target_or_kind'] for r in positive),negative_total=10,
            unnecessary_negative_cases=sum(r['rating']['unnecessary_proposals']>0 for r in negative),
            unnecessary_negative_proposals=sum(r['rating']['unnecessary_proposals'] for r in negative),
            valid_negative_abstentions=sum(r['rating']['valid_abstention'] is True for r in negative),
            auxiliary_qa_answer_and_citation=sum(success(r['rating']) for r in qas),auxiliary_qa_total=20,
            auxiliary_qa_ambiguous=sum(bool(r['rating'].get('uncertainty')) for r in qas),
            review_statuses=dict(Counter(r['card']['status'] for r in reviews)))
    lost=[]; lost_content=[]
    for (case,arm,label),r in legacy.items():
        if arm=='simple' and success(r['rating']) and not success(legacy[(case,'cupmem',label)]['rating']):
            lost.append(r['card']['expected']['original_id'])
        if arm=='simple' and r['rating']['answer_correct'] and not legacy[(case,'cupmem',label)]['rating']['answer_correct']:
            lost_content.append(r['card']['expected']['original_id'])
    summary['legacy']['lost_simple_successes']=lost
    summary['legacy']['lost_content_correct_items']=lost_content
    cost={arm:defaultdict(lambda:dict(operations=0,calls=0,seconds=0,prompt_tokens=0,completion_tokens=0,calls_missing_usage=0)) for arm in ('simple','cupmem')}
    all_calls=[];qa=[];citation_total=citation_valid=unapproved=0
    for name in LEGACY+TRANSFER:
        folder=OUT/name;c=read(folder/'cards.json')
        calls=[json.loads(s) for s in gzip.decompress((folder/'calls.jsonl.gz').read_bytes()).splitlines()]
        all_calls.extend(calls)
        for op in c['operation_costs']:
            bucket=cost[op['arm']][op['operation']];bucket['operations']+=1
            for k in ('calls','seconds','prompt_tokens','completion_tokens','calls_missing_usage'):bucket[k]+=op[k]
            if op['operation']=='ask':qa.append(op)
        for row in entries(name):
            card=row['card'];sources=card['source_records']
            witnesses=[w for a in card['answers'] for w in a['evidence']]
            for prop in card['proposals']:
                unapproved+=prop['status']=='approved'
                witnesses += [prop['previous'],prop['incoming']]
                witnesses += [w for group in prop.get('support',{}).values() for w in group]
                witnesses += [w for group in prop.get('selected_evidence',{}).values() for w in group]
            citation_total+=len(witnesses);citation_valid+=sum(valid_witness(w,sources) for w in witnesses)
    for arm in cost:
        invoked=[q for q in qa if q['arm']==arm and q['calls']>0]
        blocked=[q for q in qa if q['arm']==arm and q['calls']==0]
        summary['cost'][arm]=dict(by_operation=dict(cost[arm]),qa_invoked=len(invoked),qa_blocked_zero_calls=len(blocked),
            mean_calls_per_invoked_qa=statistics.mean(q['calls'] for q in invoked),
            mean_seconds_per_invoked_qa=statistics.mean(q['seconds'] for q in invoked),
            median_seconds_per_invoked_qa=statistics.median(q['seconds'] for q in invoked))
    # Physical totals include unfinished native writes omitted from step snapshots.
    summary['cost']['recorded_physical_calls']=len(all_calls)
    summary['cost']['calls_without_usage']=sum(not c.get('response',{}).get('usage') for c in all_calls)
    summary['cost']['physical_calls_by_arm']=dict(Counter(c['context']['arm'] for c in all_calls))
    summary['cost']['recorded_physical_tokens']={k:sum(c.get('response',{}).get('usage',{}).get(k,0) or 0 for c in all_calls)
        for k in ('prompt_tokens','completion_tokens')}
    summary['cost']['token_accounting_note']='Recorded usage only; failed/timed-out calls without usage are unknown, not zero. GPU time includes every attempt, startup, development and CLI smoke.'
    summary['cost']['unfinished_operation_calls']=sum(read(OUT/name/'cards.json')['unfinished_operation_calls'] for name in LEGACY+TRANSFER)
    summary['cost']['all_goal_gpu_minutes']=sum(j['gpus']*j['elapsed_seconds']/60 for j in jobs.values())
    summary['cost']['goal_gpu_cap']=240
    assert summary['cost']['all_goal_gpu_minutes']<=240
    summary['evidence']=dict(returned_witness_instances=citation_total,valid_original_witness_instances=citation_valid,
                             unapproved_promotions_observed=unapproved)
    c=summary['transfer']['cupmem']
    summary['gates']=dict(development_qa_5=read(OUT/'dev-v2/ratings.json')['candidate']['cedar_qa_answer_and_citation']==5,
        legacy_no_lost_simple_successes=not lost,
        transfer_reconsider_8_of_10=c['supported_reconsiderations']>=8,
        transfer_no_unnecessary_proposals=c['unnecessary_negative_cases']==0 and c['valid_negative_abstentions']==10,
        exact_returned_citations=citation_total==citation_valid,no_unapproved_promotion=unapproved==0,
        call_reduction=summary['cost']['cupmem']['mean_calls_per_invoked_qa']<=4.5)
    summary['gates']['candidate_adoption']=all(summary['gates'].values())
    summary['gates']['cost_claim_requires_quality']='Invocation count alone is not an overall speed/quality success; report blocked QA and ingestion cost alongside quality.'
    write(OUT/'summary.json',summary)
    write(OUT/'scored-cases.json',dict(legacy=list(legacy.values()),transfer=transfer))
    return summary


if __name__=='__main__':print(json.dumps(evaluate(),ensure_ascii=False,indent=2))
