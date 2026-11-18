"""Supervised adaptation of DisCoDisCo's directed body/sentence-pair input."""
import csv
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import random
import sys
from urllib.request import urlopen

import numpy as np
import torch
from torch import nn
from transformers import AutoModel, AutoTokenizer

PROJECT=Path('/ceph_data/pjw031003/capstone-shared-knowledge')
ENCODER=PROJECT/'runtime/speakermem-v1/models/embed'
REV='a9dac1afd9f9800c4fbe704b7ade839bf298c97f'
BLOBS={'train':'aaaf1ce2879e5aac7bc4dfc9ded0e6f2db886154','dev':'675b2fa931c5e1c19980daeadcfcb9bdd86449ce'}
LABELS=['keep','condition','basis']
BASIS={'cause','purpose','motivation','justify','evidence'}


def corpus(split):
    name=f'eng.rst.gum_{split}.rels'
    root=Path('/local_datasets/pjw031003/capstone-shared-knowledge/disrpt2021')/REV
    root.mkdir(parents=True,exist_ok=True)
    path=root/name
    data=path.read_bytes() if path.exists() else urlopen(
        f'https://raw.githubusercontent.com/disrpt/sharedtask2021/{REV}/data/eng.rst.gum/{name}',timeout=60).read()
    assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==BLOBS[split]
    if not path.exists():
        tmp=path.with_suffix('.tmp');tmp.write_bytes(data);tmp.replace(path)
    rows=[]
    for r in csv.DictReader(data.decode().splitlines(),delimiter='\t',quoting=csv.QUOTE_NONE):
        if not all(any(c.isalpha() for c in r[k]) for k in ('unit1_txt','unit2_txt')):continue
        if r['doc'].startswith('GUM_reddit_'):continue  # masked subset in shared task
        label=r['label']
        rows.append((render(r['unit1_txt'],r['unit2_txt'],r['unit1_sent'],r['unit2_sent'],r['dir']),
                     1 if label=='condition' else 2 if label in BASIS else 0))
    return rows


def render(left,right,left_sentence,right_sentence,direction):
    # Mark dependency direction in both the unit and surrounding sentence channels.
    def marked(a,b):
        return ('} '+a+' > [SEP] '+b) if direction=='1>2' else (a+' [SEP] < '+b+' {')
    return marked(left,right),marked(left_sentence,right_sentence)


def record_input(pair):
    c,t=pair['context'],pair['target']
    # An embedded qualifier retains its original text order and both endpoints.
    left,right,direction=(c,t,'1>2') if c['start']<=t['start'] else (t,c,'1<2')
    return render(left['text'],right['text'],left['sentence'],right['sentence'],direction)


class RelationModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.encoder=AutoModel.from_pretrained(ENCODER,local_files_only=True)
        self.head=nn.Linear(2*self.encoder.config.hidden_size,3)

    def forward(self,tokens):
        vec=self.encoder(**tokens).last_hidden_state[:,0]
        body,sentence=vec.chunk(2)
        return self.head(torch.cat((body,sentence),dim=1))


def main(folder):
    job=os.environ['SLURM_JOB_ID']
    assert os.environ['SLURMD_NODENAME']=='aurora-g8' and torch.cuda.is_available()
    assert Path(os.environ['CONDA_PREFIX'])==PROJECT/'runtime/cupmem-qwen3-v1'
    torch.manual_seed(42);random.seed(42);np.random.seed(42)
    tokenizer=AutoTokenizer.from_pretrained(ENCODER,local_files_only=True)
    model=RelationModel().cuda()
    def logits(inputs):
        body,sentence=zip(*inputs)
        tokens=tokenizer(list(body)+list(sentence),max_length=128,padding=True,truncation=True,return_tensors='pt').to('cuda')
        return model(tokens)
    train=corpus('train');dev=corpus('dev')
    print('DATA',len(train),len(dev),flush=True)
    weights=np.bincount([label for _,label in train])**-0.5
    criterion=nn.CrossEntropyLoss(weight=torch.tensor(weights/weights.mean(),dtype=torch.float32,device='cuda'))
    opt=torch.optim.AdamW(model.parameters(),lr=3e-5)
    for epoch in range(3):
        model.train();random.shuffle(train)
        for start in range(0,len(train),32):
            inputs,labels=zip(*train[start:start+32])
            opt.zero_grad(set_to_none=True)
            loss=criterion(logits(inputs),torch.tensor(labels,device='cuda'))
            loss.backward();torch.nn.utils.clip_grad_norm_(model.parameters(),1.0);opt.step()
        print('EPOCH',epoch+1,flush=True)
    model.eval()
    def probs(inputs):
        with torch.inference_mode():
            return np.concatenate([logits(inputs[i:i+32]).softmax(1).cpu().numpy() for i in range(0,len(inputs),32)])
    pred=probs([x for x,_ in dev]);truth=np.array([y for _,y in dev])
    calibration={}
    for k in (1,2):
        points=[]
        for threshold in (0.50,0.60,0.70,0.80,0.85,0.90,0.95,0.975,0.99):
            use=(pred.argmax(1)==k)&(pred[:,k]>=threshold)
            points.append(dict(threshold=threshold,n=int(use.sum()),correct=int((truth[use]==k).sum())))
        accepted=next((p['threshold'] for p in points if p['n']>=10 and p['correct']/p['n']>=0.90),None)
        calibration[LABELS[k]]=dict(threshold=accepted,points=points)
    ckpt=PROJECT/'checkpoints'/f'record-discourse-{job}';ckpt.mkdir(parents=True,exist_ok=False)
    torch.save(model.state_dict(),ckpt/'weights.pt')
    (ckpt/'calibration.json').write_text(json.dumps(calibration))
    packet=(folder/'pairs.json').read_bytes()
    docs=json.loads(packet);pairs=[p for d in docs for p in d['pairs']]
    predictions=iter(probs([record_input(p) for p in pairs]))
    rows=[]
    for d in docs:
        decisions=[]
        for p in d['pairs']:
            proba=next(predictions);k=int(proba.argmax());label=LABELS[k]
            threshold=calibration.get(label,{}).get('threshold')
            selected=label if threshold is not None and proba[k]>=threshold else 'keep'
            decisions.append(dict(index=p['index'],probs=proba.tolist(),argmax=label,decision=selected))
        rows.append(dict(id=d['id'],decisions=decisions))
    result=dict(status='complete',job=job,checkpoint=str(ckpt),rows=rows,calibration=calibration,
                train_counts=dict(Counter(LABELS[y] for _,y in train)),dev_counts=dict(Counter(LABELS[y] for _,y in dev)),
                input_sha256=hashlib.sha256(packet).hexdigest(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    assert len(rows)==68
    (PROJECT/'results'/f'record-discourse-{job}.json').write_text(json.dumps(result,indent=2))
    print('COMPLETE',len(pairs),flush=True)

if __name__=='__main__':
    main(Path(sys.argv[1]))
