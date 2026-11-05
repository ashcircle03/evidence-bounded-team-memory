"""Source-only actor streams for all20 frozen legacy questions.

Identical full histories share one fresh CUP ingestion; their independent
questions may read, but must never mutate, that memory. Historical source order
is preserved. This is an explicit source-collection adapter, not chronological
STALE: query text carries the original question AND its original as_of value.
No gold aliases, old answers, condition labels or review scripts enter actors.
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path

from .audit import digest
from .transfer_inputs import envelope_only
from team_memory.store import digest as source_id


def build(data, *, input_sha256):
    if len(data['cases']) != 20 or data['provenance']['canonical_order'] != 'historical':
        raise ValueError('Require all20 original legacy questions in canonical source order')
    actors, mapping = [], {}
    counts = Counter(case['history_id'] for case in data['cases'])
    for history_id in sorted(counts):
        history = data['histories'][history_id]
        cid = digest(dict(adapter='cupmem-legacy-actor-v1', history_id=history_id))[:24]
        events, queries = [], {}
        for index, sid in enumerate(history['historical_source_ids']):
            env = envelope_only(deepcopy(data['documents'][sid]))
            if source_id(env) != sid:
                raise ValueError('Legacy source ID does not bind its exact envelope')
            events.append(dict(op='ingest', event_id=digest([cid, 'ingest', index])[:24], source=env))
        for case in [case for case in data['cases'] if case['history_id'] == history_id]:
            eid = digest([cid, 'ask', case['id']])[:24]
            # CUP's public answer_query accepts one query_text. Preserve both
            # original query fields in an explicit JSON envelope for BOTH arms.
            question = json.dumps(dict(question=case['question'], as_of=case['as_of']),
                                  ensure_ascii=False, sort_keys=True, separators=(',', ':'))
            events.append(dict(op='ask', event_id=eid, question=question))
            queries[eid] = dict(legacy_case_id=case['id'], original_question=case['question'],
                               original_as_of=case['as_of'], model_query_sha256=digest(question))
        actors.append(dict(case_id=cid, events=events))
        mapping[cid] = dict(history_id=history_id, queries=queries,
                           original_source_ids=history['historical_source_ids'])
    if len(mapping) != len(counts) or sum(len(m['queries']) for m in mapping.values()) != 20:
        raise ValueError('Lost a legacy history or question')
    actor = dict(schema='cupmem-legacy-actor-v1', cases=actors)
    return actor, dict(schema='cupmem-legacy-actor-evaluator-manifest-v1', audience='evaluator_only',
                       source_artifact_sha256=input_sha256, actor_sha256=digest(actor), mapping=mapping,
                       counts=dict(histories=len(actors), questions=20,
                                   source_arrivals=sum(len(m['original_source_ids']) for m in mapping.values())),
                       adaptation='one attributed source per session in historical source collection order; query_text is original question/as_of JSON; not native STALE chronology',
                       reuse='only byte-identical complete histories share ingestion; no private state restore or prefix branch reuse')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('input_manifest', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('output_manifest', type=Path)
    args = parser.parse_args()
    raw = args.input.read_bytes()
    fingerprint = hashlib.sha256(raw).hexdigest()
    if fingerprint != json.loads(args.input_manifest.read_text())['sha256']:
        raise ValueError('Frozen legacy source artifact changed')
    actor, manifest = build(json.loads(raw), input_sha256=fingerprint)
    args.output.write_text(json.dumps(actor, ensure_ascii=False, indent=2) + '\n')
    manifest['actor_file_sha256'] = hashlib.sha256(args.output.read_bytes()).hexdigest()
    args.output_manifest.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(manifest['counts']))
