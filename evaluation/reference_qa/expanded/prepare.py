"""Prepare a reviewable, immutable GPU job; never authorize or submit it."""
from hashlib import sha256
import json,re,tarfile
from pathlib import Path
from team_memory.store import source_envelope,digest
from evaluation.cupmem.dispatch import validate_submission


def main():
    root=Path(__file__).resolve().parents[3];camp=root.parent/'campaigns/speakermem-dev'
    version='cup-ref-claims-v2';dest=camp/'source'/version
    output=root/'results/reference-qa'/version.removeprefix('cup-ref-')
    assert not output.exists(),'Prepared version already frozen'
    assert version not in json.loads((camp/'campaign-dispatch.json').read_text())['jobs']
    dest.mkdir(exist_ok=True)
    prior=camp/'source/cup-ref-simple-v2';old=root/'results/reference-qa/quote-normalized-v1'
    def read(p):return json.loads(p.read_text())
    originals=[e for c in read(root/'evaluation/cupmem/practical/legacy.json')['cases'] for ev in c['events'] for e in ev.get('records',[])]
    transfers=read(root/'evaluation/reference_qa/simplify/inputs.json')['cases']
    originals += [e for c in transfers for e in c['records']]
    env={digest(source_envelope(e)):source_envelope(e) for e in originals}
    cases=[]
    def add(split,cid,q,w):
        witnesses=[dict(s,observed_at=env[s['source_id']]['observed_at']) for s in w]
        cases.append(dict(split=split,id=cid,question=q,witnesses=witnesses))
    for cid,c in read(old/'cards.json').items():add('legacy',cid,c['result']['alce']['question'],c['result']['citation_sources'])
    previous=read(root/'results/reference-qa/simplify-v2/cards.json')
    for c in transfers:
        answer=previous['transfer/'+c['id']+'/joint']['result']
        add('transfer',c['id'],c['question'],answer['citation_sources'])
    assert len(cases)==32
    one=next(c for c in transfers if c['id']=='new-conflict-one-source')
    a,b=one['records'][0]['source']['text'].split('\n\nSynthetic appended test report:\n')
    blocks=['Verbatim manual excerpt:\n'+a.strip(),'Synthetic test report:\n'+b.strip()]
    order=[dict(id=name,question=one['question'],text='\n\n'.join(parts)) for name,parts in [('forward',blocks),('reversed',blocks[::-1])]]
    (dest/'regressions.json').write_text(json.dumps(dict(cases=cases,order=order),ensure_ascii=False,indent=2)+'\n')
    names=['team_memory/'+n for n in ['__init__.py','store.py','reference_qa.py','reference_prompts.py','reference_joint.py','reference_claims.py','reference_quotes.py','reference_fallback.py']]
    names += ['team_memory/_vendor/langchain_citation/'+n for n in ['__init__.py','quoted_answer.py','LICENSE']]
    names += ['team_memory/_vendor/attribute_first/'+n for n in ['prompts.json','LICENSE','NOTICE.md']]
    names += ['evaluation/reference_qa/expanded/run.py']
    with tarfile.open(dest/'code.tar.gz','w:gz') as tar:
        for n in names:tar.add(root/n,arcname=n)
    for n in ['serve.py','service.py','prepare_nltk.py']:(dest/n).write_bytes((prior/n).read_bytes())
    (dest/'service.py').write_text((dest/'service.py').read_text().replace('reference_qa/simplify/run.py','reference_qa/expanded/run.py'))
    (dest/'serve.py').write_text((dest/'serve.py').read_text().replace("'cup-reference-'","'cup-expanded-'"))
    for n in ['download.py','manifest.json']:(dest/n).write_bytes((camp/'source/cup-ref-eval-data-v1'/n).read_bytes())
    (dest/'PROTOCOL.md').write_bytes((root/'evaluation/reference_qa/expanded/PROTOCOL.md').read_bytes())
    base=read(prior/'config.json')
    cfg={k:base[k] for k in ['project','conda_prefix','model_path','model_shared','model_repo','model_revision','model_files_sha256','embedding','python_client','reference_extras']}
    excluded=sorted(set(re.findall(r'(?:F_SH|F_MH|F_TP|MA_[UP])_Top\d+_\d+',(camp/'source/scoped-five-v2/questions.json').read_text())))
    cfg.update(source_version=version,resources=dict(gpus=1,cpus=8,ram_gb=48,wall_minutes=45),
        client_seconds=2200,serve_seconds=2250,max_calls=220,expected_max_calls=172,expected_output_rows=104,
        profile='attribute-first-claims-vs-joint',excluded_ever_ids=excluded,
        ever_revision='a6b210a32248e841967b7b64a64281d2ff3f669d',wiki_revision='c20e361f985ed480a659b35d98b49f2311fcd174',
        code_sha256={n:sha256((root/n).read_bytes()).hexdigest() for n in names},
        data_sha256={n:sha256((dest/n).read_bytes()).hexdigest() for n in ['regressions.json','manifest.json','PROTOCOL.md']},
        scope='32 fixed-retrieval historical regressions, pure order pair,10 native Ever development QA,8 Wiki unique questions in3 supplied-context conditions. Not merge/full benchmark evaluation.',
        execution_changes=dict(model='Unchanged Qwen3-8B BF16/nonthinking/temperature0/output1024/context32768',
            reader='Attribute First selection then fusion with typed claim-evidence units; no iterative revision or document judge',
            retrieval='Native Ever: whole-topic BM25 top8,512/64; other inputs fixed. Identical witnesses between arms.',
            timestamp='Native unspecified timezone preserved as text; Wiki date unknown. No approval semantics inferred.'))
    (dest/'config.json').write_text(json.dumps(cfg,indent=2)+'\n')
    script=(prior/'run.sbatch').read_text().replace('cup-ref-simple-v2',version).replace('00:14:00','00:45:00')
    command='python -u '+cfg['project']+'/source/sm-'+version+'/download.py\n'
    script=script.replace('python -u '+cfg['project']+'/source/sm-'+version+'/serve.py',command+'python -u '+cfg['project']+'/source/sm-'+version+'/serve.py')
    validate_submission(script,1);assert '--time=00:45:00' in script
    (dest/'run.sbatch').write_text(script)
    files=['run.sbatch','config.json','serve.py','service.py','prepare_nltk.py','download.py','manifest.json','PROTOCOL.md','regressions.json','code.tar.gz']
    output.mkdir(exist_ok=False)
    freeze=dict(source_version=version,submission_status='prepared_not_submitted_budget_approval_required',
        files_sha256={n:sha256((dest/n).read_bytes()).hexdigest() for n in files},
        evaluation_sha256={n:sha256((root/n).read_bytes()).hexdigest() for n in ['evaluation/cupmem/practical/legacy-key.json','evaluation/reference_qa/simplify/key.json','evaluation/reference_qa/expanded/PROTOCOL.md']},
        prior_sha256={str(p.relative_to(root)):sha256(p.read_bytes()).hexdigest() for p in [old/'cards.json',old/'ratings.json',root/'results/reference-qa/simplify-v2/cards.json',root/'results/reference-qa/simplify-v2/ratings.json']},
        requested_resources=dict(gpus=1,wall_minutes=45,additional_budget_gpu_minutes=60,includes_failures=True),
        submit_command='python -m evaluation.cupmem.dispatch submit '+version+' 1 45 '+' '.join(files))
    (output/'freeze.json').write_text(json.dumps(freeze,indent=2)+'\n')
    for n in ['config.json','run.sbatch','PROTOCOL.md']:(output/n).write_bytes((dest/n).read_bytes())
    print(json.dumps(dict(version=version,cases=len(cases),rows=104,excluded_ever_ids=excluded,status=freeze['submission_status']),indent=2))


if __name__=='__main__':main()
