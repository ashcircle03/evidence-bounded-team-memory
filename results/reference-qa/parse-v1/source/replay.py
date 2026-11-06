"""Replay all20 frozen drafts/judgments after a format-only parser repair.

Reuse a previous revision only if its complete model input is byte-equivalent.
Only newly reachable revision inputs call Qwen. Gold answers are never loaded.
"""
from copy import deepcopy
from hashlib import sha256
import json
import os
from pathlib import Path
import sys
import time


def main():
    folder=Path(sys.argv[1]);cfg=json.loads((folder/'config.json').read_text())
    job=os.environ['SLURM_JOB_ID'];assert os.environ['SLURMD_NODENAME']
    assert os.environ['CONDA_PREFIX']==cfg['conda_prefix']
    sys.path.insert(0,str(folder/'code'))
    for name,h in cfg['code_sha256'].items():assert sha256((folder/'code'/name).read_bytes()).hexdigest()==h
    for name,h in cfg['replay_files_sha256'].items():assert sha256((folder/name).read_bytes()).hexdigest()==h
    assert sha256((folder/'inputs.json').read_bytes()).hexdigest()==cfg['input_sha256']
    import httpx
    from transformers import AutoTokenizer
    from llama_index.llms.openai_like import OpenAILike
    from team_memory.reference_checked import parse_judgment,review_messages
    from team_memory.reference_qa import format_response,guard_request
    previous=json.loads((folder/'prior-result.json').read_text())
    old_calls=[json.loads(l) for l in (folder/'prior-calls.jsonl').read_text().splitlines()]
    inputs=json.loads((folder/'inputs.json').read_text())
    questions={(c['id'],e['label']):e['question'] for c in inputs['cases'] for e in c['events'] if e['operation']=='ask'}
    assert len(questions)==20 and previous['status']=='complete'
    record=deepcopy(previous)
    record.update(status='running',job_id=job,source_version=cfg['source_version'],
        code_sha256=cfg['code_sha256'],replay_from_job_id=previous['job_id'],
        scope='All20 exact-output replay; existing physical calls reused, newly reachable revisions use same Qwen',
        reused_physical_calls=len(old_calls),new_physical_calls=0,previous_seconds=previous['seconds'],
        replay_files_sha256=cfg['replay_files_sha256'])
    output=Path(cfg['project'])/'results'/f'cup-reference-{job}.json'
    calls_file=output.with_suffix('.calls.jsonl').open('x')
    for call in old_calls:
        calls_file.write(json.dumps(dict(call,replayed_from_job_id=previous['job_id']),ensure_ascii=False)+'\n')
    calls_file.flush();context={};began=time.monotonic()
    tokenizer=AutoTokenizer.from_pretrained(cfg['model_path'],local_files_only=True)

    def save():
        record['seconds']=time.monotonic()-began
        tmp=output.with_suffix('.tmp');tmp.write_text(json.dumps(record,ensure_ascii=False,indent=2));tmp.replace(output)

    def request_hook(request):
        if not request.url.path.endswith('/chat/completions'):return
        if record['new_physical_calls']>=cfg['max_new_calls']:raise RuntimeError('New-call limit reached')
        body=json.loads(request.content)
        trace=dict(id=record['calls'],context=dict(context),request=body,started=time.monotonic(),
            rendered_prompt_tokens=len(tokenizer.apply_chat_template(body['messages'],tokenize=True,
                add_generation_prompt=True,enable_thinking=False)))
        request.extensions['reference_trace']=trace
        record['calls']+=1;record['new_physical_calls']+=1

    def response_hook(response):
        response.read();trace=response.request.extensions.get('reference_trace')
        if trace:
            calls_file.write(json.dumps(dict(trace,response=response.json(),http_status=response.status_code,
                seconds=time.monotonic()-trace['started']),ensure_ascii=False)+'\n');calls_file.flush()

    save()
    with httpx.Client(trust_env=False,event_hooks={'request':[guard_request(tokenizer),request_hook],
                                                 'response':[response_hook]}) as client:
        llm=OpenAILike(model='Qwen3-8B',api_base=os.environ['PRACTICAL_MODEL_URL'],api_key='local-no-secret',
            is_chat_model=True,is_function_calling_model=False,context_window=32768,max_tokens=1024,
            tokenizer=tokenizer,temperature=0,timeout=90,max_retries=0,http_client=client,
            additional_kwargs={'extra_body':{'chat_template_kwargs':{'enable_thinking':False}}})
        try:
            for row in record['rows']:
                for step in row['steps']:
                    if step['label']=='import':continue
                    start=time.monotonic();context.clear();context.update(case_id=row['case_id'],label=step['label'])
                    question=questions[row['case_id'],step['label']]
                    original=step['result'];witnesses=original['citation_sources']
                    judgments=[dict(j,label=parse_judgment(j['raw'])) for j in original['document_judgments']]
                    result=format_response(question,original['draft_raw'],witnesses,allow_source_labels=True)
                    revised=any(j['label']=='CONTRADICTS' for j in judgments)
                    new_calls_before=record['new_physical_calls'];reused_revision=False
                    if revised:
                        messages=review_messages(question,original['draft_raw'],witnesses,judgments)
                        plain=[dict(role=m.role.value,content=m.content) for m in messages]
                        matches=[c for c in old_calls if c['context']==context and c['request']['messages']==plain]
                        if matches:
                            call=matches[-1]
                            assert call['request']['model']=='Qwen3-8B' and call['request']['max_tokens']==1024
                            assert call['request']['temperature']==0
                            raw=call['response']['choices'][0]['message']['content'];reused_revision=True
                        else:
                            raw=llm.chat(messages).message.content
                        result=format_response(question,raw,witnesses,allow_source_labels=True)
                    result.update(draft_raw=original['draft_raw'],document_judgments=judgments,revised=revised)
                    if any(j['label']=='ERROR' for j in judgments):
                        result['warnings'].append('Conflict review incomplete: document judge parse or transport failure')
                        result['status']='partial'
                    step.update(result=result,previous_seconds=step['seconds'],seconds=time.monotonic()-start,
                        new_physical_calls=record['new_physical_calls']-new_calls_before,
                        answer_text_unchanged=result['raw']==original['raw'],reused_revision_input=reused_revision)
                    step['calls']+=step['new_physical_calls']
                    save();print('REPLAY_STEP',row['case_id'],step['label'],result['status'],step['new_physical_calls'],flush=True)
            assert record['new_physical_calls']==cfg['expected_new_calls']
            record['status']='complete'
        finally:
            save();calls_file.close()


if __name__=='__main__':main()
