"""Prepare source-review cards or aggregate explicit ratings with fixed criteria."""
from collections import defaultdict
from hashlib import sha256
import json
import sys

from .verify import OUT, ROOT, read


def write(name, value):
    (OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def prepare():
    result = read(OUT/'result.json')
    keys = read(ROOT/'results/reference-qa/claims-v3/keys.json')
    legacy = read(ROOT/'evaluation/cupmem/practical/legacy-key.json')['cases']
    cards = {}
    for row in result['rows']:
        if row['split']=='legacy':
            case, question = row['case_id'].rsplit('/',1)
            reference = legacy[case]['questions'][question]
        else:
            reference = keys['keys'][row['case_id']]
        identity = '/'.join(row[k] for k in ['split','case_id','arm'])
        cards[identity] = dict(**row,reference=reference)
    write('cards.json',cards)
    retrieval = []
    old = {row['id']:row for row in keys['retrieval']}
    for item in result['retrieval']:
        previous = old[item['id']]
        gold = set(previous['gold_reference_locations'])
        current = {w['location'] for w in item['sources']}
        before = set(previous['retrieved_locations'])
        retrieval.append(dict(id=item['id'],total_R=len(gold),
            before_R_retrieved=len(gold&before),after_R_retrieved=len(gold&current),
            retrieved_locations=sorted(current),recovered_R=sorted(gold&(current-before)),
            lost_R=sorted(gold&(before-current))))
    write('retrieval-metrics.json',retrieval)
    print(json.dumps(dict(cards=len(cards),old_R=sum(r['before_R_retrieved'] for r in retrieval),
        new_R=sum(r['after_R_retrieved'] for r in retrieval),total_R=sum(r['total_R'] for r in retrieval))))


def score():
    cards = read(OUT/'cards.json')
    reviews = read(OUT/'ratings.json')
    ratings = reviews['ratings']
    assert set(cards)==set(ratings) and reviews['reviewer']
    fields = ['answer_correct','returned_evidence_supports_all_claims',
              'required_evidence_complete','narrow_quotes_support_all_claims','unsupported_extra']
    groups = defaultdict(list)
    for identity, rating in ratings.items():
        assert all(isinstance(rating[field],bool) for field in fields)
        assert rating['reason'] and len(rating['claim_reviews'])==len(cards[identity]['result']['claims'])
        rating['success'] = (rating['answer_correct'] and rating['returned_evidence_supports_all_claims']
            and rating['required_evidence_complete'] and not rating['unsupported_extra'])
        row = cards[identity]
        groups[row['split']+'/'+row['arm']].append(identity)
    before = read(ROOT/'results/reference-qa/claims-v3/ratings-by-id.json')
    before.update(read(ROOT/'results/reference-qa/format-recovery-v1/reviewed-deltas.json'))
    original_joint_successes = [identity.split('/')[1] for identity,rating in before.items()
        if identity.startswith('ever/') and identity.endswith('/joint') and rating['success']]
    legacy_lost = [key for key,r in ratings.items() if key.startswith('legacy/') and not r['success']]
    ever_lost = [case for case in original_joint_successes if not ratings[f'ever/{case}/combined']['success']]
    summary = {group:dict(n=len(ids),**{field:sum(ratings[key][field] for key in ids)
               for field in fields+['success']}) for group,ids in groups.items()}
    prior = read(ROOT/'results/reference-qa/connected-v1/ratings-by-id.json')
    preserved = set(original_joint_successes) | {identity.split('/')[1]
        for identity, rating in prior.items() if identity.startswith('ever/')
        and identity.endswith('/combined') and rating['success']}
    current_joint = {identity.split('/')[1] for identity, rating in ratings.items()
        if identity.startswith('ever/') and identity.endswith('/direct') and rating['success']}
    ever_lost = sorted(case for case in preserved | current_joint
        if not ratings[f'ever/{case}/combined']['success'])
    contract_errors = [identity for identity, card in cards.items()
        if card['arm'] != 'direct' and (card['result']['status']=='error' or card['result'].get('warnings'))]
    criteria = dict(legacy20_preserved=not legacy_lost,
        ever_more_than_prior_best=summary['ever/combined']['success']>3,
        ever_prior_successes_preserved=not ever_lost,
        beats_fresh_direct=summary['ever/combined']['success']>summary['ever/direct']['success'],
        no_contract_errors=not contract_errors)
    report = dict(summary=summary,criteria=criteria,adopt_demonstrated=all(criteria.values()),
        legacy_losses_against_selected_attributed=legacy_lost,ever_losses_against_prior_joint=ever_lost,
        contract_errors=contract_errors,reviewer=reviews['reviewer'],independent_human=reviews['independent_human'],
        verification=read(OUT/'verification.json'),
        limitations='Exposed development; legacy inputs fixed; implementing AI review; no full benchmark or merge evaluation.',
        evidence_hashes={name:sha256((OUT/name).read_bytes()).hexdigest()
            for name in ['result.json','calls.jsonl','ratings.json','cards.json']})
    write('ratings-by-id.json',ratings)
    write('summary.json',report)
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__=='__main__':
    {'prepare':prepare,'score':score}[sys.argv[1]]()
