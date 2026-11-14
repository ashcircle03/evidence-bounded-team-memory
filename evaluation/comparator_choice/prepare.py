"""Build immutable explicit Slurm packets; submission uses the existing dispatcher."""
from datetime import datetime,timezone
from hashlib import sha256
import json,shutil,tarfile,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
HERE=ROOT/'evaluation/comparator_choice'


def write(path,obj):path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')


def oracle_inputs():
    old=json.loads((ROOT/'evaluation/service_completion/inputs.json').read_text());cases=[]
    for c in old['streams']:
        if c['id'] not in ('writer-reopen','cache-reopen'):continue
        plan=c['steps'][0]['question']
        c=dict(c,split='supplied_correct_relation',selector=dict(kind='reconsider',
            old_sentence_ids=[0,1] if c['id']=='writer-reopen' else [0],new_sentence_ids=[0,1],
            reason='The new report changes the stated constraint that justified the earlier decision; the earlier report remains true under its original conditions.'))
        c['steps']=[dict(label='pending-reason',operation='ask',question=plan),
            dict(label='pending-status',operation='ask',question='What is the review status of this proposal, and what remains established?'),
            dict(label='approve',operation='review_fixture',choice='approve'),
            dict(label='restart',operation='restart'),
            dict(label='approved-reason',operation='ask',question=plan),
            dict(label='approved-status',operation='ask',question='What did Mina approve, and what does that approval establish about the earlier decision and any further experiment?')]
        cases.append(c)
    return dict(cases=cases)


def prepare(label,mode,inputs,*,large=False,replays=None):
    version='cup-choice-'+label
    folder=ROOT.parent/'campaigns/speakermem-dev/source'/version;folder.mkdir(exist_ok=False)
    report=ROOT/'results/comparator-choice'/label;report.mkdir(parents=True,exist_ok=False)
    baseline=ROOT/'results/module-boundary/v1/runtime'
    cfg=json.loads((baseline/'config.json').read_text())
    cfg.update(source_version=version,mode=mode,served_model='Qwen3-8B',max_calls=800,
        expected_qa=sum(s['operation']=='ask' for c in inputs['cases'] for s in c.get('steps',[])),
        expected_comparisons=sum('incoming' in c for c in inputs['cases']),scope='Fixed comparator isolation; see PROTOCOL.md')
    if large:
        manifest=json.loads((HERE/'model14.json').read_text());cfg.update(manifest)
        cfg['resources']=dict(gpus=2,cpus=16,ram_gb=96,wall_minutes=720)
    for name in ('prepare_nltk.py','nltk-data.tar.gz'):shutil.copyfile(baseline/name,folder/name)
    serve=(baseline/'serve.py').read_text().replace('torch.cuda.device_count()==1',"torch.cuda.device_count()==cfg['resources']['gpus']")
    serve=serve.replace("ready['files_sha256']==cfg['model_files_sha256']", "all(cfg['model_files_sha256'].get(k)==v for k,v in ready.get('files_sha256',ready.get('weight_sha256',{})).items())")
    serve=serve.replace("'--served-model-name','Qwen3-8B'", "'--served-model-name',cfg['served_model']")
    serve=serve.replace("'--tensor-parallel-size','1'", "'--tensor-parallel-size',str(cfg['resources']['gpus'])")
    serve=serve.replace("'service-completion-'+record['job_id']", "'comparator-choice-'+record['job_id']")
    (folder/'serve.py').write_text(serve)
    service=(baseline/'service.py').read_text().replace('evaluation/service_completion/run.py','evaluation/comparator_choice/run.py')
    (folder/'service.py').write_text(service)
    script=(baseline/'run.sbatch').read_text().replace('cup-boundary-v1',version)
    if large:script=script.replace('--gres=gpu:1','--gres=gpu:2').replace('--cpus-per-task=8','--cpus-per-task=16').replace('--mem=48G','--mem=96G').replace('OMP_NUM_THREADS=8','OMP_NUM_THREADS=16')
    (folder/'run.sbatch').write_text(script)
    write(folder/'inputs.json',inputs);shutil.copyfile(HERE/'PROTOCOL.md',folder/'PROTOCOL.md')
    data=['inputs.json','PROTOCOL.md']
    if replays is not None:write(folder/'replays.json',replays);data.append('replays.json')
    names=sorted((set(cfg['code_sha256'])-{'evaluation/service_completion/run.py'})|{'evaluation/comparator_choice/run.py'})
    with tarfile.open(folder/'code.tar.gz','w:gz') as archive:
        for name in names:archive.add(ROOT/name,arcname=name)
    cfg['code_sha256']={n:sha256((ROOT/n).read_bytes()).hexdigest() for n in names}
    cfg['data_sha256']={n:sha256((folder/n).read_bytes()).hexdigest() for n in data}
    write(folder/'config.json',cfg);shutil.copytree(folder,report/'runtime')
    write(report/'freeze.json',dict(created_at=datetime.now(timezone.utc).isoformat(),config=cfg,
        files={p.name:sha256(p.read_bytes()).hexdigest() for p in folder.iterdir()}))
    print(version,' '.join(p.name for p in sorted(folder.iterdir())))


if __name__=='__main__':
    if sys.argv[1]=='oracle':prepare('oracle-v1','oracle',oracle_inputs())
    elif sys.argv[1] in ('8b','14b'):
        prepare('compare-'+sys.argv[1]+'-v1','compare',json.loads((HERE/'compare-inputs.json').read_text()),large=sys.argv[1]=='14b')
