"""Verify frozen files, actual reader requests, source offsets and paired inputs."""
from hashlib import sha256
import json
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT/'results/reference-qa/contextual-v1'


def read(path):
    return json.loads(path.read_text())


def main():
    from team_memory.reference_claims import answer_from_sources as claims_reader
    from team_memory.reference_contextual import answer_from_sources as contextual_reader
    freeze = read(OUT/'freeze.json')
    campaign = ROOT.parent/'campaigns/speakermem-dev'
    package = campaign/'source'/freeze['version']
    for base, hashes in [(ROOT, freeze['actor']), (package, freeze['files'])]:
        for name, expected in hashes.items():
            assert sha256((base/name).read_bytes()).hexdigest() == expected, name
    result = read(OUT/'result.json')
    job = read(campaign/'campaign-dispatch.json')['jobs'][freeze['version']]
    assert job['state']=='COMPLETED' and job['exit_code']=='0:0' and job['verified']
    assert result['status']=='complete' and result['job_id']==job['job_id']
    assert result['code_sha256']==freeze['actor']
    config = read(package/'config.json')
    assert result['data_sha256']==config['data_sha256']
    calls = [json.loads(line) for line in (OUT/'calls.jsonl').read_text().splitlines()]
    assert len(calls)==result['calls']<=config['max_calls']
    assert len({call['id'] for call in calls})==len(calls)
    assert all(call['http_status']==200 for call in calls)
    inputs = read(package/'inputs.json')
    cases = {c['id']:c for split in inputs.values() for c in split}
    retrievals = {item['id']:item for item in result['retrieval']}
    rows = {(row['case_id'],row['arm']):row for row in result['rows']}
    assert len(rows)==len(result['rows'])==50 and len(retrievals)==10
    replayed, spans = [], 0
    for row in result['rows']:
        identity = {key:row[key] for key in ['split','case_id','arm']}
        physical = [call for call in calls if call['context']==identity]
        position = 0

        class Decoder:
            def chat(self, messages):
                nonlocal position
                call = physical[position]
                actual = [dict(role=m.role.value,content=m.content) for m in messages]
                assert call['request']['messages']==actual, identity
                position += 1
                replayed.append(call['id'])
                return SimpleNamespace(message=SimpleNamespace(
                    content=call['response']['choices'][0]['message']['content']))

        reader = claims_reader if row['arm']=='retrieval_only' else contextual_reader
        replay = reader(row['question'],row['retrieval_sources'],Decoder())
        assert position==len(physical)==row['calls']
        assert replay==row['result'], identity
        case = cases[row['case_id']]
        assert row['question']==case['question']
        if row['arm'] in ['reader_only','contextual']:
            assert row['retrieval_sources']==case['sources']
        else:
            assert row['retrieval_sources']==retrievals[row['case_id']]['sources']
        for claim in replay.get('claims',[]):
            for span in claim.get('quoted_spans',claim.get('evidence',[])):
                assert any(source['source_id']==span['source_id'] and
                    source['start']<=span['start']<span['end']<=source['end'] and
                    source['quote'][span['start']-source['start']:span['end']-source['start']]==span['quote']
                    for source in row['retrieval_sources'])
                spans += 1
    query_calls = []
    for case in inputs['ever']:
        item = retrievals[case['id']]
        assert item['trace']['initial_sources']==case['sources']
        assert item['trace']['initial_query']==case['query']
        physical = [c for c in calls if c['context']==dict(split='ever',case_id=case['id'],arm='retrieval')]
        assert len(physical)==1
        # OpenAILike.complete wraps the prompt as one user message.
        assert physical[0]['request']['messages']==[dict(role='user',content=item['trace']['query_generation_prompt'])]
        query_calls.append(physical[0]['id'])
    assert set(replayed+query_calls)=={c['id'] for c in calls}
    summary = dict(job_id=job['job_id'],state=job['state'],exit_code=job['exit_code'],
        fixed_hashes_verified=True,reader_outputs_replayed=len(rows),
        reader_calls_replayed=len(replayed),query_calls_verified=len(query_calls),
        literal_spans_verified=spans,original_top8_reproduced=10,
        finish_reasons={reason:sum(c['response']['choices'][0]['finish_reason']==reason for c in calls)
                        for reason in sorted({c['response']['choices'][0]['finish_reason'] for c in calls})},
        prompt_tokens=sum(c['response']['usage']['prompt_tokens'] for c in calls),
        completion_tokens=sum(c['response']['usage']['completion_tokens'] for c in calls),
        external_model_calls=result['external_model_api_calls'],
        gpu_minutes=job['elapsed_seconds']*job['gpus']/60)
    (OUT/'verification.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary))


if __name__=='__main__':
    main()
