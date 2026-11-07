"""Freeze one bounded comparison; do not modify any budget or previous run."""
from pathlib import Path
from hashlib import sha256
import json,tarfile
from team_memory.store import source_envelope,digest
from evaluation.cupmem.dispatch import validate_submission


def main():
    repo=Path(__file__).resolve().parents[3];camp=repo.parent/'campaigns/speakermem-dev'
    version='cup-ref-simple-v1';ledger=json.loads((camp/'campaign-dispatch.json').read_text())
    assert version not in ledger['jobs']
    prior=camp/'source/cup-ref-quote-v2';dest=camp/'source'/version;dest.mkdir(exist_ok=False)
    cfg=json.loads((prior/'config.json').read_text())
    names=list(cfg['code_sha256'])+['team_memory/reference_fallback.py','team_memory/reference_joint.py','team_memory/_vendor/langchain_citation/quoted_answer.py','evaluation/reference_qa/simplify/run.py']
    with tarfile.open(dest/'code.tar.gz','w:gz') as tar:
        for n in names:tar.add(repo/n,arcname=n)
    for n in ['serve.py','service.py','prepare_nltk.py']:(dest/n).write_bytes((prior/n).read_bytes())
    (dest/'service.py').write_text((dest/'service.py').read_text().replace('reference_qa/quote_replay.py','reference_qa/simplify/run.py'))
    old=json.loads((repo/'results/reference-qa/quote-normalized-v1/cards.json').read_text())
    data=json.loads((repo/'evaluation/cupmem/practical/legacy.json').read_text())
    env={digest(source_envelope(e)):source_envelope(e) for c in data['cases'] for event in c['events'] for e in event.get('records',[])}
    cases=[]
    for cid,c in old.items():
        w=c['result']['citation_sources']
        context='\n\n'.join(f"Source {i}:\nrecord_author: {s['speaker']}\nrecorded_at: {env[s['source_id']]['observed_at']}\n\n{s['quote']}" for i,s in enumerate(w,1))
        cases.append(dict(id=cid,question=c['result']['alce']['question'],context=context,witnesses=w))
    assert len(cases)==20
    (dest/'legacy-contexts.json').write_text(json.dumps(dict(cases=cases),ensure_ascii=False,indent=2)+'\n')
    (dest/'transfer-inputs.json').write_bytes((repo/'evaluation/reference_qa/simplify/inputs.json').read_bytes())
    cfg.update(source_version=version,client_seconds=600,serve_seconds=650,max_calls=180,profile='joint-comparison',
        data_sha256={n:sha256((dest/n).read_bytes()).hexdigest() for n in ['legacy-contexts.json','transfer-inputs.json']},
        code_sha256={n:sha256((repo/n).read_bytes()).hexdigest() for n in names})
    cfg['resources']['wall_minutes']=17
    cfg['scope']='Legacy20 fixed-context fresh joint generation; new12 paired full-history attributed vs joint; no gold in server input.'
    cfg['execution_changes']['joint']='AQA source-specific answer intent and LangChain QuotedAnswer schema in one upstream compact query; no document judge, draft revision or posthoc attribution.'
    (dest/'config.json').write_text(json.dumps(cfg,indent=2)+'\n')
    script=(prior/'run.sbatch').read_text().replace('cup-ref-quote-v2',version).replace('00:20:00','00:17:00')
    script='\n'.join(line for line in script.splitlines() if '-m pip install' not in line)+'\n'
    validate_submission(script,1);(dest/'run.sbatch').write_text(script)
    files=['run.sbatch','config.json','serve.py','service.py','prepare_nltk.py','code.tar.gz','legacy-contexts.json','transfer-inputs.json']
    out=repo/'results/reference-qa/simplify-v1';out.mkdir(exist_ok=True)
    freeze=dict(source_version=version,files_sha256={n:sha256((dest/n).read_bytes()).hexdigest() for n in files},
        evaluation_sha256={n:sha256((repo/n).read_bytes()).hexdigest() for n in ['evaluation/cupmem/practical/legacy.json','evaluation/cupmem/practical/legacy-key.json','evaluation/reference_qa/simplify/inputs.json','evaluation/reference_qa/simplify/key.json','evaluation/reference_qa/simplify/PROTOCOL.md']},
        previous_sha256={n:sha256((repo/'results/reference-qa/quote-normalized-v1'/n).read_bytes()).hexdigest() for n in ['cards.json','ratings.json']},
        budget=dict(gpus=1,wall_minutes=17,phase_cap=90,cup_cap=460,campaign_cap=760),
        submit_command='python3 -m evaluation.cupmem.dispatch submit '+version+' 1 17 '+' '.join(files))
    (out/'freeze.json').write_text(json.dumps(freeze,indent=2)+'\n')
    for n in ['config.json','run.sbatch']:(out/n).write_bytes((dest/n).read_bytes())
    print(freeze['submit_command'])


if __name__=='__main__':main()
