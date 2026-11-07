"""GPU-node-only dense retrieval preparation, before the Qwen server starts."""
from hashlib import sha256
import json
import os
from pathlib import Path
import sys
from urllib.request import urlopen


def main():
    folder = Path(sys.argv[1])
    cfg = json.loads((folder/'config.json').read_text())
    assert os.environ['SLURMD_NODENAME'] and os.environ['CONDA_PREFIX'] == cfg['conda_prefix']
    for name, digest in cfg['code_sha256'].items():
        assert sha256((folder/'code'/name).read_bytes()).hexdigest() == digest, name
    for name, digest in cfg['data_sha256'].items():
        assert sha256((folder/name).read_bytes()).hexdigest() == digest, name
    sys.path.insert(0, str(folder/'code'))
    import torch
    from transformers import AutoTokenizer
    from llama_index.core.schema import NodeWithScore
    from llama_index.core.vector_stores.utils import metadata_dict_to_node
    from team_memory.reference_retrieval import FeedbackRetriever
    from team_memory._vendor.longmemeval.contriever import Contriever
    from team_memory.store import digest
    from evaluation.reference_qa.expanded.run import iter_dialogue_messages

    assert torch.cuda.device_count() == 1
    model_path = Path(cfg['contriever_path'])
    model_path.mkdir(parents=True, exist_ok=True)
    files = {}
    for name in ['config.json','pytorch_model.bin','special_tokens_map.json','tokenizer.json','tokenizer_config.json','vocab.txt']:
        target = model_path/name
        if not target.exists():
            temporary = target.with_suffix(target.suffix+'.'+os.environ['SLURM_JOB_ID']+'.tmp')
            url = f"https://huggingface.co/facebook/contriever/resolve/{cfg['contriever_revision']}/{name}"
            with urlopen(url, timeout=120) as inp, temporary.open('xb') as out:
                while block := inp.read(8*1024*1024):
                    out.write(block)
            temporary.replace(target)
        files[name] = sha256(target.read_bytes()).hexdigest()
    assert files['pytorch_model.bin'] == cfg['contriever_weight_sha256']
    tokenizer = AutoTokenizer.from_pretrained(cfg['model_shared'], local_files_only=True)
    dense = Contriever(str(model_path), batch_size=16)
    cases = json.loads((folder/'inputs.json').read_text())
    result = dict(status='running', job_id=os.environ['SLURM_JOB_ID'], retrieval=[], topics=[],
        model_revision=cfg['contriever_revision'], model_files_sha256=files,
        code_sha256=cfg['code_sha256'], data_sha256=cfg['data_sha256'])
    output = Path(cfg['project'])/'results'/f"documents-{os.environ['SLURM_JOB_ID']}.retrieval.json"
    def save():
        tmp=output.with_suffix('.tmp'); tmp.write_text(json.dumps(result, ensure_ascii=False, indent=2)); tmp.replace(output)
    save()
    for topic in ['01','02']:
        data=Path(cfg['dataset_root'])/'EverMemBench-Dynamic'/topic/'dialogue.json'
        sources=[]
        for date,group,index,message in iter_dialogue_messages(json.loads(data.read_text())):
            location=f"EverMemBench-Dynamic@{cfg['ever_revision']}/{topic}/{date}/{group}/{index}"
            envelope=dict(owner=message['speaker'],observed_at=message['time'],
                source=dict(text=message['dialogue'],location=location,speaker=message['speaker']))
            sources.append(dict(source_id=digest(envelope),quote=message['dialogue'],start=0,
                end=len(message['dialogue']),location=location,speaker=message['speaker'],observed_at=message['time']))
        bm25=FeedbackRetriever(sources,tokenizer,None,top_k=8)
        # Reuse exactly the BM25 corpus nodes, not a separate chunking pipeline.
        nodes=[NodeWithScore(node=metadata_dict_to_node(metadata)) for metadata in bm25.original.corpus]
        corpus=bm25.witnesses(nodes)
        before=dense.truncated
        dense.index(corpus)
        result['topics'].append(dict(topic=topic, records=len(sources),chunks=len(corpus),
            key_truncations=dense.truncated-before,
            corpus_sha256=sha256(json.dumps(corpus,ensure_ascii=False,sort_keys=True).encode()).hexdigest(),
            dataset_sha256=sha256(data.read_bytes()).hexdigest()))
        for case in (c for c in cases['ever'] if c['topic']==topic):
            initial=bm25.witnesses(bm25.original.retrieve(case['query']))
            assert initial==case['sources'],case['id']
            selected=dense.retrieve(case['query'],8)
            assert len(selected)==8
            result['retrieval'].append(dict(id=case['id'],query=case['query'],initial_sources=initial,sources=selected))
            save()
        print('RETRIEVAL_COMPLETE',topic,len(corpus),flush=True)
    result['status']='complete'; save()


if __name__=='__main__':
    main()
