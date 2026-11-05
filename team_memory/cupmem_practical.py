"""Single-readout QA and source-grounded team review over the existing CUPMem writer.

Service-v1 stays frozen. This version reuses its response/QA/approval handling,
and replaces query orchestration rather than changing historical measurements.
"""
import json

from . import timeline
from .core import compare_records, passages, records_view
from .cupmem_review import review_sources
from .cupmem_service import CUPMemService, response
from .store import capture, digest, source_envelope


REVIEW_SCOPE = '''A reconsideration is a recommendation to revisit a decision under changed premises.
It does not establish that the earlier decision was wrong, invalidated, or already reversed.
Explain which premise no longer applies and why reconsideration is warranted; do not announce
an unapproved decision change. The incoming report must affect the SAME entity, operation and
scope as the old rationale. Evidence that merely concerns a similar topic is insufficient.
Conditions for coexist must describe the actual measured settings, not merely available options.
An explicit correction/retraction is distinct from a changed operating condition.'''


class PracticalCUPMemService(CUPMemService):
    def __init__(self, memory, generate, store, *, strategy='cupmem', original_top_k=4,
                 max_source_passages=16384, max_review_candidates=8):
        if strategy not in ('cupmem', 'simple'):
            raise ValueError('strategy must be cupmem or simple')
        self.strategy = strategy
        if max_review_candidates < 1:
            raise ValueError('positive review candidate bound required')
        self.max_review_candidates = max_review_candidates
        super().__init__(memory, generate, store, original_top_k=original_top_k,
                         max_source_passages=max_source_passages)

    def _native(self, question):
        # The inherited QA path calls this hook. No answer is generated and
        # discarded before the one authoritative original-source reader.
        return dict(backend=self.strategy, native_query_executed=False), None

    def _packet(self, question, native, *, incoming=None):
        visible = set(self._arrivals())
        originals = {sid: env for sid, env in self.store.load('sources').items() if sid in visible}
        records, origins, warnings = {}, {}, []
        annotations = dict(unverified_model_annotations=True, selected_bases=[])

        def add(env, origin):
            sid = digest(env)
            if originals.get(sid) != env:
                raise ValueError('Selected source is not an ingested original')
            records[sid] = env
            if origin not in origins.setdefault(sid, []):
                origins[sid].append(origin)

        earlier = [e for sid, e in originals.items() if incoming is None or sid != digest(incoming)]
        candidates = passages(dict(sources=records_view(earlier)))
        if len(candidates) > self.max_source_passages:
            raise ValueError('Source retrieval candidate limit exceeded; no silent truncation')
        query = incoming['source']['text'] if incoming else question
        if self.original_top_k and candidates:
            ranked = self.memory.engine.embedding.rank(query_text=query, candidates=candidates,
                text_getter=lambda p: p['quote'], top_k=self.original_top_k)
            lookup = {p['id']: p for p in candidates}
            for hit in ranked:
                if lookup.get(hit['item'].get('id')) != hit['item']:
                    raise ValueError('Retriever returned a non-candidate passage')
                add(originals[hit['item']['source_id']], 'original_embedding_search')

        # Factual QA intentionally shares its retrieval/readout with the simple
        # control. Native state candidates assist review, not factual deletion.
        if incoming is not None and self.strategy == 'cupmem':
            try:
                selected = self.memory.candidates(query)
                annotations = selected['memory_annotations']
                warnings.extend(selected['warnings'])
                for env in selected['records']:
                    add(env, 'native_profile_candidate')
            except AssertionError:
                self.ready = False
                raise
            except Exception as exc:
                warnings.append('Native candidate retrieval failed: ' + type(exc).__name__)
        if incoming is not None:
            add(incoming, 'explicit_incoming_record')
        links = self._links()
        changed = True
        while changed:
            changed = False
            for p in links:
                ends = {p['previous']['source_id'], p['incoming']['source_id']}
                if ends & records.keys():
                    for sid in ends - records.keys():
                        add(originals[sid], 'team_review_counterpart'); changed = True
        links = [p for p in links if {p['previous']['source_id'], p['incoming']['source_id']} <= records.keys()]
        return dict(records=list(records.values()), question=question, memory_annotations=annotations,
                    source_origins=origins, relations=links, warnings=warnings)

    def _review(self, packet, incoming):
        if self.strategy == 'simple':
            prior = [e for e in packet['records'] if digest(e) != digest(incoming)]
            result = compare_records(prior, incoming, self.generate)
            result['proposals'] = [{k: v for k, v in p.items() if k not in ('id', 'status')}
                                   for p in result.pop('relations')]
            return result
        def scoped(system, content):
            return self.generate(system + '\n' + REVIEW_SCOPE, content)
        earlier = [e for e in packet['records'] if digest(e) != digest(incoming)]
        output, warnings, traces = [], [], []
        if len(earlier) > self.max_review_candidates:
            warnings.append('Review candidate limit exceeded; remaining candidates were not judged')
        for old in earlier[:self.max_review_candidates]:
            # Each question is about THIS incoming report. Comparing all prior
            # sources together let the model rediscover an old-old relationship
            # on unrelated intake. Reuse the same reviewer on one candidate pair.
            sid = digest(old)
            reviewed = review_sources([old, incoming], incoming, scoped,
                annotations=dict(unverified_model_annotations=True,
                                 candidate_origins=packet['source_origins'].get(sid, [])))
            output.extend(reviewed['proposals'])
            warnings.extend(sid + ': ' + w for w in reviewed['warnings'])
            traces.append(dict(previous_source_id=sid, incoming_source_id=digest(incoming),
                               status=reviewed['status'], raw=reviewed['raw']))
        if not earlier:
            return dict(status='insufficient', proposals=[], warnings=['No retrieved earlier source'],raw=None,traces=[])
        valid_pairs = any(t['status']=='ok' for t in traces)
        status = 'partial' if warnings and (output or valid_pairs) else 'invalid' if warnings else 'ok'
        return dict(status=status,proposals=output,warnings=warnings,raw=None,traces=traces)

    def ingest(self, source):
        with self.lock:
            try:
                env = source_envelope(source)
            except (KeyError, TypeError, ValueError) as exc:
                result = self._error('ingest', 'input', exc); result['status'] = 'invalid'; return result
            sid = digest(env)
            if not self.ready:
                return response('ingest', 'needs_rebuild', source_id=sid)
            known = self._arrivals()
            if sid in known:
                # Existing service refreshes actual vote status on saved receipts.
                return super().ingest(env)
            capture(self.store, env)
            self.store.put('cup_intakes', dict(source_id=sid, ordinal=len(known)))
            self.store.put('cup_batches', dict(ordinal=len(known), source_ids=[sid], kind='arrival'))
            try:
                written = self.memory.ingest(env, review_changes=False)
            except Exception as exc:
                self.ready = False
                result = self._error('ingest', 'native_write', exc, source_id=sid, original_preserved=True)
                result['recovery'] = 'explicit_rebuild_required'; return result
            result = response('ingest', source_id=sid, replayed=False, native_write=written['native_write'])
            if known:
                try:
                    packet = self._packet(env['source']['text'], None, incoming=env)
                    reviewed = self._review(packet, env)
                    result.update(status=reviewed['status'], raw_review=reviewed['raw'],
                                  source_origins=packet['source_origins'], review_traces=reviewed.get('traces', []))
                    result['warnings'] = packet['warnings'] + reviewed['warnings']
                    ids = [self.store.put('timeline_proposals', dict(p, producer='cupmem-practical-v2/'+self.strategy))
                           for p in reviewed['proposals']]
                    result['proposals'] = [p for p in timeline.proposals(self.store) if p['id'] in ids]
                except Exception as exc:
                    result['status'] = 'error'
                    result['errors'].append(dict(stage='review', type=type(exc).__name__))
            if result['status'] == 'ok' and result['warnings']:
                result['status'] = 'partial'
            self.store.put('cup_receipts', dict(source_id=sid, result=result))
            return result

    def import_history(self, records, *, max_batch_records=16, max_batch_chars=12000):
        """Initialize a source collection through native multi-turn writes.

        No automatic proposals on bulk import; original records/chronology stay
        intact. This operation is explicit and only permitted in an empty store.
        """
        with self.lock:
            if not self.ready:
                return response('import_history', 'needs_rebuild')
            if self._arrivals():
                return response('import_history', 'invalid', reason='empty store required')
            try:
                if not isinstance(records, list) or not records or max_batch_records < 1 or max_batch_chars < 1:
                    raise ValueError('nonempty records and positive import bounds required')
                envs = [source_envelope(e) for e in records]
                if len({digest(e) for e in envs}) != len(envs):
                    raise ValueError('duplicate source in import')
                batches, batch, size = [], [], 0
                for e in envs:
                    width = len(json.dumps(e, ensure_ascii=False))
                    if width > max_batch_chars:
                        raise ValueError('single original exceeds import bound')
                    if batch and (len(batch) >= max_batch_records or size+width > max_batch_chars):
                        batches.append(batch); batch, size = [], 0
                    batch.append(e); size += width
                if batch: batches.append(batch)
            except (KeyError, ValueError, TypeError) as exc:
                result = self._error('import_history', 'input', exc); result['status'] = 'invalid'; return result
            for i, e in enumerate(envs):
                capture(self.store, e)
                self.store.put('cup_intakes', dict(source_id=digest(e), ordinal=i))
            offset = 0
            for group in batches:
                self.store.put('cup_batches', dict(ordinal=offset, source_ids=[digest(e) for e in group], kind='import'))
                offset += len(group)
            self.ready = False
            try:
                for group in batches:
                    self.memory.ingest_many(group)
                self.ready = True
                return response('import_history', source_count=len(envs), batches=len(batches),
                                native_writer=self.strategy == 'cupmem')
            except Exception as exc:
                return self._error('import_history', 'native_write', exc, original_preserved=True,
                                   completed_sources=len(self.memory.sources), recovery='explicit_rebuild_required')

    def rebuild(self):
        with self.lock:
            self.ready = False
            try:
                self.memory.reset()
                originals = self.store.load('sources')
                batches = sorted(self.store.load('cup_batches').values(), key=lambda b: b['ordinal'])
                if [sid for b in batches for sid in b['source_ids']] != self._arrivals():
                    raise ValueError('Import/arrival manifest does not cover exact source order')
                for batch in batches:
                    self.memory.ingest_many([originals[sid] for sid in batch['source_ids']])
                self.ready = True
                return response('rebuild', source_count=len(self.memory.sources), native_batches=len(batches),
                                native_writer=self.strategy == 'cupmem')
            except Exception as exc:
                return self._error('rebuild', 'native_write', exc, completed_sources=len(self.memory.sources))

    def handle(self, request):
        if isinstance(request, dict) and request.get('operation') == 'import_history':
            return self.import_history(request.get('records'))
        return super().handle(request)
