"""Diagnostic replay after original verifier stopped on non-stop completion.
Original frozen verifier and scoring remain unchanged; non-stop failures retained.
"""
"""Replay exact model messages and original document bindings, not correctness."""
from hashlib import sha256
import json
from pathlib import Path
from types import SimpleNamespace

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'results/reference-qa/documents-v1'


def read(path): return json.loads(path.read_text())


def main():
    from team_memory.reference_documents import answer_from_sources
    freeze=read(OUT/'freeze.json')
    campaign=ROOT.parent/'campaigns/speakermem-dev'
    package=campaign/'source'/freeze['version']
    for base, hashes in [(ROOT,freeze['actor']),(package,freeze['files'])]:
        for name,expected in hashes.items():
            assert sha256((base/name).read_bytes()).hexdigest()==expected,name
    job=read(campaign/'campaign-dispatch.json')['jobs'][freeze['version']]
    assert job['state']=='COMPLETED' and job['exit_code']=='0:0' and job['verified']
    result=read(OUT/'result.json'); retrieval=read(OUT/'retrieval.json')
    assert result['status']==retrieval['status']=='complete'
    assert result['job_id']==retrieval['job_id']==job['job_id']
    assert result['code_sha256']==retrieval['code_sha256']==freeze['actor']
    assert result['data_sha256']==retrieval['data_sha256']==read(package/'config.json')['data_sha256']
    assert result['retrieval_sha256']==sha256((OUT/'retrieval.json').read_bytes()).hexdigest()
    assert result['retrieval']==retrieval['retrieval']
    calls=[json.loads(line) for line in (OUT/'calls.jsonl').read_text().splitlines()]
    assert len(calls)==result['calls']==len(result['rows'])==80
    assert all(c['http_status']==200 for c in calls)
    finish_failures=[c['context'] for c in calls if c['response']['choices'][0]['finish_reason']!='stop']
    inputs=read(package/'inputs.json'); cases={c['id']:c for split in inputs.values() for c in split}
    retrieved={r['id']:r for r in result['retrieval']}
    expected={(split,c['id'],a) for split,cs in inputs.items() for c in cs
        for a in (('direct','con') if split=='legacy' else ('bm25_direct','bm25_con','dense_direct','dense_con'))}
    assert {(r['split'],r['case_id'],r['arm']) for r in result['rows']}==expected
    consumed=set(); bound=0
    for row in result['rows']:
        identity={k:row[k] for k in ['split','case_id','arm']}
        call=[c for c in calls if c['context']==identity]
        assert len(call)==row['calls']==1
        call=call[0]; assert call['id'] not in consumed; consumed.add(call['id'])
        case=cases[row['case_id']]
        assert row['question']==case['question']
        witnesses=case['sources'] if row['split']=='legacy' or row['arm'].startswith('bm25') else retrieved[case['id']]['sources']
        assert witnesses==row['retrieval_sources']
        if row['split']=='ever': assert retrieved[case['id']]['initial_sources']==case['sources']
        class Decoder:
            def chat(self,messages):
                assert call['request']['messages']==[dict(role=m.role.value,content=m.content) for m in messages]
                return SimpleNamespace(message=SimpleNamespace(content=call['response']['choices'][0]['message']['content']))
        replay=answer_from_sources(case['question'],witnesses,Decoder(),reading=row['arm'].split('_')[-1])
        assert replay==row['result'],identity
        for claim,answer in zip(replay['claims'],replay['answers']):
            assert answer['evidence']==claim['evidence']==[witnesses[n-1] for n in claim['source_numbers']]
            bound+=len(answer['evidence'])
    summary=dict(job_id=job['job_id'],state=job['state'],exit_code=job['exit_code'],
        fixed_hashes_verified=True,original_all_stop_check_passed=not finish_failures,non_stop_calls=finish_failures,requests_replayed=80,outputs_replayed=80,source_bindings_verified=bound,
        original_top8_preserved=10,prompt_tokens=sum(c['response']['usage']['prompt_tokens'] for c in calls),
        completion_tokens=sum(c['response']['usage']['completion_tokens'] for c in calls),
        gpu_minutes=job['elapsed_seconds']*job['gpus']/60,external_model_calls=0)
    (OUT/'verification.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))


if __name__=='__main__': main()
