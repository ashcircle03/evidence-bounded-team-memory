"""JSONL adapter for a local model; transport/authentication belongs to the caller.

Start the local model inside an existing Slurm GPU allocation, then pipe source,
question and explicit owner-review requests to this process. No UI or MCP server.
"""
import argparse
from contextlib import redirect_stdout
import json
import os
from pathlib import Path
import sys
from urllib.parse import urlparse


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--upstream',required=True,type=Path)
    parser.add_argument('--embedding',required=True,type=Path)
    parser.add_argument('--store',required=True,type=Path)
    parser.add_argument('--base-url',required=True)
    parser.add_argument('--strategy',choices=('simple','cupmem'),required=True,
                        help='simple: retained development base; cupmem: experimental candidate')
    args=parser.parse_args()
    endpoint=urlparse(args.base_url)
    if endpoint.scheme!='http' or endpoint.hostname not in ('127.0.0.1','localhost') or endpoint.path.rstrip('/')!='/v1':
        parser.error('Use the local /v1 inference endpoint in your compute allocation')
    if not os.environ.get('SLURM_JOB_ID') or not os.environ.get('CONDA_PREFIX'):
        parser.error('Run in an activated conda environment inside a Slurm GPU allocation')
    if not (os.environ.get('SLURM_JOB_GPUS') or os.environ.get('SLURM_STEP_GPUS') or os.environ.get('CUDA_VISIBLE_DEVICES')):
        parser.error('A GPU allocation is required')
    root=Path(__file__).resolve().parents[1]
    sys.path[:0]=[str(root),str(args.upstream)]
    from cup_mem import CupMemEngine, LLMClient
    from openai import OpenAI
    from evaluation.cupmem.upstream import verify_source
    from team_memory.cupmem_candidates import CachedEmbedding, CUPMemCandidateMemory, SourceOnlyMemory
    from team_memory.cupmem_practical import PracticalCUPMemService

    verify_source(args.upstream)

    # Match the frozen evaluation's local model settings. Do not silently use a
    # paid fallback or extend request/runtime limits when an operation fails.
    class LocalOpenAI(OpenAI):
        def __init__(self,**kwargs):
            super().__init__(**kwargs,max_retries=0,timeout=90)
            original=self.chat.completions.create
            def create(**request):
                request['max_tokens']=4096
                request.setdefault('temperature',0)
                request.setdefault('response_format',{'type':'json_object'})
                request['extra_body']={'chat_template_kwargs':{'enable_thinking':False}}
                return original(**request)
            self.chat.completions.create=create

    llm=LLMClient(model='Qwen3-8B',api_key='local-no-secret',base_url=args.base_url,openai_cls=LocalOpenAI)
    with redirect_stdout(sys.stderr):
        engine=CupMemEngine(llm=llm,embedding_model_path=str(args.embedding),embedding_device='cpu')
    engine.embedding=CachedEmbedding(engine.embedding)
    reader=LocalOpenAI(api_key='local-no-secret',base_url=args.base_url)
    def generate(system,content):
        return reader.chat.completions.create(model='Qwen3-8B',messages=[
            dict(role='system',content=system),dict(role='user',content=content)]).choices[0].message.content
    memory=CUPMemCandidateMemory(engine,lambda:[]) if args.strategy=='cupmem' else SourceOnlyMemory(engine)
    service=PracticalCUPMemService(memory,generate,args.store,strategy=args.strategy)
    for line in sys.stdin:
        if not line.strip():continue
        try:
            request=json.loads(line)
            with redirect_stdout(sys.stderr):
                result=service.handle(request)
        except (ValueError,TypeError,KeyError) as exc:
            result=dict(status='error',errors=[dict(type=type(exc).__name__,message=str(exc))])
        print(json.dumps(result,ensure_ascii=False),flush=True)


if __name__=='__main__':main()
