"""Freeze explicit files and prepare a job; submission is a separate command."""
import argparse,json,shutil,tarfile
from hashlib import sha256
from pathlib import Path
from datetime import datetime, timezone


def main(phase):
    root=Path(__file__).resolve().parents[2];camp=root.parent/'campaigns/speakermem-dev'
    version='cup-state-'+phase+'-v1';dest=camp/'source'/version
    dest.mkdir(exist_ok=False)
    prior=camp/'source/cup-service-v2-v6'
    cfg=json.loads((prior/'config.json').read_text())
    keep=['project','conda_prefix','model_path','model_shared','model_repo','model_revision','model_files_sha256',
          'embedding','python_client','reference_extras','execution_time_policy','resources','startup_seconds']
    cfg={k:cfg[k] for k in keep}
    cfg.update(source_version=version,client_seconds=42000,serve_seconds=42660,max_calls=8 if phase=='dev' else 600,
        scope='Known state citation repair' if phase=='dev' else 'Frozen direct-vs-attributed decision',
        phase=phase,ever_revision='a6b210a32248e841967b7b64a64281d2ff3f669d',
        wiki_revision='c20e361f985ed480a659b35d98b49f2311fcd174')
    for n in ['serve.py','prepare_nltk.py','nltk-data.tar.gz']:shutil.copyfile(prior/n,dest/n)
    (dest/'serve.py').write_text((dest/'serve.py').read_text().replace("'service-v2-'","'service-v3-'"))
    (dest/'service.py').write_text((prior/'service.py').read_text().replace('evaluation/service_v2_smoke.py','evaluation/service_v3/'+phase+'.py'))
    (dest/'run.sbatch').write_text((prior/'run.sbatch').read_text().replace('cup-service-v2-v6',version))
    (dest/'PROTOCOL.md').write_bytes((root/'evaluation/service_v3/PROTOCOL.md').read_bytes())
    data=['PROTOCOL.md']
    if phase=='dev':
        prior_result=json.loads((root/'results/service-v2/run-120359.json').read_text())
        sources=[];cases=[]
        for r in prior_result['rows']:
            req=r.get('request',{})
            if req.get('operation')=='import_history':sources+=req['records']
            if req.get('operation')=='ingest':sources.append(req['source'])
            if r['label'] in ('pending_qa','current_qa'):
                x=r['result'];cases.append(dict(label=r['label'],question=req['question'],raw=x['pre_citation_raw'],
                    witnesses=x['citation_sources'],context=x['review_context']))
        (dest/'dev.json').write_text(json.dumps(dict(sources=sources,cases=cases),ensure_ascii=False,indent=2))
        data.append('dev.json')
    else:
        shutil.copyfile(camp/'source/cup-state-dev-v1/dev.json',dest/'dev.json');data.append('dev.json')
        for n in ['streams.json','stream-keys.json','legacy.json','exclusions.json','dataset-manifest.json']:
            shutil.copyfile(root/'evaluation/service_v3'/n,dest/n);data.append(n)
    names=sorted(str(p.relative_to(root)) for p in (root/'team_memory').rglob('*')
                 if p.is_file() and '__pycache__' not in p.parts and (p.suffix in ('.py','.json','.md','.txt') or p.name=='LICENSE'))
    names+=['evaluation/service_v3/'+phase+'.py']
    if phase=='final':names+=['evaluation/service_v3/dev.py','evaluation/service_v3/verify.py','evaluation/service_v3/score.py']
    with tarfile.open(dest/'code.tar.gz','w:gz') as tar:
        for n in names:tar.add(root/n,arcname=n,recursive=False)
    cfg['code_sha256']={n:sha256((root/n).read_bytes()).hexdigest() for n in names}
    cfg['data_sha256']={n:sha256((dest/n).read_bytes()).hexdigest() for n in data}
    (dest/'config.json').write_text(json.dumps(cfg,indent=2))
    files=['run.sbatch','config.json','serve.py','service.py','prepare_nltk.py','nltk-data.tar.gz','code.tar.gz']+data
    freeze=dict(frozen_at=datetime.now(timezone.utc).isoformat(),version=version,
        files={n:sha256((dest/n).read_bytes()).hexdigest() for n in files},config=cfg,
        command='python -m evaluation.cupmem.dispatch submit '+version+' 1 720 '+' '.join(files))
    target=root/'results/service-v3'/('freeze-'+phase+'.json');assert not target.exists();target.write_text(json.dumps(freeze,indent=2))
    print(freeze['command'])


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['dev','final']);main(parser.parse_args().phase)
