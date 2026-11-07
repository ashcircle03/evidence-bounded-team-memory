"""Offline audit counterexamples; no model, network, or production-store writes.

Run from repository root: PYTHONPATH=. .venv/bin/python results/audit-2026-11-07/probes.py
These diagnose boundaries, not model accuracy. All stores are temporary.
"""
import json
import shutil
import tempfile
from pathlib import Path
from types import SimpleNamespace

from team_memory.store import source_envelope
from team_memory.reference_documents import documents
from team_memory.reference_qa import ReferenceQA, format_response
from team_memory.reference_attributed import repair_omitted_answer
from team_memory.cupmem_practical import PracticalCUPMemService
from team_memory.cupmem_candidates import SourceOnlyMemory
from tests.test_cupmem_practical import Engine, source


def witness(sid, text, stamp=None):
    return dict(source_id=sid, quote=text, start=0, end=len(text),
                speaker=sid, location='audit://'+sid, observed_at=stamp)


out = {}
class Node:
    metadata = dict(source_id='s', parent_start=0, parent_end=4)
    def get_content(self, metadata_mode):
        return 'Source 1:\nFact\n'

env = dict(source=dict(text='Fact', location='audit://s', speaker='Alice'),
           observed_at='2025-01-02T00:00:00Z')
w = ReferenceQA._witness(Node(), {'s': env}, 1)
out['date_boundary'] = dict(input_date=env['observed_at'], witness=w,
                            downstream_date=documents([w])[0]['recorded_at'])

rows = [witness('earlier', 'A', '2025-01-01T09:00:00+09:00'),
        witness('later', 'B', '2025-01-01T01:00:00+00:00')]
out['timezone_order'] = dict(expected=['earlier', 'later'],
                             actual=[r['source_id'] for r in documents(rows)])

raw = '  Fact\n'
canonical = source_envelope(dict(owner='Alice', observed_at='2025-01-01T00:00:00Z',
    source=dict(speaker='Alice', location='audit://text', text=raw)))['source']['text']
out['original_normalization'] = dict(raw=raw, stored=canonical,
    raw_fact_offset=raw.index('Fact'), stored_fact_offset=canonical.index('Fact'))

ws = [witness('a', 'The value is 10.'), witness('b', 'The value is 20.')]
previous = format_response('What is the value?', 'The value is 10 [1].', ws, allow_source_labels=True)
previous.update(draft_raw=previous['raw'], revised=False,
                document_judgments=[dict(source_id='b', label='CONTRADICTS')])
class LLM:
    def chat(self, messages):
        return SimpleNamespace(message=SimpleNamespace(content='The value is 999 [1][2].'))
repaired = repair_omitted_answer('What is the value?', previous, LLM())
out['source_id_guard'] = dict(before=previous['raw'], after=repaired['raw'],
    accepted=repaired['aqa_candidate_accepted'], status=repaired['status'])

# Practical service explicitly documents single-process ownership, not Git merging.
# Exercise the product boundary without misclassifying it as a supported-path bug.
with tempfile.TemporaryDirectory() as td:
    root = Path(td)
    for n in range(16):
        base = root / str(n)
        def service(path):
            return PracticalCUPMemService(SourceOnlyMemory(Engine()),
                lambda *_: '{"relations":[]}', path, strategy='simple')
        left, right = service(base/'left'), service(base/'right')
        a = left.ingest(source('Independent report A '+str(n)))
        b = right.ingest(source('Independent report B '+str(n), 2, 'Bob'))
        shutil.copytree(base/'left', base/'merged', dirs_exist_ok=True)
        shutil.copytree(base/'right', base/'merged', dirs_exist_ok=True)
        merged = service(base/'merged')
        result = merged.rebuild()
        if result['status'] == 'error':
            out['practical_git_merge_boundary'] = dict(trial=n, initial_statuses=[a['status'], b['status']],
                source_count=len(merged.store.load('sources')), arrivals=merged._arrivals(),
                batches=list(merged.store.load('cup_batches').values()), rebuild=result,
                classification='documented unsupported workflow; not a supported-path regression')
            break
    else:
        out['practical_git_merge_boundary'] = dict(reproduced=False)

print(json.dumps(out, ensure_ascii=False, indent=2))
