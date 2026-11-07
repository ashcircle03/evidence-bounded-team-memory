"""Replay identical requests. Collect only previously unseen fusion inputs."""
from hashlib import sha256
import json
from pathlib import Path
from types import SimpleNamespace

from team_memory.reference_claims import answer_from_sources
from team_memory.reference_joint import format_joint


ROOT = Path(__file__).resolve().parents[3]
PRIOR = ROOT / 'results/reference-qa/claims-v3'
OUT = ROOT / 'results/reference-qa/format-recovery-v1'


def key(messages):
    return sha256(json.dumps(messages, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')


class MissingFusion(BaseException):
    """Escape the reader's ordinary model-failure fallback only during planning."""


def replay(fresh=None):
    original = json.loads((PRIOR/'result.json').read_text())
    traces = [json.loads(line) for line in (PRIOR/'calls.jsonl').read_text().splitlines()]
    by_case = {}
    for call in traces:
        ctx = call['context']
        by_case.setdefault((ctx['split'],ctx['case_id'],ctx['arm']),[]).append(call)
    pending, results = [], {}
    for row in original['rows']:
        identity = tuple(row[k] for k in ('split','case_id','arm'))
        name = '/'.join(identity)
        calls = by_case[identity]
        prior = {key(c['request']['messages']): c for c in calls}
        count = 0
        class Decoder:
            def chat(self, messages):
                nonlocal count
                count += 1
                actual = [dict(role=m.role.value,content=m.content) for m in messages]
                fingerprint = key(actual)
                if fingerprint in prior:
                    call = prior[fingerprint]
                    assert call['request']['messages'] == actual
                    content = call['response']['choices'][0]['message']['content']
                else:
                    assert count==2, 'Selection prompt changed'
                    if fresh is None:
                        body = dict(calls[0]['request'],messages=actual)
                        pending.append(dict(id=name,key=fingerprint,body=body))
                        raise MissingFusion
                    call = fresh[name]
                    assert call['request']==dict(calls[0]['request'], messages=actual)
                    assert call['key']==fingerprint and call['http_status']==200
                    content = call['response']['choices'][0]['message']['content']
                return SimpleNamespace(message=SimpleNamespace(content=content))
        witnesses=row['retrieval_sources']
        try:
            if row['arm']=='joint':
                raw=calls[0]['response']['choices'][0]['message']['content']
                assert row['result']['generation_raw']==raw
                result=format_joint(row['question'],raw,witnesses)
            else:
                result=answer_from_sources(row['question'],witnesses,Decoder())
        except MissingFusion:
            continue
        for claim in result.get('claims',[]):
            for q in claim.get('evidence',claim.get('quoted_spans',[])):
                assert any(w['source_id']==q['source_id'] and w['start']<=q['start']<q['end']<=w['end'] and
                           w['quote'][q['start']-w['start']:q['end']-w['start']]==q['quote'] for w in witnesses)
        results[name]=result
    return pending,results


if __name__=='__main__':
    path=OUT/'fresh.json'
    if path.exists():
        calls=json.loads(path.read_text())['calls']
        planned=json.loads((OUT/'requests.json').read_text())
        assert {r['id'] for r in planned}=={r['id'] for r in calls} and len(calls)==len(planned)
        pending,results=replay({c['id']:c for c in calls})
        assert not pending and len(results)==104
        write(OUT/'outputs.json',results)
    else:
        pending,results=replay()
        write(OUT/'requests.json',pending)
        print('New fusion requests',len(pending),[r['id'] for r in pending],'offline results',len(results))
