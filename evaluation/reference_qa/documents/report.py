"""Frozen criterion aggregation; each rating requires output hash and reasons."""
from collections import defaultdict
from hashlib import sha256
import json
import sys
from .verify import ROOT,OUT,read


def write(name,obj): (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')


def prepare():
    result=read(OUT/'result.json')
    keys=read(ROOT/'results/reference-qa/claims-v3/keys.json')
    legacy=read(ROOT/'evaluation/cupmem/practical/legacy-key.json')['cases']
    cards={}
    for row in result['rows']:
        if row['split']=='legacy':
            cid,qid=row['case_id'].rsplit('/',1); reference=legacy[cid]['questions'][qid]
        else: reference=keys['keys'][row['case_id']]
        identity='/'.join(row[k] for k in ['split','case_id','arm'])
        cards[identity]=dict(**row,reference=reference,
            output_sha256=sha256(json.dumps(row['result'],ensure_ascii=False,sort_keys=True).encode()).hexdigest())
    write('cards.json',cards)
    retrieval=[]
    golds={r['id']:r for r in keys['retrieval']}
    for r in result['retrieval']:
        gold=set(golds[r['id']]['gold_reference_locations'])
        old={w['location'] for w in r['initial_sources']}; new={w['location'] for w in r['sources']}
        retrieval.append(dict(id=r['id'],total_R=len(gold),bm25_R=len(gold&old),dense_R=len(gold&new),
            recovered_R=sorted(gold&(new-old)),lost_R=sorted(gold&(old-new))))
    write('retrieval-metrics.json',retrieval)
    print(json.dumps(dict(cards=len(cards),bm25_R=sum(r['bm25_R'] for r in retrieval),dense_R=sum(r['dense_R'] for r in retrieval))))


def score():
    cards=read(OUT/'cards.json'); reviews=read(OUT/'ratings.json'); ratings=reviews['ratings']
    assert set(cards)==set(ratings) and reviews['reviewer']
    ef=read(OUT/'evaluation-freeze.json')
    for name,expected in ef.items(): assert sha256((ROOT/name).read_bytes()).hexdigest()==expected,name
    fields=['answer_correct','returned_evidence_supports_all_claims','required_evidence_complete','all_citations_relevant','unsupported_extra']
    groups=defaultdict(list)
    for identity,r in ratings.items():
        card=cards[identity]
        assert all(isinstance(r[f],bool) for f in fields)
        assert r['reason'] and len(r['claim_reviews'])==len(card['result']['claims'])
        assert r['reviewed_output_sha256']==card['output_sha256']
        assert isinstance(r['input_evidence_sufficient'],bool)
        r['success']=all(r[f] for f in fields[:-1]) and not r['unsupported_extra'] and card['result']['status']=='ok'
        groups[card['split']+'/'+card['arm']].append(identity)
    summary={g:dict(n=len(ids),**{f:sum(ratings[i][f] for i in ids) for f in fields+['success']}) for g,ids in groups.items()}
    prior=read(ROOT/'results/reference-qa/connected-v1/ratings-by-id.json')
    preserved={i.split('/')[1] for i,r in prior.items() if i.startswith('ever/') and i.endswith('/combined') and r['success']}
    criteria={}
    for reading in ['direct','con']:
        legacy_lost=[i for i in groups['legacy/'+reading] if not ratings[i]['success']]
        ever_lost=[c for c in preserved if not ratings['ever/'+c+'/dense_'+reading]['success']]
        relevant=[i for g,ids in groups.items() if g in ['legacy/'+reading,'ever/dense_'+reading] for i in ids]
        criteria[reading]=dict(legacy20_preserved=not legacy_lost,prior_ever_preserved=not ever_lost,
            ever_more_than_prior_best=summary['ever/dense_'+reading]['success']>3,
            dense_beats_same_reader_bm25=summary['ever/dense_'+reading]['success']>summary['ever/bm25_'+reading]['success'],
            no_contract_errors=all(cards[i]['result']['status'] in ['ok','insufficient'] for i in relevant),
            legacy_losses=legacy_lost,ever_losses=ever_lost)
    eligible=[r for r,c in criteria.items() if all(c[k] for k in ['legacy20_preserved','prior_ever_preserved','ever_more_than_prior_best','dense_beats_same_reader_bm25','no_contract_errors'])]
    selected=max(eligible,key=lambda r:(summary['ever/dense_'+r]['success'],r=='direct')) if eligible else None
    result=dict(summary=summary,criteria=criteria,adopt_documents=bool(selected),selected_reading=selected,
        verification=read(OUT/'verification.json'),reviewer=reviews['reviewer'],independent_human=reviews['independent_human'],
        limitations='Exposed development, fixed legacy sources, implementing AI source review; not generalization, whole benchmark or merge evaluation.')
    write('ratings-by-id.json',ratings);write('summary.json',result);print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__': {'prepare':prepare,'score':score}[sys.argv[1]]()
