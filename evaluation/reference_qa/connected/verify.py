"""Replay actual model requests; verify frozen inputs, source IDs and offsets."""
from hashlib import sha256
import json
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT/'results/reference-qa/connected-v1'


def read(path):
    return json.loads(path.read_text())


def main():
    from team_memory.reference_connected import answer_from_sources, plan_sources, finish, expand_sources
    from team_memory.reference_joint import joint_template, format_joint
    from team_memory.reference_contextual import source_context
    from llama_index.core.llms import ChatMessage
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
    assert result['data_sha256']==read(package/'config.json')['data_sha256']
    calls = [json.loads(line) for line in (OUT/'calls.jsonl').read_text().splitlines()]
    assert len(calls)==result['calls']==80
    assert all(c['http_status']==200 for c in calls)
    assert len({c['id'] for c in calls})==80
    inputs = read(package/'inputs.json')
    cases = {c['id']:c for split in inputs.values() for c in split}
    plans = {p['id']:p['planning'] for p in result['plans']}
    retrieval = {r['id']:r for r in result['retrieval']}
    assert len(plans)==len(retrieval)==10 and len(result['rows'])==50
    consumed, spans = [], 0

    class Decoder:
        def __init__(self, identity):
            self.calls = [c for c in calls if c['context']==identity]
            self.position = 0

        def chat(self, messages):
            call = self.calls[self.position]
            assert call['request']['messages']==[dict(role=m.role.value, content=m.content) for m in messages]
            consumed.append(call['id']); self.position += 1
            return SimpleNamespace(message=SimpleNamespace(content=call['response']['choices'][0]['message']['content']))

        def done(self):
            assert self.position==len(self.calls)

    for case in inputs['ever']:
        decoder = Decoder(dict(split='ever', case_id=case['id'], arm='plan'))
        replay = plan_sources(case['question'], case['sources'], decoder)
        decoder.done(); assert replay==plans[case['id']]
        retrieved = retrieval[case['id']]
        assert retrieved['initial_sources']==case['sources']
        batches = iter(retrieved['searches'])
        def search(query):
            batch = next(batches)
            assert query==batch['query'] and len(batch['sources'])<=4
            return batch['sources']
        expanded, searches = expand_sources(case['sources'], replay, search)
        assert list(batches)==[] and expanded==retrieved['sources'] and searches==retrieved['searches']
        assert expanded[:len(case['sources'])]==case['sources'] and len(expanded)<=len(case['sources'])+8

    for row in result['rows']:
        identity = {k:row[k] for k in ['split','case_id','arm']}
        case = cases[row['case_id']]
        assert row['question']==case['question']
        decoder = Decoder(identity)
        if row['split']=='legacy':
            assert row['retrieval_sources']==case['sources']
            replay = answer_from_sources(case['question'], case['sources'], decoder)
        elif row['arm']=='joint':
            assert row['retrieval_sources']==case['sources']
            raw = decoder.chat([ChatMessage(role='user', content=joint_template().format(
                context_str=source_context(case['sources']), query_str=case['question']))]).message.content
            replay = format_joint(case['question'], raw, case['sources'])
        else:
            combined = row['arm']=='combined'
            expected = retrieval[case['id']]['sources'] if combined else case['sources']
            assert row['retrieval_sources']==expected
            replay = finish(case['question'], case['sources'], expected, plans[case['id']], decoder,
                retrieval[case['id']]['searches'] if combined else None)
        decoder.done()
        assert len(decoder.calls)==row['calls'] and replay==row['result'], identity
        for claim in replay.get('claims', []):
            for span in claim['quoted_spans']:
                assert any(w['source_id']==span['source_id'] and w['start']<=span['start']<span['end']<=w['end']
                    and w['quote'][span['start']-w['start']:span['end']-w['start']]==span['quote']
                    for w in row['retrieval_sources'])
                spans += 1
    assert len(consumed)==len(set(consumed))==80
    summary = dict(job_id=job['job_id'], state=job['state'], exit_code=job['exit_code'],
        fixed_hashes_verified=True, outputs_replayed=50, requests_replayed=80,
        spans_verified=spans, original_top8_preserved=10,
        finish_reasons={reason:sum(c['response']['choices'][0]['finish_reason']==reason for c in calls)
            for reason in sorted({c['response']['choices'][0]['finish_reason'] for c in calls})},
        prompt_tokens=sum(c['response']['usage']['prompt_tokens'] for c in calls),
        completion_tokens=sum(c['response']['usage']['completion_tokens'] for c in calls),
        gpu_minutes=job['elapsed_seconds']*job['gpus']/60, external_model_calls=0)
    (OUT/'verification.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary))


if __name__=='__main__':
    main()
