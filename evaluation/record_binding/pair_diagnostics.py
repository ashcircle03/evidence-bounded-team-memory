"""Read-only post-run diagnostics; never changes gold, predictions or acceptance."""
from copy import deepcopy
import json
from pathlib import Path
from evaluation.record_binding.pair_rows import compiled_rows
from evaluation.record_full.evaluate import score
from team_memory.records.graph import linked_span,describe


def main():
    out=Path('results/record-binding/v4')
    report=json.loads((out/'pair-evaluation.json').read_text())
    stored=json.loads((out/'pair-stored.json').read_text())
    gold={d['id']:d for d in json.loads(Path('evaluation/record_full/gold.json').read_text())['documents']}
    bases={c['id']:c['score'] for c in report['cases'] if c['arm']=='baseline'}
    diagnostics=[];transported=0
    for row in stored:
        if row['arm']!='pair_atomic':continue
        source=row['source'];g=source['record_graph'];base=bases[row['id']]
        for binding in g.get('context_bindings',[]):
            a,b=linked_span(source,binding['target_start'],binding['target_end'])
            ctx=describe(source,a,b)
            delivered=next(x for x in ctx['context_bindings'] if x['id']==binding['id'])
            assert delivered['target_quote']==source['text'][binding['target_start']:binding['target_end']]
            assert delivered['context_quote']==source['text'][binding['context_start']:binding['context_end']]
            assert delivered['qualification']=='model_extracted_unverified'
            transported+=1
            single=deepcopy(source);single['record_graph']['context_bindings']=[binding]
            s=score(compiled_rows(single),gold[row['id']],source)
            new_correct=set(map(tuple,base['missing_edges']))-set(map(tuple,s['missing_edges']))
            new_wrong=set(map(tuple,s['incorrect_edges']))-set(map(tuple,base['incorrect_edges']))
            diagnostics.append(dict(id=row['id'],binding=delivered,new_correct=sorted(new_correct),new_wrong=sorted(new_wrong),
                lost_complete=base['complete'] and not s['complete'],new_extra_rows=len(s['extra_rows'])-len(base['extra_rows'])))
    (out/'pair-edge-diagnostics.json').write_text(json.dumps(dict(all_new_bindings_delivered=transported,edges=diagnostics),ensure_ascii=False,indent=2)+'\n')
    lines=['# Case-by-case fixed-span binding results','',
        'Counts include all typed edges in the frozen scorer, not just condition/basis. '
        'Existing failures remain counted. This is records evaluation, not QA accuracy.','',
        '| Case | Baseline TP/FP | Atomic TP/FP | Group TP/FP | New correct links | Old complete lost |',
        '|---|---:|---:|---:|---|---|']
    for iid,base in bases.items():
        scores={c['arm']:c['score'] for c in report['cases'] if c['id']==iid}
        p=next(p for p in report['protection'] if p['id']==iid and p['arm']=='pair_atomic')
        fmt=lambda arm:str(scores[arm]['typed_edges']['tp'])+'/'+str(scores[arm]['typed_edges']['fp'])
        lines.append('| '+iid+' | '+' | '.join(fmt(a) for a in ('baseline','pair_atomic','pair_group'))+' | '+str(p['new_edges'])+' | '+str(p['lost_complete'])+' |')
    lines+=['','## Every newly persisted edge','', 'The two source quotes below are the actual selected endpoints. Marginal changes use the unchanged scorer with exactly one new edge; they do not override aggregate scoring.','']
    for x in diagnostics:
        b=x['binding'];lines += ['### '+x['id']+' / '+b['id'],'',
            '- Target: '+json.dumps(b['target_quote'],ensure_ascii=False),
            '- Context: '+json.dumps(b['context_quote'],ensure_ascii=False),
            '- Relation: `'+b['role']+'`',
            '- New correct: `'+str(x['new_correct'])+'`',
            '- New wrong: `'+str(x['new_wrong'])+'`','']
    (out/'cases.md').write_text('\n'.join(lines)+'\n')
    print('Explicit endpoint packets verified:',transported)


if __name__=='__main__':main()
