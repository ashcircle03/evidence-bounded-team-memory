"""Meaningful mutation tests: omission, extra assertion, bad edge, modality, provenance."""
import copy,json
from pathlib import Path
from evaluation.record_full.evaluate import score,raw_rows

def oracle(doc):
    rows=[]
    for n in doc['nodes']:
        if not n['required']:continue
        role='claim' if n['role'] in ('caveat','method') else 'subject' if n['role']=='recipient' else n['role']
        rows.append(dict(id=len(rows),role=role,text=n['spans'][0]['quote'],group=n['record_id'],stance=n.get('stances',['unknown'])[0],basis_kind='stated'))
    return rows

def main():
    docs=json.loads(Path('evaluation/record_full/gold.json').read_text())['documents'];inp={x['id']:x['source'] for x in json.loads(Path('evaluation/record_strata/inputs.json').read_text())['items']}
    errors=[]
    for d in docs:
        r=score(oracle(d),d,inp[d['id']])
        if not r['complete']:errors.append((d['id'],{k:r[k] for k in ('missing_nodes','missing_claims','missing_edges','incorrect_edges','extra_rows','extra_claim_rows','stance_wrong','stance_missing','overmerged_record_pairs')}))
    assert not errors,json.dumps(errors,indent=2)
    d=docs[0];s=inp[d['id']];base=oracle(d);assert score(base,d,s)['complete']
    dropped=base[:-1];assert score(dropped,d,s)['typed_edges']['fn']>0
    # Whole-sentence copy preserves content but fails structured linkage.
    flat=[dict(id=0,role='claim',text=s['text'],group='x',stance='decision')]
    r=score(flat,d,s);assert r['content_recall']['fn']==0 and r['typed_edges']['fn']>0
    extra=copy.deepcopy(base)+[dict(id=99,role='claim',text='The moon is green.',group='alien',stance='observation')]
    r=score(extra,d,s);assert r['extra_claim_rows'] and r['claim_recall']['fp']>0 and r['raw_verbatim_rows']<r['rows']
    swap=copy.deepcopy(base);swap[1]['role']='basis';swap[2]['role']='condition'
    r=score(swap,d,s);assert r['typed_edges']['fp'] and r['typed_edges']['fn'] and r['content_recall']['fn']==0
    # Wrong target with valid source quotation must be false positive + false negative.
    d=next(x for x in docs if x['id']=='h01-full');base=oracle(d);s=inp[d['id']]
    bad=copy.deepcopy(base);next(r for r in bad if r['group']=='r1' and r['role']=='condition')['group']='r6'
    r=score(bad,d,s);assert r['typed_edges']['fp'] and r['typed_edges']['fn']
    merged=copy.deepcopy(base)
    for r in merged:r['group']='one'
    assert score(merged,d,s)['overmerged_record_pairs']
    # Preserve differing per-claim stances instead of collapsing to group unknown.
    d=next(x for x in docs if x['id']=='e04-full');base=oracle(d);s=inp[d['id']]
    assert score(base,d,s)['complete']
    mixed=copy.deepcopy(base)
    for r in mixed:
        if r['role']=='claim':r['stance']='unknown'
    assert score(mixed,d,s)['stance_wrong']
    # Exact subspans split into multiple same-group rows are equivalent.
    for d in docs:
        base=oracle(d);split=[]
        for r in base:
            if r['role']=='claim' and ' ' in r['text']:
                cut=r['text'].find(' ',len(r['text'])//2)
                if cut>0:
                    for text in (r['text'][:cut],r['text'][cut+1:]):split.append(dict(r,id=len(split),text=text))
                    continue
            split.append(dict(r,id=len(split)))
        assert score(split,d,inp[d['id']])['complete'],('split invariance',d['id'])
    # A method mislabeled condition fails despite every word being present.
    d=next(x for x in docs if x['id']=='n13');base=oracle(d);s=inp[d['id']];bad=copy.deepcopy(base)
    next(r for r in bad if 'every 10 seconds' in r['text'])['role']='condition'
    r=score(bad,d,s);assert r['typed_edges']['fp'] and r['typed_edges']['fn']
    # One wrong quote/target is one FP even if gold reuses the quote twice.
    base=oracle(d);bad=base+[dict(id=999,role='condition',text="our message push service isn't fully ready yet",group='r1',stance='unknown')]
    assert score(bad,d,s)['typed_edges']['fp']==1
    # Missing negation/modal/numbers cannot match the original material anchors.
    d=next(x for x in docs if x['id']=='e03-full');bad=oracle(d);bad[0]['text']=bad[0]['text'].replace('not ','')
    assert score(bad,d,inp[d['id']])['claim_recall']['fn']>0
    # Trivial preposition variation does not erase the event time.
    d=next(x for x in docs if x['id']=='e02-full');bad=oracle(d)
    for r in bad:r['text']=r['text'].replace('on Thursday','Thursday')
    assert score(bad,d,inp[d['id']])['complete']
    print('68 complete gold-oracle checks +68 split-span invariance and11 failure-mode/surface mutation checks passed')
if __name__=='__main__':main()
