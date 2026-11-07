"""Exact request/output replay and source binding, not semantic grading."""
from hashlib import sha256
import json
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT/'results/reference-qa/demonstrated-v1'


def read(path):
    return json.loads(path.read_text())


def main():
    from team_memory.reference_demonstrated import answer_from_sources, select, generate, retrieve, direct
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
    assert 80 <= len(calls)==result['calls'] <= 100
    assert all(c['http_status']==200 for c in calls)
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
        decoder = Decoder(dict(split='ever', case_id=case['id'], arm='select'))
        replay = select(case['question'], case['sources'], decoder)
        decoder.done(); assert replay==plans[case['id']]
        retrieved = retrieval[case['id']]
        assert retrieved['initial_sources']==case['sources']
        decoder = Decoder(dict(split='ever', case_id=case['id'], arm='retrieve'))
        batches = iter([batch for round_ in retrieved['searches'] for batch in round_['searches']])
        def search(query):
            batch = next(batches)
            assert query==batch['query'] and len(batch['sources'])<=4
            return batch['sources']
        expanded, final, trace = retrieve(case['question'], case['sources'], replay, decoder, search)
        decoder.done()
        assert list(batches)==[] and expanded==retrieved['sources'] and trace==retrieved['searches']
        assert final==retrieved['final_selection']
        assert expanded[:len(case['sources'])]==case['sources'] and len(expanded)<=len(case['sources'])+16

    for row in result['rows']:
        identity = {k:row[k] for k in ['split','case_id','arm']}
        case = cases[row['case_id']]
        assert row['question']==case['question']
        decoder = Decoder(identity)
        if row['split']=='legacy':
            assert row['retrieval_sources']==case['sources']
            replay = answer_from_sources(case['question'], case['sources'], decoder)
        elif row['arm']=='direct':
            assert row['retrieval_sources']==case['sources']
            replay = direct(case['question'], case['sources'], decoder)
        else:
            combined = row['arm']=='combined'
            expected = retrieval[case['id']]['sources'] if combined else case['sources']
            selected = retrieval[case['id']]['final_selection'] if combined else plans[case['id']]
            assert row['retrieval_sources']==expected
            replay = generate(case['question'], expected, selected, decoder)
        decoder.done()
        assert len(decoder.calls)==row['calls'] and replay==row['result'], identity
        for claim in replay.get('claims', []):
            for span in claim['quoted_spans']:
                assert any(w['source_id']==span['source_id'] and w['start']<=span['start']<span['end']<=w['end']
                    and w['quote'][span['start']-w['start']:span['end']-w['start']]==span['quote']
                    for w in row['retrieval_sources'])
                spans += 1
    assert len(consumed)==len(set(consumed))==len(calls)
    summary = dict(job_id=job['job_id'], state=job['state'], exit_code=job['exit_code'],
        fixed_hashes_verified=True, outputs_replayed=50, requests_replayed=len(calls),
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
