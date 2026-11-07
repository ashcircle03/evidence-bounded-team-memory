"""Local deterministic quote-offset replay, using byte-identical actual prompts.

No model, embeddings, retrieval, GPU job, or external service is executed.
"""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from types import SimpleNamespace
from team_memory.reference_qa import format_response
from team_memory.reference_quotes import add_quote_citations


def main():
    repo=Path(__file__).resolve().parents[2]
    prior=repo/'results/reference-qa/quote-v2';out=repo/'results/reference-qa/quote-normalized-v1'
    freeze=json.loads((out/'freeze.json').read_text())
    for n,h in freeze['parent_sha256'].items():assert sha256((prior/n).read_bytes()).hexdigest()==h
    for n,h in freeze['runtime_sha256'].items():assert sha256((repo/n).read_bytes()).hexdigest()==h
    record=json.loads((prior/'result.json').read_text())
    calls=[json.loads(l) for l in (prior/'calls.jsonl').read_text().splitlines()]
    new_calls=calls[-14:];used=[]
    for row in record['rows']:
        for step in row['steps']:
            if step['label']=='import':continue
            context=dict(case_id=row['case_id'],label=step['label'])
            before=deepcopy(step['result']);raw=before.pop('pre_citation_raw',before['raw'])
            question=before['alce']['question']
            for key in ['posthoc_citations','quote_attribution_raw','quote_citation_reviews',
                        'quote_attribution_error','citation_method','citation_entailment_verified',
                        'unattributed_sentences','attribution_status']:
                before.pop(key,None)
            before.update(format_response(question,raw,before['citation_sources'],allow_source_labels=True))
            class Replay:
                def chat(self,messages):
                    physical=[c for c in new_calls if c['context']==context]
                    assert len(physical)==1
                    call=physical[0]
                    actual=[dict(role=m.role.value,content=m.content) for m in messages]
                    assert actual==call['request']['messages']
                    assert call['id'] not in used;used.append(call['id'])
                    return SimpleNamespace(message=SimpleNamespace(content=call['response']['choices'][0]['message']['content']))
            step['result']=add_quote_citations(question,before,Replay())
            step['new_physical_calls']=0
            step['answer_text_unchanged']=step['result']['raw']==before['raw']
    assert used==[c['id'] for c in new_calls]
    record.update(execution_kind='local deterministic offset replay',source_version='local-quote-normalized-v1',
        replay_from_job_id='119960',new_physical_calls=0,reused_physical_calls=len(calls),
        code_sha256=freeze['runtime_sha256'],original_inference_seconds=record['seconds'],
        scope='Same132 physical calls; only whitespace-tolerant quote offsets changed; all14 quote prompts exactly equal actual model inputs')
    (out/'result.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
    (out/'calls.jsonl').write_bytes((prior/'calls.jsonl').read_bytes())
    (out/'replay-verification.json').write_text(json.dumps(dict(actual_prompt_matches=len(used),used_call_ids=used,additional_model_calls=0,additional_gpu_minutes=0),indent=2)+'\n')


if __name__=='__main__':main()
