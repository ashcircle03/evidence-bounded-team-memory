"""Locked checkpoint and thresholds. No fitting or benchmark labels."""
from collections import Counter,defaultdict
import csv
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import re
import sys

import torch

from base_run import ENCODER, PROJECT, REV, BLOBS, BASIS, LABELS, RelationModel, record_input, render, AutoTokenizer

def tokens(value):
    indices=set()
    for part in re.findall(r'\d+(?:-\d+)?',value):
        ends=list(map(int,part.split('-')))
        indices.update(range(ends[0],ends[-1]+1))
    return indices

def gum(split):
    path=Path('/local_datasets/pjw031003/capstone-shared-knowledge/disrpt2021')/REV/f'eng.rst.gum_{split}.rels'
    data=path.read_bytes()
    assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==BLOBS[split]
    return [r for r in csv.DictReader(data.decode().splitlines(),delimiter='\t',quoting=csv.QUOTE_NONE)
            if not r['doc'].startswith('GUM_reddit_') and all(any(c.isalpha() for c in r[k]) for k in ('unit1_txt','unit2_txt'))]

def audit(train):
    geometries=Counter(); labels=defaultdict(Counter); examples=defaultdict(list)
    for r in train:
        assert r['dir'] in ('1>2','1<2')
        direction=r['dir']=='1>2'
        c,t=(('unit1','unit2') if direction else ('unit2','unit1'))
        cpos,tpos=tokens(r[c+'_toks']),tokens(r[t+'_toks'])
        assert cpos and tpos
        geometries['disjoint' if not cpos&tpos else 'embedded' if cpos<=tpos else 'partial_overlap']+=1
        quote=r[c+'_txt'];label=r['label']
        patterns={'considering':r'^considering\b','for_np_or_clause':r'^for\b','all':r'^all\b','if':r'^if\b','because':r'^because\b'}
        keys=[k for k,v in patterns.items() if re.search(v,quote,re.I)]
        if label in ('condition','cause','evidence','purpose'):keys.append('label_'+label)
        for key in keys:
            labels[key][label]+=1
            if len(examples[key])<4:
                examples[key].append(dict(doc=r['doc'],context=quote,target=r[t+'_txt'],label=label,direction=r['dir']))
    return dict(geometries=geometries,label_counts=labels,examples=examples)

def main(folder):
    assert os.environ['SLURMD_NODENAME']=='aurora-g8' and torch.cuda.is_available()
    assert Path(os.environ['CONDA_PREFIX'])==PROJECT/'runtime/cupmem-qwen3-v1'
    train,dev=gum('train'),gum('dev');assert (len(train),len(dev))==(11974,1845)
    stats=audit(train)
    ckpt=PROJECT/'checkpoints/record-discourse-124235'
    cal=json.loads((ckpt/'calibration.json').read_text());model=RelationModel()
    model.load_state_dict(torch.load(ckpt/'weights.pt',map_location='cpu',weights_only=True))
    model.cuda().eval();tok=AutoTokenizer.from_pretrained(ENCODER,local_files_only=True)
    @torch.inference_mode()
    def infer(inputs):
        flat=[]
        for start in range(0,len(inputs),32):
            body,sent=zip(*inputs[start:start+32])
            enc=tok(list(body)+list(sent),max_length=128,truncation=True,padding=True,return_tensors='pt').to('cuda')
            for prob in model(enc).softmax(1).tolist():
                label=LABELS[max(range(3),key=prob.__getitem__)];thr=cal.get(label,{}).get('threshold')
                flat.append(dict(probs=prob,argmax=label,decision=label if thr is not None and max(prob)>=thr else 'keep'))
        return flat
    dev_pred=infer([render(r['unit1_txt'],r['unit2_txt'],r['unit1_sent'],r['unit2_sent'],r['dir']) for r in dev])
    bins={}
    for lo,hi in [(0.8,0.85),(0.99,1.0001)]:
        labs=[r['label'] for r,p in zip(dev,dev_pred) if p['argmax']=='basis' and lo<=p['probs'][2]<hi]
        bins[str(lo)]=dict(n=len(labs),correct=sum(l in BASIS for l in labs),labels=Counter(labs))
    docs=json.loads((folder/'pairs.json').read_text())
    outputs={}
    for arm in ('old','sentence','remove_duplicate_diagnostic'):
        inputs=[]
        for d in docs:
            for p in d['pairs'] if arm=='old' else d['localized']:
                p=deepcopy(p)
                if arm=='remove_duplicate_diagnostic' and p['geometry']=='embedded':
                    c,t=p['context'],p['target'];a,b=c['start']-t['start'],c['end']-t['start']
                    t['text']=(t['text'][:a]+' '+t['text'][b:]).strip()
                inputs.append(record_input(p))
        outputs[arm]=infer(inputs)
    result=dict(status='complete',job=os.environ['SLURM_JOB_ID'],train_stats=stats,dev_basis_bins=bins,
        calibration=cal,outputs=outputs,hashes={name:hashlib.sha256((folder/name).read_bytes()).hexdigest()
                                                for name in ('base_run.py','run.py','pairs.json')})
    (PROJECT/'results'/('record-scope-'+result['job']+'.json')).write_text(json.dumps(result,indent=2))
    print('COMPLETE',len(inputs),stats['geometries'],flush=True)
if __name__=='__main__':main(Path(sys.argv[1]))
