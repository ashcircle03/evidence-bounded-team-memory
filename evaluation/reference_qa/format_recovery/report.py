"""Score changed reader outputs against the prior evaluation and verify the run."""
import json
from collections import defaultdict
from hashlib import sha256
from pathlib import Path

from .replay import OUT, PRIOR, ROOT, write


def read(path):
    return json.loads(path.read_text())


def check_hashes(root, expected):
    for name, digest in expected.items():
        assert sha256((root / name).read_bytes()).hexdigest() == digest, name


def metrics(ids, ratings):
    return {
        'n': len(ids),
        'answer': sum(ratings[key]['answer_correct'] for key in ids),
        'supported': sum(ratings[key]['success'] for key in ids),
    }


def main():
    freeze = read(OUT / 'freeze.json')
    check_hashes(ROOT, freeze['actor'])
    check_hashes(PRIOR, freeze['prior'])
    outputs = read(OUT / 'outputs.json')
    before = read(PRIOR / 'ratings-by-id.json')
    cards = read(PRIOR / 'cards.json')
    changed = read(OUT / 'reviewed-deltas.json')
    identical = {key for key in cards if cards[key]['result'] == outputs[key]}
    assert set(outputs) == set(cards) == set(before)
    assert set(changed) == set(outputs) - identical
    groups = defaultdict(list)
    for key, card in cards.items():
        groups[card['split'] + '/' + card['arm']].append(key)
        if card['split'] == 'wiki':
            condition = card['case_id'].split('/')[-1]
            groups['wiki-' + condition + '/' + card['arm']].append(key)
    for key, review in changed.items():
        assert review['reason'] and len(review['claim_reviews']) == len(outputs[key]['claims'])
        review['success'] = (review['answer_correct'] and review['required_evidence_complete']
                             and review['returned_evidence_supports_all_claims'] and not review['unsupported_extra'])
    after = {**before, **changed}
    fresh = read(OUT / 'fresh.json')
    campaign = ROOT.parent / 'campaigns/speakermem-dev'
    package = campaign / 'source' / freeze['version']
    check_hashes(package, freeze['files'])
    assert read(package / 'config.json')['input_hashes'] == fresh['input_hashes']
    job = read(campaign / 'campaign-dispatch.json')['jobs'][freeze['version']]
    assert job['state'] == 'COMPLETED' and job['exit_code'] == '0:0' and job['verified']
    assert job['job_id'] == fresh['job_id'] and fresh['status'] == 'complete'
    calls = fresh['calls']
    assert len(calls) == freeze['expected_new_calls']
    assert all(call['response']['choices'][0]['finish_reason'] == 'stop' for call in calls)
    summary = dict(
        job_id=job['job_id'], state=job['state'], exit_code=job['exit_code'],
        fresh_Qwen_calls=len(calls), external_model_calls=fresh['external_model_api_calls'],
        gpu_minutes=job['elapsed_seconds']*job['gpus']/60,
        prompt_tokens=sum(c['response']['usage']['prompt_tokens'] for c in calls),
        completion_tokens=sum(c['response']['usage']['completion_tokens'] for c in calls),
        evaluated_outputs=len(cards), identical_whole_outputs=len(identical),
        previously_supported=sum(v['success'] for v in before.values()),
        preserved=sum(v['success'] and after[k]['success'] for k,v in before.items()),
        recovered=[k for k,v in before.items() if not v['success'] and after[k]['success']],
        lost=[k for k,v in before.items() if v['success'] and not after[k]['success']],
        groups={name:dict(before=metrics(ids,before),after=metrics(ids,after)) for name,ids in groups.items()},
        fixed_hashes_verified=True, independent_human=False,
    )
    write(OUT / 'summary.json', summary)
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
