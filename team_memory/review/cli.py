"""Run the minimal timeline client in each team member's checkout."""
import argparse
import json
from pathlib import Path
import subprocess
from team_memory.storage.objects import Store
from team_memory.review import state as t


def local_reader(path):
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    tokenizer=AutoTokenizer.from_pretrained(path,local_files_only=True)
    model=AutoModelForCausalLM.from_pretrained(path,local_files_only=True,
             torch_dtype=torch.bfloat16,device_map='auto').eval()
    @torch.inference_mode()
    def generate(system,content):
        cap=384 if system==t.INDEX else 512 if system==t.COMPARE else 320
        ids=tokenizer.apply_chat_template([dict(role='system',content=system),dict(role='user',content=content)],
                 add_generation_prompt=True,return_tensors='pt').to(model.device)
        out=model.generate(input_ids=ids,max_new_tokens=cap,do_sample=False,pad_token_id=tokenizer.eos_token_id)
        return tokenizer.decode(out[0,ids.shape[1]:],skip_special_tokens=True)
    return generate


def process_sources(store,generate,mode):
    sources=store.load('sources')
    processed={r['source_id'] for r in t.receipts(store) if r['mode']==mode}
    rows=[]
    for sid,e in sorted(sources.items(),key=lambda kv:(kv[1]['observed_at'],kv[0])):
        if sid not in processed:rows.append(t.ingest(store,e,generate,mode))
    return rows


def pull(store, generate, mode):
    root=store.root.resolve()
    while not root.exists():root=root.parent
    repo=Path(subprocess.check_output(['git','-C',str(root),'rev-parse','--show-toplevel'],text=True).strip())
    subprocess.run(['git','-C',str(repo),'pull','--ff-only'],check=True,capture_output=True,text=True)
    # Git may transport multiple sources at once. ingest exposes only processed receipts.
    return process_sources(store,generate,mode)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--store',default='shared-records');p.add_argument('--mode',choices=('direct','indexed'),default='direct')
    sub=p.add_subparsers(dest='command',required=True)
    for name in ('ingest','ask','pull'):
        s=sub.add_parser(name);s.add_argument('--model',required=True)
        if name=='ingest':s.add_argument('json_file',type=Path)
        if name=='ask':s.add_argument('question')
    sub.add_parser('view')
    r=sub.add_parser('review');r.add_argument('proposal');r.add_argument('actor');r.add_argument('choice',choices=('approve','reject'))
    args=p.parse_args();store=Store(args.store)
    root=store.root.resolve()
    while not root.exists():root=root.parent
    probe=subprocess.run(['git','-C',str(root),'rev-parse','--absolute-git-dir'],text=True,capture_output=True)
    if probe.returncode==0:
        from team_memory.storage.objects import digest
        store.timeline_client_root=Path(probe.stdout.strip())/'timeline-clients'/digest(str(store.root.resolve()))
    if args.command=='view':result=t.view(store)
    elif args.command=='review':result=t.review(store,args.proposal,args.actor,args.choice)
    else:
        reader=local_reader(args.model)
        if args.command=='ingest':
            process_sources(store,reader,args.mode)
            result=t.ingest(store,json.loads(args.json_file.read_text()),reader,args.mode)
        elif args.command=='ask':result=t.ask(store,args.question,reader,args.mode)
        else:result=pull(store,reader,args.mode)
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
