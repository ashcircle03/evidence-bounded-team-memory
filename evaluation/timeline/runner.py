"""Sequential inference: the model only receives already processed source history."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import tempfile
import time
from team_memory.store import Store
from team_memory import timeline as t


class Reader:
    def __init__(self, generator):
        self.generator=generator;self.calls=[];self.input_tokens=0;self.output_tokens=0
    def __call__(self, system, content):
        self.generator.cap=384 if system==t.INDEX else 512 if system==t.COMPARE else 320
        start=time.monotonic();raw=self.generator(system,content);usage=dict(self.generator.last_usage)
        self.input_tokens+=usage['input_tokens'];self.output_tokens+=usage['output_tokens']
        self.calls.append(dict(system=system,content=content,raw=raw,usage=usage,
                               seconds=time.monotonic()-start,cap=self.generator.cap))
        if self.input_tokens>120000 or self.output_tokens>7000:raise RuntimeError('stream budget exceeded')
        return raw


def stream(row, mode, generator):
    reader=Reader(generator);steps=[];start=time.monotonic()
    with tempfile.TemporaryDirectory(prefix='timeline-') as directory:
        store=Store(Path(directory)/'records')
        for step in row['steps']:
            op=step['op']
            if op=='ingest':
                result=t.ingest(store,step['source'],reader,mode)
                result['relations']=[p for p in t.proposals(store) if p['id'] in result['proposals']]
            elif op=='ask':
                result=t.ask(store,step['question'],reader,mode)
            elif op=='review':
                # Explicitly simulated owner action, only after the new report and pre-review QA.
                found=[p for p in t.proposals(store) if p['kind']==step['kind']
                    and p['previous']['source_id']==step['previous'] and p['incoming']['source_id']==step['incoming']
                    and step['old_contains'] in p['previous']['quote'] and step['new_contains'] in p['incoming']['quote']]
                result=dict(matched=len(found),reviews=[t.review(store,p['id'],step['actor'],step['choice']) for p in found])
            else:raise ValueError(op)
            steps.append(dict(op=op,id=step.get('id'),result=result))
        state=t.view(store)
        objects={kind:store.load(kind) for kind in ('sources','timeline_index','timeline_proposals','timeline_votes')}
        objects['timeline_receipts']=t.client_store(store).load('receipts')
        assert len(objects['sources'])==sum(s['op']=='ingest' for s in row['steps'])
    return dict(id=row['id'],mode=mode,steps=steps,final_state=state,objects=objects,calls=reader.calls,
                input_tokens=reader.input_tokens,output_tokens=reader.output_tokens,seconds=time.monotonic()-start)


def run(args):
    import torch
    from runtime import load
    blob=args.input.read_bytes();payload=json.loads(blob);generator=load(args.model,large=True)
    result=dict(status='running',job_id=args.job,input_sha256=sha256(blob).hexdigest(),
        model='Qwen2.5-14B-Instruct',revision='cf98f3b3bbb457ad9e2bb7baf9a0125b6b88caa8',identity=generator.identity,
        devices=[torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())],streams={})
    partial=args.output.with_suffix('.partial.jsonl')
    with partial.open('x') as log:
        for i,row in enumerate(payload['streams']):
            for mode in (('direct','indexed') if i%2==0 else ('indexed','direct')):
                r=stream(row,mode,generator);result['streams'][row['id']+'/'+mode]=r
                log.write(json.dumps(r,ensure_ascii=False)+'\n');log.flush()
                print(row['id'],mode,'calls',len(r['calls']),'tokens',r['input_tokens'],r['output_tokens'],flush=True)
    result.update(status='complete',peak_gpu_bytes=[torch.cuda.max_memory_allocated(i) for i in range(torch.cuda.device_count())])
    tmp=args.output.with_suffix('.tmp');tmp.write_text(json.dumps(result,ensure_ascii=False));tmp.replace(args.output)


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('input',type=Path);p.add_argument('model');p.add_argument('output',type=Path);p.add_argument('job')
    run(p.parse_args())
