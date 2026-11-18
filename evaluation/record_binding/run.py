"""Compute-node-only learned reference inference; no evaluation labels imported."""
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import time


def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        while block:=f.read(8*1024*1024): h.update(block)
    return h.hexdigest()


def main(folder):
    cfg=json.loads((folder/'config.json').read_text())
    assert os.environ.get('SLURM_JOB_ID') and os.environ.get('SLURMD_NODENAME')
    assert os.environ['CONDA_PREFIX']==cfg['conda_prefix']
    for n,h in cfg['files_sha256'].items(): assert sha(folder/n)==h,n
    import torch
    from huggingface_hub import snapshot_download
    from gliner2 import AutoExtractor
    from team_memory.records.learned_binding import predict, MODEL_ID, MODEL_REVISION
    torch.manual_seed(42);torch.set_num_threads(8)
    assert torch.cuda.device_count()==1
    job=os.environ['SLURM_JOB_ID'];out=Path(cfg['project'])/'results'/f'record-binding-{job}.json'
    assert not out.exists()
    result=dict(status='preparing',job_id=job,rows=[],model=MODEL_ID,revision=MODEL_REVISION,
                node=os.environ['SLURMD_NODENAME'],code_sha256=cfg['files_sha256'],
                reference_commit=cfg['reference_commit'],external_model_api_calls=0)
    started=time.monotonic()
    def save():
        result['seconds']=time.monotonic()-started
        tmp=out.with_suffix('.tmp');tmp.write_text(json.dumps(result,ensure_ascii=False,indent=2));tmp.replace(out)
    save()
    try:
        checkpoint=Path(cfg['checkpoint'])
        # New model only. Explicit project checkpoint path; no dataset copy.
        snapshot_download(MODEL_ID,revision=MODEL_REVISION,local_dir=checkpoint,
                          allow_patterns=['config.json','encoder_config/config.json','model.safetensors','tokenizer.json','tokenizer_config.json'])
        names=['config.json','encoder_config/config.json','model.safetensors','tokenizer.json','tokenizer_config.json']
        result['checkpoint_sha256']={n:sha(checkpoint/n) for n in names}
        result['checkpoint_config']=json.loads((checkpoint/'config.json').read_text())
        assert result['checkpoint_config']['boundary_head']['enable_records']
        model=AutoExtractor.from_pretrained(str(checkpoint),map_location='cuda')
        model.eval()
        assert type(model).__name__=='BoundaryExtractor'
        from safetensors import safe_open
        with safe_open(checkpoint/'model.safetensors',framework='pt',device='cpu') as f:
            keys=list(f.keys())
        result['record_head_weight_keys']=[k for k in keys if k.startswith('record_decoder.')]
        assert result['record_head_weight_keys']
        # Upstream load_state_dict defaults strict=True; no replacement head.
        result['strict_checkpoint_load']=True
        result['environment']={n:importlib.metadata.version(n) for n in ('gliner2','torch','transformers','peft','huggingface-hub','tokenizers')}
        counts={}
        for method in ('forward_groups_dense','forward_group_dense','forward_group'):
            original=getattr(model.record_decoder,method)
            def observed(*args,_name=method,_method=original,**kwargs):
                counts[_name]=counts.get(_name,0)+1
                return _method(*args,**kwargs)
            setattr(model.record_decoder,method,observed)
        result['status']='running';save()
        items=json.loads((folder/'inputs.json').read_text())['items']
        for item in items:
            before=dict(counts);tic=time.monotonic()
            with torch.inference_mode(): prediction=predict(model,item['source'])
            row=dict(id=item['id'],source=item['source'],prediction=prediction,seconds=time.monotonic()-tic,
                     record_head_calls={k:v-before.get(k,0) for k,v in counts.items()})
            assert sum(row['record_head_calls'].values())>0,'Record assignment head not executed'
            result['rows'].append(row);save();print('ROW',item['id'],len(prediction.get('statement',[])),flush=True)
        assert len(result['rows'])==68
        result.update(status='complete',record_head_calls=counts)
    except BaseException as exc:
        result.update(status='failed',error=f'{type(exc).__name__}: {exc}');raise
    finally:save()


if __name__=='__main__':
    import sys
    main(Path(sys.argv[1]))
