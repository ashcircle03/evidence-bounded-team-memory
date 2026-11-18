"""Git transport orchestrator. Gold answers never enter this process."""
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import time


def main(packet):
    from team_memory.storage.sources import SourceStore
    cfg=json.loads((packet/'config.json').read_text())
    assert os.environ.get('SLURM_JOB_ID') and os.environ['CONDA_PREFIX']==cfg['conda_prefix']
    for name,h in cfg['code_sha256'].items(): assert sha256((packet/'code'/name).read_bytes()).hexdigest()==h, name
    for name,h in cfg['data_sha256'].items(): assert sha256((packet/name).read_bytes()).hexdigest()==h, name
    inputs=json.loads((packet/'inputs.json').read_text())
    job=os.environ['SLURM_JOB_ID']; root=Path(cfg['project'])/'results'/('git-local-'+job)
    root.mkdir(exist_ok=False); remote=root/'shared.git'; a=root/'A'; b=root/'B'
    result=dict(status='running', job_id=job, code_sha256=cfg['code_sha256'], data_sha256=cfg['data_sha256'],
                git=[], phases=[], mutations=[], sources={}, scope='records/index/QA only; no relationship inference or approvals')
    def save(): (root/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    def git(*args):
        p=subprocess.run(['git',*map(str,args)],text=True,capture_output=True)
        result['git'].append(dict(args=list(map(str,args)),stdout=p.stdout,stderr=p.stderr,exit_code=p.returncode));save()
        p.check_returncode()
        return p.stdout.strip()
    def commit(path, message):
        git('-C',path,'add','records');git('-C',path,'commit','-m',message);git('-C',path,'push','-u','origin','main')
    def configure(path):
        git('-C',path,'config','user.name','Local integration fixture')
        git('-C',path,'config','user.email','fixture@example.invalid')
    def phase(label,path,prepare=True,canary=0):
        env=dict(os.environ); env['PRACTICAL_MODEL_URL']=os.environ['MODEL_URL_'+path.name]
        output=root/(label+'.json')
        subprocess.run([sys.executable,'-u','-m','evaluation.git_local.worker',str(packet),str(path),label,str(output),str(int(prepare)),str(canary)],
                       env=env,check=True,timeout=cfg['phase_seconds'])
        x=json.loads(output.read_text());assert x['status']=='complete'
        result['phases'].append(dict(label=label,head=git('-C',path,'rev-parse','HEAD'),pid=x['pid'],
            calls=x['calls'],output=output.name));save()
    def add(path,revision):
        ids={}
        for case in inputs['cases']:
            store=SourceStore(path/'records'/case['id'])
            env=dict(owner='storage-probe',observed_at=f'2026-01-0{revision}T00:00:00Z',source=dict(
                speaker='storage-probe', location='synthetic://storage-probe/'+case['id'],
                text=f'Storage probe report dated 2026-01-0{revision}. The depot marker for the Zephyr spare telemetry unit is '+('violet.' if revision==1 else 'amber. This is revision 2 of the dated report; revision 1 remains in the history.')))
            ids[case['id']]=[store.capture_source(env)]
            if revision==2:
                extra=dict(owner='storage-probe',observed_at='2026-01-02T01:00:00Z',source=dict(speaker='storage-probe',
                    location='synthetic://storage-probe/spares/'+case['id'],text='The storage probe spare drawer contains seven blank labels.'))
                ids[case['id']].append(store.capture_source(extra))
        result['mutations'].append(dict(checkout=path.name,revision=revision,new_ids=ids));save()
    try:
        git('init','--bare',remote)
        git('--git-dir',remote,'symbolic-ref','HEAD','refs/heads/main')
        if cfg.get('seed_repository'):
            # Recover only the already committed source objects from a pre-QA
            # transport failure. Git clone never copies private index/receipts.
            git('clone','--no-hardlinks',cfg['seed_repository'],a)
            git('-C',a,'branch','-M','main')
            git('-C',a,'remote','set-url','origin',remote)
            configure(a)
            for case in inputs['cases']:
                assert SourceStore(a/'records'/case['id']).load('sources')==case['sources']
            assert not (a/'.git/team-memory-clients').exists()
            git('-C',a,'push','-u','origin','main')
        else:
            git('clone',remote,a); configure(a)
            # Git2.25 can create master when cloning an empty remote, even when
            # the bare remote's symbolic HEAD explicitly points to main.
            git('-C',a,'symbolic-ref','HEAD','refs/heads/main')
            for case in inputs['cases']:
                store=SourceStore(a/'records'/case['id'])
                for sid,env in case['sources'].items(): assert store.put('sources',env)==sid
            commit(a,'Import immutable historical sources')
        phase('a_initial',a)
        git('clone',remote,b);configure(b)
        assert not (b/'.git/team-memory-clients').exists(), 'Derived cache leaked through Git'
        phase('b_clone',b)
        add(b,1)
        # Prepare new records before any question. This phase has no QA.
        prepare_only(packet,b,root/'b_add_prepare.json')
        commit(b,'Append dated probe record')
        git('-C',a,'pull','--ff-only');phase('a_pull',a,canary=1)
        phase('a_restart',a,prepare=False,canary=1)
        add(a,2);prepare_only(packet,a,root/'a_change_prepare.json')
        commit(a,'Append revised record and new spare record')
        git('-C',b,'pull','--ff-only');phase('b_pull',b,canary=2)
        phase('b_restart',b,prepare=False,canary=2)
        # No-op refresh must parse/embed nothing, on both independent caches.
        for name,path in [('a',a),('b',b)]:
            prepare_only(packet,path,root/(name+'_noop_prepare.json'))
            tracked=git('-C',path,'ls-files').splitlines()
            assert all(n.startswith('records/') and '/sources/' in n and n.endswith('.json') for n in tracked)
            assert not git('-C',path,'status','--porcelain')
            result['sources'][name]={c['id']:SourceStore(path/'records'/c['id']).load('sources') for c in inputs['cases']}
        assert result['sources']['a']==result['sources']['b']
        assert len({p['pid'] for p in result['phases']})==6
        result['status']='complete'
    except BaseException as exc:
        result.update(status='failed',error=repr(exc));raise
    finally:save()


def prepare_only(packet,path,output):
    env=dict(os.environ);env['PRACTICAL_MODEL_URL']=os.environ['MODEL_URL_'+path.name]
    subprocess.run([sys.executable,'-u','-m','evaluation.git_local.prepare',str(packet),str(path),str(output)],env=env,check=True,timeout=1800)


if __name__=='__main__':main(Path(sys.argv[1]))
