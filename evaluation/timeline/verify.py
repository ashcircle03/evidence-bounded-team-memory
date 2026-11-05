"""Audit completed Slurm outputs before scoring or claiming model results."""
from hashlib import sha256
import json
import sys
import zipfile
from .build import HERE, ROOT, write
from team_memory.store import digest

CAMPAIGN=ROOT.parent/'campaigns/speakermem-dev'
OUT=ROOT/'results/timeline'


def verify(phase):
    versions=['timeline-dev-v1'] if phase=='development' else ['timeline-final-a-v1','timeline-final-b-v1']
    ledger=json.loads((CAMPAIGN/'campaign-dispatch.json').read_text())
    for path,h in json.loads((HERE/'freeze.json').read_text())['files'].items():
        assert sha256((ROOT/path).read_bytes()).hexdigest()==h,path
    if phase=='final':
        for name,h in json.loads((HERE/'data-freeze.json').read_text())['files'].items():
            assert sha256((HERE/name).read_bytes()).hexdigest()==h,name
    streams={};runs=[];identity=None
    for version in versions:
        j=ledger['jobs'][version]
        assert (j['state'],j['exit_code'],j.get('verified'))==('COMPLETED','0:0',True),version
        src=CAMPAIGN/'source'/version;path=CAMPAIGN/'results'/f"sm-{j['job_id']}.json"
        for name,h in j['source_sha256'].items():assert sha256((src/name).read_bytes()).hexdigest()==h,(version,name)
        data=json.loads(path.read_text());payload=json.loads((src/'packets.json').read_text())
        assert data['status']=='complete' and str(data['job_id'])==j['job_id']
        assert data['input_sha256']==j['source_sha256']['packets.json']
        assert data['model']=='Qwen2.5-14B-Instruct' and data['revision']=='cf98f3b3bbb457ad9e2bb7baf9a0125b6b88caa8'
        if identity is None:identity=data['identity']
        assert data['identity']==identity
        expected={r['id']+'/'+m for r in payload['streams'] for m in ('direct','indexed')}
        assert set(data['streams'])==expected
        assert not (set(streams)&expected)
        if phase=='final':
            with zipfile.ZipFile(src/'infer.py') as z:
                for p in (ROOT/'team_memory').glob('*.py'):assert z.read('team_memory/'+p.name)==p.read_bytes()
                assert z.read('__main__.py')==(HERE/'runner.py').read_bytes()
        for uid,s in data['streams'].items():
            row=next(r for r in payload['streams'] if r['id']==s['id'])
            originals={digest(x['source']):x['source'] for x in row['steps'] if x['op']=='ingest'}
            assert s['objects']['sources']==originals,(uid,'raw loss')
            assert s['input_tokens']==sum(c['usage']['input_tokens'] for c in s['calls'])<=120000
            assert s['output_tokens']==sum(c['usage']['output_tokens'] for c in s['calls'])<=7000
            assert len(s['steps'])==len(row['steps'])
            approved=set()
            for expected_step,step in zip(row['steps'],s['steps']):
                assert expected_step['op']==step['op'] and expected_step.get('id')==step['id']
                if step['op']=='review':
                    for p in step['result']['reviews']:
                        assert p['reviewer']==expected_step['actor'] and p['status']=='approved'
                        approved.add(p['id'])
                if step['op']=='ask':
                    for a in step['result'].get('answers',[]):
                        if a['status'] in ('approved_correction','superseded_assertion','correction_conflict'):
                            assert approved,(uid,step['id'],'unreviewed promotion')
            assert all(p['status']!='approved' or p['id'] in approved for p in s['final_state']['relations'])
        streams.update(data['streams'])
        runs.append(dict(version=version,job=j,result_sha256=sha256(path.read_bytes()).hexdigest()))
    write(OUT/f'{phase}-generations.json',dict(status='verified_complete',streams=streams))
    goaljobs=[j for v,j in ledger['jobs'].items() if v.startswith('timeline-')]
    write(OUT/f'{phase}-audit.json',dict(status='passed',phase=phase,runs=runs,stream_arms=len(streams),
          model_identity=identity,frozen_inputs_unchanged=True,raw_source_losses=0,unreviewed_promotions=0,
          gpu_seconds=sum(j.get('elapsed_seconds',0)*j['gpus'] for j in goaljobs),
          cpu_only_seconds=sum(j.get('elapsed_seconds',0) for j in goaljobs if not j['gpus']),
          accounting_note='Elapsed usage for checked jobs; pending or unrefreshed jobs are not a completed total. Missing MaxRSS is not zero memory usage.'))
    print('verified',phase,len(streams),'stream-arms')


if __name__=='__main__':verify(sys.argv[1])
