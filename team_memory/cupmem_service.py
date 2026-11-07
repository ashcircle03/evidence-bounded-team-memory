"""A transport-free, serialized CUPMem service with durable originals and owner review.

The native profile is derived state. Original sources and approval events are
separate append-only records. Restart explicitly rebuilds the derived profile.
"""
import json
from threading import RLock

from . import timeline
from .core import answer_question, passages, records_view
from .cupmem_adapter import CUPMemTeamMemory, REVIEW_QUESTION
from .cupmem_readout import SOURCE_POLICY, source_packet
from .cupmem_review import review_sources
from .store import Store, capture, digest, source_envelope


from .review_policy import TEMPORAL_POLICY


def response(operation, status='ok', **fields):
    return dict(schema_version='team-memory-service/v1', operation=operation, status=status,
                answers=[], proposals=[], warnings=[], errors=[], **fields)


class CUPMemService:
    def __init__(self, memory, generate, store, *, original_top_k=4, max_source_passages=2048):
        if memory.source_generate is not None:
            raise ValueError('Inject the final generator into the service only; avoid duplicate readout')
        if not callable(generate) or not 0 <= original_top_k <= 8 or max_source_passages < 1:
            raise ValueError('generator and bounded source retrieval configuration required')
        self.memory, self.generate = memory, generate
        self.store = store if isinstance(store, Store) else Store(store)
        self.original_top_k, self.max_source_passages = original_top_k, max_source_passages
        self.lock = RLock()
        self.ready = [digest(e) for e in memory.sources] == self._arrivals()

    def _arrivals(self):
        rows = self.store.load('cup_intakes').values()
        return [r['source_id'] for r in sorted(rows, key=lambda r: (r['ordinal'], r['source_id']))]

    def _error(self, operation, stage, exc, **fields):
        result = response(operation, 'error', **fields)
        result['errors'] = [dict(stage=stage, type=type(exc).__name__)]
        return result

    def _links(self):
        sources = self.store.load('sources')
        visible = set(self._arrivals())
        links = []
        for p in timeline.proposals(self.store):
            if not {p['previous']['source_id'], p['incoming']['source_id']} <= visible:
                continue
            if p['status'] == 'rejected':
                continue
            support = p.get('support', {})
            if any(not timeline.valid_witness(w, sources) for items in support.values() for w in items):
                continue
            links.append(p)
        return links

    def _packet(self, question, native, *, incoming=None):
        visible = set(self._arrivals())
        originals = {sid: env for sid, env in self.store.load('sources').items() if sid in visible}
        records, origins, warnings = {}, {}, []
        annotations = dict(unverified_model_annotations=True, selected_bases=[])

        def add(env, origin):
            sid = digest(env)
            if originals.get(sid) != env:
                raise ValueError('Selected source does not match a captured original')
            records[sid] = env
            origins.setdefault(sid, [])
            if origin not in origins[sid]:
                origins[sid].append(origin)

        if native is not None:
            try:
                packet = source_packet(native)
                for env in packet['records']:
                    add(env, 'native_provenance')
                annotations = packet['memory_annotations']
            except (ValueError, KeyError, TypeError):
                records.clear(); origins.clear()
                warnings.append('Native provenance unavailable; independent original retrieval remains explicit')
        else:
            warnings.append('Native query failed; independent original retrieval remains explicit')

        if self.original_top_k:
            candidates = passages(dict(sources=records_view(list(originals.values()))))
            if len(candidates) > self.max_source_passages:
                warnings.append('Original retrieval passage limit exceeded; no silent history truncation')
            else:
                query = question if incoming is None else incoming['source']['text']
                try:
                    ranked = self.memory.engine.embedding.rank(query_text=query, candidates=candidates,
                        text_getter=lambda p: p['quote'], top_k=self.original_top_k)
                    by_id = {p['id']: p for p in candidates}
                    if any(by_id.get(hit['item'].get('id')) != hit['item'] for hit in ranked):
                        raise ValueError('Original retriever returned a non-candidate passage')
                    for hit in ranked:
                        add(originals[hit['item']['source_id']], 'original_embedding_search')
                except Exception as exc:
                    warnings.append('Original retrieval failed: ' + type(exc).__name__)
        if incoming is not None:
            add(incoming, 'explicit_incoming_record')

        # Review counterparts are explicit evidence links, never a full-history fallback.
        links = self._links()
        changed = True
        while changed:
            changed = False
            for p in links:
                endpoints = {p['previous']['source_id'], p['incoming']['source_id']}
                if endpoints & records.keys():
                    for sid in endpoints - records.keys():
                        add(originals[sid], 'team_review_counterpart')
                        changed = True
        links = [p for p in links if {p['previous']['source_id'], p['incoming']['source_id']} <= records.keys()]
        return dict(records=list(records.values()), question=question, memory_annotations=annotations,
                    source_origins=origins, relations=links, warnings=warnings)

    def _native(self, question):
        try:
            return self.memory.ask(question), None
        except AssertionError as exc:
            self.ready = False
            return None, dict(stage='native_query_state', type=type(exc).__name__)
        except Exception as exc:
            return None, dict(stage='native_query', type=type(exc).__name__)

    def ingest(self, source):
        with self.lock:
            try:
                env = source_envelope(source)
            except (KeyError, TypeError, ValueError) as exc:
                result = self._error('ingest', 'input', exc); result['status'] = 'invalid'; return result
            sid = digest(env)
            if not self.ready:
                return response('ingest', 'needs_rebuild', source_id=sid)
            done = [r for r in self.store.load('cup_receipts').values() if r['source_id'] == sid]
            if done:
                result = json.loads(json.dumps(done[0]['result']))
                result['replayed'] = True
                # A previously pending proposal may have been reviewed since intake.
                ids = {p['id'] for p in result['proposals']}
                result['proposals'] = [p for p in timeline.proposals(self.store) if p['id'] in ids]
                return result
            known = self._arrivals()
            if sid in known:
                return response('ingest', source_id=sid, replayed=True, review_available=False)
            capture(self.store, env)
            self.store.put('cup_intakes', dict(source_id=sid, ordinal=len(known)))
            try:
                written = self.memory.ingest(env, review_changes=False)
            except Exception as exc:
                self.ready = False
                result = self._error('ingest', 'native_write', exc, source_id=sid, original_preserved=True)
                result['recovery'] = 'explicit_rebuild_required'
                return result
            result = response('ingest', source_id=sid, replayed=False, native_write=written['native_write'])
            if known:
                question = REVIEW_QUESTION + '\nIncoming original report:\n' + env['source']['text']
                native, native_error = self._native(question)
                result['native'] = native
                if native_error:
                    result['errors'].append(native_error)
                try:
                    if not self.ready:
                        raise RuntimeError('Native query mutated memory')
                    packet = self._packet(question, native, incoming=env)
                    reviewed = review_sources(packet['records'], env, self.generate,
                                              annotations=packet['memory_annotations'])
                    result.update(status=reviewed['status'], raw_review=reviewed['raw'],
                                  source_origins=packet['source_origins'])
                    result['warnings'] += packet['warnings'] + reviewed['warnings']
                    ids = [self.store.put('timeline_proposals', p) for p in reviewed['proposals']]
                    result['proposals'] = [p for p in timeline.proposals(self.store) if p['id'] in ids]
                except Exception as exc:
                    result['status'] = 'error'
                    result['errors'].append(dict(stage='review', type=type(exc).__name__))
            if result['status'] == 'ok' and (result['warnings'] or result['errors']):
                result['status'] = 'partial'
            self.store.put('cup_receipts', dict(source_id=sid, result=result))
            return result

    def ask(self, question, *, temporal_scope='current'):
        with self.lock:
            if not isinstance(question, str) or not question.strip() or temporal_scope not in ('current', 'historical'):
                return response('ask', 'invalid', temporal_scope=temporal_scope)
            if not self.ready:
                return response('ask', 'needs_rebuild', temporal_scope=temporal_scope)
            if not self._arrivals():
                return response('ask', 'insufficient', temporal_scope=temporal_scope)
            native, native_error = self._native(question)
            result = response('ask', question=question, temporal_scope=temporal_scope, native=native)
            if native_error:
                result['errors'].append(native_error)
            if not self.ready:
                result['status'] = 'needs_rebuild'; return result
            try:
                packet = self._packet(question, native)
                result['source_origins'] = packet['source_origins']
                result['warnings'] += packet['warnings']
                if not packet['records']:
                    result['status'] = 'insufficient'; return result

                def generate(system, content):
                    body = json.loads(content)
                    body.update(temporal_scope=temporal_scope, memory_annotations=packet['memory_annotations'],
                                source_origins=packet['source_origins'])
                    return self.generate(system + '\n' + SOURCE_POLICY + '\n' + TEMPORAL_POLICY,
                                         json.dumps(body, ensure_ascii=False))

                answer = answer_question(packet['records'], question, generate, relations=packet['relations'])
                result.update(status=answer['status'], kind=answer['kind'], answers=answer['answers'],
                              raw=answer['raw'], rejected_answers=answer['rejected_answers'])
                result['warnings'] += answer['warnings']
                for a in result['answers']:
                    for e in a['evidence']:
                        e['source_origins'] = packet['source_origins'][e['source_id']]
                        e['fully_superseded'] = any(p['kind'] == 'correction' and p['status'] == 'approved'
                            and p['previous']['source_id'] == e['source_id']
                            and p['previous']['start'] <= e['start'] and e['end'] <= p['previous']['end']
                            for p in packet['relations'])
                    if temporal_scope == 'current' and all(e['fully_superseded'] for e in a['evidence']):
                        result['warnings'].append('Current answer relies only on superseded assertions; needs review')
                if answer['kind'] == 'insufficient' and not answer['answers'] and answer['status'] == 'ok':
                    result['status'] = 'insufficient'
                if result['status'] == 'ok' and (result['warnings'] or result['errors']):
                    result['status'] = 'partial'
            except Exception as exc:
                result['status'] = 'error'
                result['errors'].append(dict(stage='source_readout', type=type(exc).__name__))
            return result

    def review(self, proposal_id, actor, choice):
        with self.lock:
            try:
                row = timeline.review(self.store, proposal_id, actor, choice)
                result = response('review'); result['proposals'] = [row]; return result
            except (ValueError, KeyError, TypeError) as exc:
                result = self._error('review', 'owner_review', exc); result['status'] = 'invalid'; return result

    def rebuild(self):
        with self.lock:
            self.ready = False
            try:
                self.memory.engine.reset()
                self.memory = CUPMemTeamMemory(self.memory.engine, self.memory.recorded_calls)
                originals = self.store.load('sources')
                for sid in self._arrivals():
                    self.memory.ingest(originals[sid], review_changes=False)
                self.ready = True
                return response('rebuild', source_count=len(self.memory.sources),
                                native_writes_performed=len(self.memory.sources))
            except Exception as exc:
                return self._error('rebuild', 'native_write', exc, completed_sources=len(self.memory.sources))

    def handle(self, request):
        if not isinstance(request, dict):
            return response('invalid', 'invalid')
        operation = request.get('operation', 'invalid')
        try:
            if operation == 'ingest': return self.ingest(request['source'])
            if operation == 'ask': return self.ask(request['question'], temporal_scope=request.get('temporal_scope', 'current'))
            if operation == 'review': return self.review(request['proposal_id'], request['actor'], request['choice'])
            if operation == 'rebuild': return self.rebuild()
            return response(str(operation), 'invalid')
        except (KeyError, TypeError, ValueError) as exc:
            result = self._error(str(operation), 'input', exc); result['status'] = 'invalid'; return result
        except Exception as exc:
            return self._error(str(operation), 'service', exc)
