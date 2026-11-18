"""Whole-source content, typed edges, extra rows, overmerging and provenance.
No model judge; deterministic source-anchor diagnostics, not unrestricted entailment.
"""
from collections import Counter,defaultdict
from itertools import combinations
from pathlib import Path
from hashlib import sha256
import json,re
from evaluation.record_full.gold import anchors

INLINE={'caveat','method','recipient'}
JUNK=re.compile(r'\b(?:good morning everyone|hello everyone|good morning|email received|received|thanks a lot|great plan|good question|okay|understood)\b',re.I)

def matches(text,node):
    # Ordered material-token subsequence permits articles/prepositions and span
    # boundaries but preserves predicate, target, negation, modality and numbers.
    it=iter(anchors(text))
    return all(any(t==a for t in it) for a in node['anchors'])

def contributors(rows,node):
    whole=[r for r in rows if matches(r['text'],node)]
    if whole:return {r['id'] for r in whole}
    eligible=[r for r in rows if anchors(r['text']) and not (Counter(anchors(r['text']))-Counter(node['anchors']))]
    seq=[(t,r['id']) for r in eligible for t in anchors(r['text'])];at=0;ids=set()
    for token in node['anchors']:
        while at<len(seq) and seq[at][0]!=token:at+=1
        if at==len(seq):return set()
        ids.add(seq[at][1]);at+=1
    return ids

def raw_rows(raw):
    try:
        rows=[]
        for i,row in enumerate(json.loads(raw)['extractions']):
            role=next(r for r in ('claim','condition','basis','time','subject') if r in row)
            a=row[role+'_attributes'];rows.append(dict(id=i,role=role,text=row[role],group=a['claim_group'],stance=a['stance'],basis_kind=a.get('basis_kind','unspecified')))
        return rows
    except (ValueError,KeyError,StopIteration,TypeError):return []

def compiled_rows(source):
    from evaluation.record_groups.evaluate import linked_text
    out=[]
    for c in source['record_graph']['claims']:
        for role in ('claim','condition','basis','time','subject'):
            for text in linked_text(source,c,role):out.append(dict(id=len(out),role=role,text=text,group=c['id'],stance=c['stance'] if role=='claim' else 'unknown'))
    return out

def metric(tp,fp,fn):
    return dict(tp=tp,fp=fp,fn=fn,precision=tp/(tp+fp) if tp+fp else None,recall=tp/(tp+fn) if tp+fn else None,f1=2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else None)

def score(rows,gold,source,compiled=False):
    nodes=gold['nodes'];required={n['id'] for n in nodes if n['required']};cores={n['id'] for n in nodes if n['role']=='claim'}
    byid={n['id']:n for n in nodes};groups=defaultdict(list)
    for row in rows:groups[row['group']].append(row)
    covered=set();claimed=set();edges=set();extra=[];extra_claim_rows=[];pollution=[];wrong_types=[];unbound=[];merge_pairs=set();stances={};basis_labels=[];duplicate=0;seen=Counter();row_annotations=[];valid_fragments=set()
    for row in rows:
        match=[n for n in nodes if matches(row['text'],n)]
        covered.update(n['id'] for n in match)
        ident=(row['group'],row['role'],row['text']);seen[ident]+=1
        if seen[ident]>1:duplicate+=1
        if not match:extra.append(dict(row=row['id'],role=row['role'],text=row['text'],reason='No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity'))
        if JUNK.search(row['text']):pollution.append(row['id'])
        row_annotations.append(dict(row=row['id'],matches=[n['id'] for n in match]))
        if row['role']=='claim':
            if not any(n['role'] in ('claim','basis','caveat','method') for n in match):extra_claim_rows.append(row['id'])
            for n in match:
                if n['role']=='claim':claimed.add(n['id'])
                if n['role'] in ('claim','caveat'):stances.setdefault(n['id'],[]).append(row['stance'])
    for gid,rr in groups.items():
        claimtexts=[r['text'] for r in rr if r['role']=='claim'];joined=' '.join(claimtexts)
        for n in nodes:
            if n['role'] not in ('claim','basis','caveat','method'):continue
            ids=contributors([r for r in rr if r['role']=='claim'],n)
            if ids:
                valid_fragments.update(ids)
                valid_fragments.update(r['id'] for r in rr if r['role']=='claim' and not anchors(r['text']) and r['text'].strip() and r['text'].casefold() in n['text'].casefold())
                if n['role'] in ('claim','caveat') and n['id'] not in stances:
                    stances[n['id']]=[r['stance'] for r in rr if r['id'] in ids]
        target_nodes=[n for n in nodes if n['role']=='claim' and matches(joined,n)]
        targets={n['record_id'] for n in target_nodes}
        claimed.update(n['id'] for n in target_nodes);covered.update(n['id'] for n in nodes if matches(joined,n))
        merge_pairs.update(tuple(sorted(p)) for p in combinations(targets,2))
        for r in rr+[dict(role='claim',text=joined,id='joined:'+str(gid))]:
            if r['role']=='claim':
                # Inline method/caveat/recipient is legal, but must be linked to
                # a source-grounded target, not just present in another group.
                candidates=[n for n in nodes if n['role'] in INLINE and matches(r['text'],n)]
            else:candidates=[n for n in nodes if matches(r['text'],n)]
            if r['role']=='claim' and not candidates:continue
            if not candidates:
                if r['role']!='claim':edges.add(('unbound:'+gid,r['role'],'unmatched:'+str(r['id'])))
                continue
            for target in targets or {'unbound:'+gid}:
                owned=[n for n in candidates if n['record_id']==target]
                use=owned or candidates
                if r['role']!='claim':
                    typed=[n for n in use if n['role']==r['role'] or (r['role']=='subject' and n['role']=='recipient')]
                    if typed:use=typed
                # One quoted semantic value is one prediction even when gold
                # reuses that value under several different records.
                use=list({tuple(n['anchors']):n for n in reversed(use)}.values())
                for n in use:
                    role=n['role'] if r['role']=='claim' or (r['role']=='subject' and n['role']=='recipient') else r['role']
                    # Core assertions quoted as subject/basis may be legitimate
                    # only if a corresponding gold subject/basis exists.
                    edge=(target,role,n['id']);edges.add(edge)
                    if r['role']=='basis':basis_labels.append(dict(edge=edge,kind=r.get('basis_kind','unspecified'),expected='inferred' if not n['required'] else 'stated'))
                    if role!=n['role']:wrong_types.append(dict(row=r['id'],target=target,predicted=role,gold=n['role'],node=n['id']))
    extra=[e for e in extra if e['row'] not in valid_fragments]
    extra_claim_rows=[r for r in extra_claim_rows if r not in valid_fragments]
    expected={tuple(e) for e in gold['edges']};optional={tuple(e) for e in gold['optional_edges']}
    # Repeated exact output rows are reported separately; distinct original
    # mentions can legitimately produce repeated factual assertions.
    tp=len(edges&expected);fp=len(edges-expected-optional);fn=len(expected-edges)
    bad_stances=[];stance_ok=0;stance_missing=0
    for n in nodes:
        if n['role'] not in ('claim','caveat'):continue
        values=stances.get(n['id'],[])
        if not values:stance_missing+=1
        elif any(v not in n['stances'] for v in values):bad_stances.append(dict(node=n['id'],expected=n['stances'],predicted=values))
        else:stance_ok+=1
    strict_spans=[r['text'] in source['text'] for r in rows]
    node_missing=sorted(required-covered);claim_missing=sorted(cores-claimed)
    result=dict(content_recall=metric(len(required&covered),0,len(node_missing)),claim_recall=metric(len(cores&claimed),len(extra_claim_rows),len(claim_missing)),
        typed_edges=metric(tp,fp,fn),extra_claim_rows=extra_claim_rows,extra_rows=extra,extra_row_rate=len(extra)/len(rows) if rows else None,boilerplate_rows=pollution,duplicate_rows=duplicate,
        overmerged_record_pairs=sorted(merge_pairs),wrong_role_assignments=wrong_types,missing_nodes=node_missing,missing_claims=claim_missing,
        missing_edges=sorted(expected-edges),incorrect_edges=sorted(edges-expected-optional),stance_correct=stance_ok,stance_wrong=bad_stances,stance_missing=stance_missing,
        raw_verbatim_rows=sum(strict_spans),rows=len(rows),row_matches=row_annotations,basis_labels=basis_labels,
        complete=not(node_missing or fn or fp or extra or extra_claim_rows or pollution or duplicate or merge_pairs or bad_stances or stance_missing))
    result['semantic_complete']=result['complete']
    result['complete']=result['complete'] and all(strict_spans)
    # A failed empty graph must never gain precision=1 or a full-document pass.
    if not rows:result['complete']=False
    return result

def main():
    base=Path('evaluation/record_full');out=Path('results/record-full/v3');freeze=json.loads((out/'freeze.json').read_text())
    for name,h in freeze['files'].items():assert sha256(Path(name).read_bytes()).hexdigest()==h,name
    old=Path('results/record-strata/v1');result=json.loads((old/'record-strata-122970.json').read_text())
    assert result['status']=='complete' and result['calls']==136
    inputs={x['id']:x for x in json.loads(Path('evaluation/record_strata/inputs.json').read_text())['items']};gold={d['id']:d for d in json.loads((base/'gold.json').read_text())['documents']}
    cases=[]
    for row in result['rows']:
        item=inputs[row['id']];d=gold[row['id']];source=row['source']
        assert {k:v for k,v in source.items() if k!='record_graph'}==item['source']
        assert sha256(source['text'].encode()).hexdigest()==d['source_sha256']
        metadata={k:source[k] for k in d['source']}==d['source']
        c=dict(id=row['id'],arm=row['arm'],panel=d['panel'],difficulty=d['difficulty'],availability=d['availability'],raw=score(raw_rows(row['raw']),d,source),compiled=score(compiled_rows(source),d,source,True),source_metadata_exact=metadata,source_fingerprint=source['record_graph']['source_fingerprint'],all_claims_unverified=all(x['qualification']=='model_extracted_unverified' for x in source['record_graph']['claims']),compile_error=row['compile_error'],transport=row['transport'])
        cases.append(c)
    summary=[]
    for panel in ('balanced_synthetic','natural_audit'):
        for arm in ('simple','ours'):
            for stage in ('raw','compiled'):
                for diff,av in [('all','all')]+([(d,a) for d in ('easy','medium','hard') for a in ('full','partial','none')] if panel=='balanced_synthetic' else []):
                    cc=[c[stage] for c in cases if c['panel']==panel and c['arm']==arm and (diff=='all' or(c['difficulty']==diff and c['availability']==av))]
                    metrics={k:metric(*(sum(c[k][z] for c in cc) for z in ('tp','fp','fn'))) for k in ('content_recall','claim_recall','typed_edges')}
                    macro={k:sum(c[k]['recall'] for c in cc if c[k]['recall'] is not None)/sum(c[k]['recall'] is not None for c in cc) if any(c[k]['recall'] is not None for c in cc) else None for k in metrics}
                    summary.append(dict(panel=panel,arm=arm,stage=stage,difficulty=diff,availability=av,n=len(cc),metrics=metrics,macro_recall=macro,complete=sum(c['complete'] for c in cc),extra_rows=sum(len(c['extra_rows']) for c in cc),rows=sum(c['rows'] for c in cc),extra_claim_rows=sum(len(c['extra_claim_rows']) for c in cc),boilerplate_rows=sum(len(c['boilerplate_rows']) for c in cc),overmerged_pairs=sum(len(c['overmerged_record_pairs']) for c in cc),duplicate_rows=sum(c['duplicate_rows'] for c in cc),stance_correct=sum(c['stance_correct'] for c in cc),stance_wrong=sum(len(c['stance_wrong']) for c in cc),stance_missing=sum(c['stance_missing'] for c in cc)))
    report=dict(scope='Whole-source inventory under explicit annotation policy; retrospective same136 real Qwen outputs, not held-out evaluation or new inference.',job_id='122970',fresh_model_calls=0,cached_model_calls=136,cases=cases,summary=summary)
    (out/'evaluation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    for r in summary:
        if r['difficulty']=='all':print(json.dumps(r))
if __name__=='__main__':main()
