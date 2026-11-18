"""One bounded upstream training run on independent procedural supervision."""
import hashlib
import json
import os
from pathlib import Path
import time


def signature(records):
    values=set()
    for r in records:
        a=r.get('claim')
        if not isinstance(a,dict):continue
        anchor=(a['start'],a['end'])
        values.add(('claim',*anchor))
        for role in ('condition','basis'):
            for v in r.get(role,[]):
                values.add((role,*anchor,v['start'],v['end']))
    return values


def main(folder):
    import torch
    from gliner2 import AutoExtractor
    from gliner2.training.data import InputExample
    from gliner2.training.trainer import ExtractorTrainer, ExtractorDataset, ExtractorCollator, TrainingConfig
    from team_memory.records.learned_binding import predict
    from evaluation.record_binding.run import sha
    cfg=json.loads((folder/'config.json').read_text())
    assert os.environ.get('SLURM_JOB_ID') and os.environ['CONDA_PREFIX']==cfg['conda_prefix']
    assert torch.cuda.device_count()==1
    for p,h in cfg['files_sha256'].items():assert sha(folder/p)==h,p
    job=os.environ['SLURM_JOB_ID'];out=Path(cfg['project'])/'results'/f'record-adapt-{job}.json'
    assert not out.exists();torch.manual_seed(42);torch.set_num_threads(8)
    result=dict(status='preparing',job_id=job,rows=[],external_model_api_calls=0,config=cfg,training_audit=[])
    start=time.monotonic()
    def save():
        result['seconds']=time.monotonic()-start
        tmp=out.with_suffix('.tmp');tmp.write_text(json.dumps(result,ensure_ascii=False,indent=2));tmp.replace(out)
    save()
    try:
        data=Path(cfg['training_data_dir'])
        for n in ('train.json','dev.json'):assert sha(data/n)==cfg['files_sha256'][n]
        train=json.loads((data/'train.json').read_text());dev=json.loads((data/'dev.json').read_text())
        assert not ({r['family'] for r in train}&{r['family'] for r in dev})
        for r in train+dev:
            assert not InputExample.from_dict(r).validate(),r['id']
        # Upstream's sanitizing round trip drops explicit field metadata. We
        # validate without mutation, then retain the exact original schema.
        td=ExtractorDataset([{k:r[k] for k in ('input','output')} for r in train],validate=False,shuffle=True,seed=42)
        vd=ExtractorDataset([{k:r[k] for k in ('input','output')} for r in dev],validate=False,shuffle=False)
        assert all(r['output']['record_metadata']['statement']['fields']['basis']['cardinality']=='zero_or_more' for r in td.data)
        model=AutoExtractor.from_pretrained(cfg['base_checkpoint'],map_location='cuda')
        assert model.boundary_settings.enable_records
        from gliner2.processor import SamplingConfig
        # This is a single-task dataset; dropping its only structure would
        # remove all supervision. Keep upstream field-order augmentation.
        model.processor.sampling_config=SamplingConfig(remove_json_structure_prob=0.0)
        collate=ExtractorCollator(model.processor,is_training=True,architecture='boundary',max_gold_per_query=64)
        batch=collate([td[0],td[1]])
        for specs in batch.record_specs:
            for spec in specs.values():
                assert spec.mode=='natural'
                assert {f.name:f.cardinality.value for f in spec.fields}==dict(claim='required_one',condition='zero_or_more',basis='zero_or_more')
        result['training_schema_verified']=True
        before={k:v.detach().cpu().clone() for k,v in model.record_decoder.state_dict().items()}
        grad_stats=dict(calls=0,nonzero=0)
        def grad_hook(g):
            grad_stats['calls']+=1
            if torch.isfinite(g).all() and g.abs().sum()>0:grad_stats['nonzero']+=1
            return g
        handles=[p.register_hook(grad_hook) for p in model.record_decoder.parameters() if p.requires_grad]
        def loss_audit(m,args,output):
            if not m.training:return
            assert output.losses is not None and 'record_field_loss' in output.losses,'Missing field supervision'
            v=output.losses['record_field_loss'];assert v is not None and torch.isfinite(v) and v.requires_grad
            result['training_audit'].append(dict(field_loss=float(v.detach()),object_loss=float(output.losses['record_object_loss'].detach())))
        handle=model.register_forward_hook(loss_audit)
        val_history=[]
        def validate(m,_dataset):
            tp=fp=fn=0;rows=[]
            for r in dev:
                with torch.inference_mode():p=predict(m,dict(text=r['input']))
                got=signature(p.get('statement',[]));gold=signature([s['statement'] for s in r['output']['json_structures']])
                tp+=len(got&gold);fp+=len(got-gold);fn+=len(gold-got)
                rows.append(dict(id=r['id'],prediction=p))
            f1=2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 0
            val_history.append(dict(tp=tp,fp=fp,fn=fn,f1=f1,rows=rows))
            result['validation_history']=val_history;save()
            return dict(dev_joint_f1=f1)
        conf=TrainingConfig(output_dir=cfg['output_checkpoint'],num_epochs=6,batch_size=8,eval_batch_size=8,
            encoder_lr=1e-5,task_lr=5e-4,fp16=False,bf16=False,eval_strategy='epoch',save_best=True,
            metric_for_best='dev_joint_f1',greater_is_better=True,save_total_limit=1,
            logging_steps=10,num_workers=0,validate_data=False,report_to_wandb=False,seed=42)
        result['training_config']=conf.to_dict() if hasattr(conf,'to_dict') else vars(conf)
        result['status']='training';save()
        trainer=ExtractorTrainer(model,conf,compute_metrics=validate)
        result['training_summary']=trainer.train(train_data=td,eval_data=vd)
        result['record_head_gradients']=grad_stats
        assert grad_stats['nonzero']>0 and result['training_audit']
        result['changed_record_parameters']=sum(not torch.equal(v,model.record_decoder.state_dict()[k].detach().cpu()) for k,v in before.items())
        assert result['changed_record_parameters']>0
        handle.remove()
        for h in handles:h.remove()
        del trainer,model;torch.cuda.empty_cache()
        selected=Path(cfg['output_checkpoint'])/'best'
        model=AutoExtractor.from_pretrained(str(selected),map_location='cuda');model.eval()
        result['selected_checkpoint']=str(selected)
        result['checkpoint_sha256']={n:sha(selected/n) for n in ['config.json','model.safetensors','tokenizer.json','tokenizer_config.json']}
        result['status']='evaluating_fixed_inputs';save()
        for item in json.loads((folder/'inputs.json').read_text())['items']:
            with torch.inference_mode():p=predict(model,item['source'])
            result['rows'].append(dict(id=item['id'],source=item['source'],prediction=p));save()
            print('ROW',item['id'],len(p.get('statement',[])),flush=True)
        assert len(result['rows'])==68
        result['status']='complete'
    except BaseException as exc:
        result.update(status='failed',error=f'{type(exc).__name__}: {exc}');raise
    finally:save()


if __name__=='__main__':
    import sys
    main(Path(sys.argv[1]))
