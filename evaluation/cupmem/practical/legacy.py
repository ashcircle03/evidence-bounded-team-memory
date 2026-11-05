"""Project the exact historical20 QA cases, with full corpora, into paired events."""
from hashlib import sha256
import json
from pathlib import Path

from team_memory.store import digest, source_envelope
from .prepare import write


HERE = Path(__file__).resolve().parent


def build():
    raw = (HERE.parent/'legacy-inputs.json').read_bytes()
    manifest = json.loads((HERE.parent/'legacy-inputs-manifest.json').read_text())
    assert sha256(raw).hexdigest() == manifest['sha256']
    source = json.loads(raw)
    assert len(source['cases']) == 20
    data = dict(scope='Exact historical20 source-collection QA regression; mixed corpus, not native chronological STALE', cases=[])
    key = dict(audience='evaluator_only', source_sha256=manifest['sha256'], cases={}, original_case_count=20)
    for history_id, history in source['histories'].items():
        name = 'legacy-'+history_id[:16]
        documents = [source_envelope(source['documents'][sid]) for sid in history['historical_source_ids']]
        assert [digest(e) for e in documents] == history['historical_source_ids']
        events = [dict(label='import',operation='import_history',records=documents)]
        mapping = {}
        for i, case in enumerate(c for c in source['cases'] if c['history_id']==history_id):
            label = 'qa-'+str(i)
            question = json.dumps(dict(question=case['question'],as_of=case['as_of']),
                                  ensure_ascii=False,sort_keys=True,separators=(',',':'))
            events.append(dict(label=label,operation='ask',question=question,temporal_scope='historical'))
            mapping[label] = dict(original_id=case['id'],question=case['question'],as_of=case['as_of'],
                                 **source['evaluation_only'][case['id']])
        data['cases'].append(dict(id=name,events=events))
        key['cases'][name] = dict(history_id=history_id,source_ids=history['historical_source_ids'],questions=mapping)
    assert sum(len(c['events'])-1 for c in data['cases'])==20
    write(HERE/'legacy.json',data);write(HERE/'legacy-key.json',key)
    provenance=dict(actor_sha256=sha256((HERE/'legacy.json').read_bytes()).hexdigest(),
        key_sha256=sha256((HERE/'legacy-key.json').read_bytes()).hexdigest(),
        original_input_sha256=manifest['sha256'], histories=len(data['cases']), questions=20,
        source_arrivals=sum(len(c['events'][0]['records']) for c in data['cases']),
        unfiltered_originals=True, original_order_preserved=True,
        adaptation='Explicit native multi-turn bulk import of source collections, no generated review during import; one original question/as_of envelope per QA',
        scorer='Frozen original aliases/locations plus manual answer-to-quote entailment; partial formatting warnings alone do not erase a correct answer',
        provenance_not_performance='Earlier3B acceptance is selection history, never a newQwen result')
    write(HERE/'legacy-manifest.json',provenance)
    return provenance


if __name__=='__main__': print(json.dumps(build(),indent=2))
