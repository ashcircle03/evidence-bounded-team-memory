"""Four live answer.generate requests with fixed evidence; executed on a Slurm GPU node."""
import hashlib
import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory

import httpx
from llama_index.core.embeddings import MockEmbedding
from llama_index.llms.openai_like import OpenAILike
from transformers import AutoTokenizer

from team_memory.adapters.answering import AnsweringAdapter
from team_memory.adapters.base import request
from team_memory.contracts.ports import CallContext
from team_memory.readers.attribution import AttributedQA


def main(reader_types=None):
    reader_types = reader_types or {'scoped': AttributedQA}
    packet = Path(os.environ['READER_PACKET'])
    cfg = json.loads((packet/'config.json').read_text())
    panel = Path(os.environ['RECORD_INPUTS']).read_bytes()
    assert hashlib.sha256(panel).hexdigest() == cfg['input_sha256']
    assert hashlib.sha256((packet/'code.tar.gz').read_bytes()).hexdigest() == cfg['code_digest']
    assert Path(__import__('team_memory.adapters.answering', fromlist=['']).__file__).resolve().is_relative_to(packet/'code')
    tokenizer = AutoTokenizer.from_pretrained(cfg['model_shared'],local_files_only=True)
    job = os.environ['SLURM_JOB_ID']
    dest = Path(cfg['project'])/'results'/f'versions-{job}.json'
    assert not dest.exists()
    rows = []
    calls = []
    def capture(response):
        response.read()
        response.raise_for_status()
        body = response.json()
        calls.append(dict(request=json.loads(response.request.content), model=body['model'], choices=body['choices'], usage=body['usage']))
    with httpx.Client(trust_env=False, event_hooks={'response':[capture]}) as client, TemporaryDirectory() as work:
        llm = OpenAILike(model='Qwen3-8B',api_base=os.environ['PRACTICAL_MODEL_URL'],api_key='local',
            is_chat_model=True,is_function_calling_model=False,context_window=32768,max_tokens=1024,
            tokenizer=tokenizer,temperature=0,timeout=90,max_retries=0,http_client=client,
            additional_kwargs={'extra_body':{'chat_template_kwargs':{'enable_thinking':False}}})
        for index, item in enumerate(json.loads(panel)):
            arms = list(reader_types.items())
            if index % 2:
                arms.reverse()
            for arm, reader_type in arms:
                def factory(store):
                    return reader_type(store,llm=llm,embed_model=MockEmbedding(embed_dim=8),tokenizer=tokenizer,
                                       context_window=32768,num_output=1024)
                bundle = item['bundle']
                snap = bundle['snapshot']
                port = AnsweringAdapter('versions',factory,Path(work)/arm/item['id'],snapshot_loader=lambda sid:snap if snap['id']==sid else None)
                calls.clear()
                response = port.handle(request('answer.generate',dict(bundle=bundle),workspace_id='versions',request_id=item['id']),
                                       context=CallContext('versions','eval',frozenset(['answer:generate'])))
                rows.append(dict(id=item['id'],arm=arm,response=response,calls=list(calls),
                                 diagnostics=list(port.diagnostics.load('answer_diagnostics').values())))
        dest.write_text(json.dumps(dict(status='complete',job=job,model_revision=cfg['model_revision'],
                                       input_sha256=cfg['input_sha256'],code_digest=cfg['code_digest'],rows=rows),ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
