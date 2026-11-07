"""Compute-node replay: preserve Qwen text and verify/rerank added citations."""
from copy import deepcopy
from hashlib import sha256,sha1
import json,os,sys,time,urllib.request
from pathlib import Path


def save_json(path,value):
    tmp=path.with_suffix('.tmp')
    tmp.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
    tmp.replace(path)


def main():
    folder=Path(sys.argv[1]);cfg=json.loads((folder/'config.json').read_text(encoding='utf-8'))
    job=os.environ['SLURM_JOB_ID'];assert os.environ['SLURMD_NODENAME']
    assert os.environ['CONDA_PREFIX']==cfg['conda_prefix']
    sys.path.insert(0,str(folder/'code'))
    for name,h in cfg['code_sha256'].items():assert sha256((folder/'code'/name).read_bytes()).hexdigest()==h
    for name,h in cfg['replay_files_sha256'].items():assert sha256((folder/name).read_bytes()).hexdigest()==h
    assert sha256((folder/'inputs.json').read_bytes()).hexdigest()==cfg['input_sha256']
    previous=json.loads((folder/'prior-result.json').read_text(encoding='utf-8'));assert previous['status']=='complete'
    record=deepcopy(previous);began=time.monotonic()
    record.update(status='running',job_id=job,source_version=cfg['source_version'],code_sha256=cfg['code_sha256'],
        replay_from_job_id=previous['job_id'],scope='All20 unchanged Qwen answers; only citation selection uses new trained NLI predictions',
        reused_physical_calls=previous['calls'],new_physical_calls=0,nli_pairs=0,nli_model=cfg['nli_model'],
        replay_files_sha256=cfg['replay_files_sha256'])
    output=Path(cfg['project'])/'results'/f'cup-reference-{job}.json'
    server_path=output.with_name(f'sm-{job}.json')
    server=dict(status='preparing',job_id=job,source_version=cfg['source_version'],
        node=os.environ['SLURMD_NODENAME'],external_model_api_calls=0,native_result=str(output))
    def save():
        record['seconds']=time.monotonic()-began
        for path,value in [(output,record),(server_path,server)]:
            save_json(path,value)
    save()
    calls=output.with_suffix('.calls.jsonl')
    with calls.open('x',encoding='utf-8') as f:
        for line in (folder/'prior-calls.jsonl').read_text(encoding='utf-8').splitlines():
            c=json.loads(line);c['replayed_from_job_id']=previous['job_id'];f.write(json.dumps(c,ensure_ascii=False)+'\n')
    nli_file=output.with_suffix('.nli.jsonl').open('x',encoding='utf-8');context={}
    try:
        plan=cfg['nli_model'];dest=Path(cfg['nli_model_path']);dest.mkdir(parents=True,exist_ok=True)
        verified={}
        for info in plan['files']:
            name=info['rfilename'];assert Path(name).name==name
            path=dest/name
            if not path.exists():
                temp=dest/(name+'.'+job+'.part');assert not temp.exists()
                url=f"https://huggingface.co/{plan['repository']}/resolve/{plan['revision']}/{name}?download=true"
                with urllib.request.urlopen(url,timeout=60) as inp,temp.open('xb') as out:
                    while block:=inp.read(8*1024*1024):out.write(block)
                temp.replace(path)
            data=path.read_bytes();assert len(data)==info['size']
            if info.get('lfs'):assert sha256(data).hexdigest()==info['lfs']['sha256']
            else:assert sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()==info['blobId']
            verified[name]=sha256(data).hexdigest();del data
            print('MODEL_FILE_VERIFIED',name,flush=True)
        record['nli_files_sha256']=verified
        import torch
        assert torch.cuda.device_count()==1
        from team_memory.reference_nli import LocalNLIVerifier
        from team_memory.reference_attributed import add_missing_citations
        from team_memory.reference_qa import format_response
        def observe(value):
            trace=dict(id=record['nli_pairs'],context=dict(context),**value)
            nli_file.write(json.dumps(trace,ensure_ascii=False)+'\n');nli_file.flush();record['nli_pairs']+=1
        nli=LocalNLIVerifier(str(dest),device='cuda',observe=observe)
        server['status']='ready';save()
        for row in record['rows']:
            for step in row['steps']:
                if step['label']=='import':continue
                start=time.monotonic();context.clear();context.update(case_id=row['case_id'],label=step['label'])
                original=step['result'];base=deepcopy(original)
                base.update(format_response(original['alce']['question'],original['pre_citation_raw'],
                    original['citation_sources'],allow_source_labels=True))
                for key in ('posthoc_citations','pre_citation_raw'):base.pop(key,None)
                before=record['nli_pairs'];out=add_missing_citations(base,nli)
                assert out['pre_citation_raw']==original['pre_citation_raw']
                step.update(result=out,previous_seconds=step['seconds'],seconds=time.monotonic()-start,
                    new_physical_calls=0,nli_pairs=record['nli_pairs']-before,
                    answer_text_unchanged=out['raw']==original['raw'],answer_words_unchanged=True)
                save();print('NLI_STEP',row['case_id'],step['label'],step['nli_pairs'],flush=True)
        assert record['nli_pairs']==cfg['expected_nli_pairs']
        record['status']='complete';server.update(status='complete',client_exit_code=0)
    except BaseException as exc:
        record.update(status='failed',error=type(exc).__name__+': '+str(exc))
        server.update(status='failed',error=record['error']);raise
    finally:
        save();nli_file.close()


if __name__=='__main__':main()
