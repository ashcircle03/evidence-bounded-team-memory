"""Pre-output scorer checks and gold minimal-span compiler/storage diagnosis."""
import json,tempfile
from pathlib import Path
from evaluation.record_strata.score import check,raw_groups,oracle_raw,compiled_groups
from evaluation.record_strata.arms import compile_source,prompt
from evaluation.record_groups.evaluate import transport

def main():
    base=Path('evaluation/record_strata');items=json.loads((base/'inputs.json').read_text())['items'];keys=json.loads((base/'keys.json').read_text())['items']
    rows=[]
    with tempfile.TemporaryDirectory(prefix='strata-oracle-') as td:
        for i,(item,key) in enumerate(zip(items,keys)):
            assert item['id']==key['id']
            raw=oracle_raw(key);assert check(raw_groups(raw),key)['passed'],key['id']
            source,error=compile_source(item['source'],raw,'gold-minimal-spans-not-a-model')
            row=dict(id=key['id'],compile_error=error,compiled=check(compiled_groups(source),key),transport=transport(source,Path(td)/str(i)))
            rows.append(row)
            for arm in item['arms']:assert item['source']['text'] in prompt(item['source'],arm)
    key=keys[0];groups=raw_groups(oracle_raw(key));assert check(groups,key)['passed']
    # Correct text but wrong role must fail typed score, not content recovery.
    groups[0]['condition'],groups[0]['basis']=groups[0]['basis'],groups[0]['condition']
    r=check(groups,key);assert r['visible_recovered'] and not r['typed_complete']
    # Missing information is allowed; inventing the withheld reason is not.
    partial=keys[1];g=raw_groups(oracle_raw(partial));assert check(g,partial)['passed']
    missing=next(s for s in partial['slots'] if not s['available']);g[0][missing['role']].append(missing['text'])
    assert check(g,partial)['unsupported_completion'] and not check(g,partial)['passed']
    # A correct target and a second wrong target group cannot conceal a false link.
    hard=next(k for k in keys if k['id']=='h01-full');g=raw_groups(oracle_raw(hard));bad=json.loads(json.dumps(g[0]));bad['condition'].append('below 1 bar')
    assert not check(g+[bad],hard)['passed']
    out=Path('results/record-strata/v1');out.mkdir(parents=True,exist_ok=True)
    (out/'preflight.json').write_text(json.dumps(dict(status='passed',oracle_minimal_spans=rows,note='Repeated short quotes may fail; this is not proof that no unique longer quote works.'),ensure_ascii=False,indent=2)+'\n')
    print('preflight passed; oracle compiler failures:',[(r['id'],r['compile_error']) for r in rows if r['compile_error']])
if __name__=='__main__':main()
