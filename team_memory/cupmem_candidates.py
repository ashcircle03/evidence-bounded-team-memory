"""Reuse the pinned CUPMem writer/retriever without generating an intermediate answer."""
from hashlib import sha256
import json

from .cupmem_adapter import CUPMemTeamMemory
from .store import digest, source_envelope
from evaluation.cupmem.provenance import persistent_state_hash, resolve_grounding
from evaluation.cupmem.transfer_inputs import attributed_session


class CachedEmbedding:
    """Batch the upstream encoder; retain its normalized vectors and cosine ranking.

    No answer cache. Both experimental arms use this same implementation. The
    bounded text cache is process-local derived state and may be discarded.
    """
    def __init__(self, upstream, *, batch_size=32, max_cached=16384):
        if batch_size < 1 or max_cached < 1:
            raise ValueError('positive embedding resource bounds required')
        self.upstream, self.batch_size, self.max_cached = upstream, batch_size, max_cached
        self.cache = {}

    def rank(self, *, query_text, candidates, text_getter, top_k):
        candidates = list(candidates)
        if not candidates or top_k <= 0:
            return []
        # The pinned TransformerRetriever supplies _encode and torch. Reuse the
        # public rank interface for alternate injected retrievers/test doubles.
        if not hasattr(self.upstream, '_encode'):
            return self.upstream.rank(query_text=query_text, candidates=candidates,
                                      text_getter=text_getter, top_k=top_k)
        texts = [text_getter(c) for c in candidates]
        missing = list(dict.fromkeys(t for t in [query_text, *texts] if t not in self.cache))
        vectors = {}
        for start in range(0, len(missing), self.batch_size):
            group = missing[start:start+self.batch_size]
            encoded = self.upstream._encode(group)
            vectors.update(zip(group, encoded))
        vectors.update((t, self.cache[t]) for t in [query_text, *texts] if t in self.cache)
        torch = self.upstream._torch
        query = vectors[query_text].unsqueeze(0)
        scores = torch.mm(query, torch.stack([vectors[t] for t in texts]).T).squeeze(0)
        rows = [dict(item=c, score=float(scores[i].item())) for i, c in enumerate(candidates)]
        rows.sort(key=lambda r: r['score'], reverse=True)
        for text in missing:
            if len(self.cache) >= self.max_cached:
                self.cache.pop(next(iter(self.cache)))
            self.cache[text] = vectors[text]
        return rows[:top_k]


def sources_for_hits(question, hits, snapshot, originals):
    """Resolve retrieved candidates, not composer-adjudicated answer evidence.

    The existing resolver follows delta/chunk/status-cause references. Each hit
    is isolated so an unresolved candidate cannot erase unrelated valid origins.
    The original JSON user turn is checked against the captured source envelope.
    """
    records, bases, warnings = {}, [], []
    by_id = {digest(e): e for e in originals}
    sessions = {s['session_id']: s for s in snapshot['session_logs']}
    for hit in hits:
        label = {'stale': 'STALE', 'unknown': 'UNKNOWN_CURRENT'}.get(hit['source'])
        if hit['source'] == 'active':
            label = 'ACTIVE_WEAK' if hit['source_detail'] == 'weak_active' else 'ACTIVE_STRONG'
        ref = {k: hit[k] for k in ('source', 'source_detail', 'id', 'bucket', 'local_track')}
        basis = dict(hit_ref=ref, status_label=label)
        resolved = resolve_grounding(dict(supporting_basis=[basis]), snapshot)
        if resolved['unresolved']:
            warnings.append(dict(reference=ref, reason='unresolved_profile_candidate'))
            continue
        selected = {}
        try:
            for p in resolved['original_turns_for_audit']:
                if sha256(p['text'].encode()).hexdigest() != p['content_sha256']:
                    raise ValueError('candidate source hash mismatch')
                env = source_envelope(json.loads(p['text']))
                sid = digest(env)
                session = sessions[p['session_id']]
                turns = {t['turn_id']: t['content'] for t in session['user_turns']}
                if (by_id.get(sid) != env or turns.get(p['turn_id']) != p['text']
                        or session['session_index'] != p['session_index']):
                    raise ValueError('candidate source binding mismatch')
                if not {u['purpose'] for u in p['uses']} <= {'value', 'status_cause'}:
                    raise ValueError('unsupported candidate lineage')
                selected[sid] = env
        except (ValueError, KeyError, TypeError):
            warnings.append(dict(reference=ref, reason='invalid_candidate_source_binding'))
            continue
        records.update(selected); bases.append(basis)
    return dict(question=question, records=list(records.values()), warnings=warnings,
                memory_annotations=dict(unverified_model_annotations=True, selected_bases=bases,
                                        selection='embedding candidates; no native premise adjudication'))


class CUPMemCandidateMemory(CUPMemTeamMemory):
    """Native writes, including explicit multi-turn source-collection imports."""
    def ingest_many(self, records):
        envs = [source_envelope(e) for e in records]
        if not envs:
            raise ValueError('nonempty source batch required')
        session = [turn for e in envs for turn in attributed_session(e)]
        # The source envelope retains each original observed_at. Native batch
        # timestamp is the latest observation, not fabricated per-record order.
        log = self.engine.write_session(session=session, session_index=len(self.sessions),
                                        session_time=max(e['observed_at'] for e in envs))
        self.sources.extend(envs); self.sessions.append(log)
        return dict(native_write=log, source_count=len(envs))

    def ingest(self, source, *, review_changes=False):
        if review_changes:
            raise ValueError('Service owns review; do not run native answer generation')
        return self.ingest_many([source])

    def candidates(self, question):
        from cup_mem.memory.models import QueryParse
        before = self.snapshot()
        try:
            parsed = QueryParse(intent_type='FACT_LOOKUP', target_bucket_tracks=[],
                                queried_proposition=question)
            hits = self.engine._retrieve_query_topk(parsed=parsed, query_text=question)
            return sources_for_hits(question, hits, before, self.sources)
        finally:
            if persistent_state_hash(before) != persistent_state_hash(self.snapshot()):
                raise AssertionError('Candidate retrieval changed native memory')

    def reset(self):
        self.engine.reset()
        self.sources.clear(); self.sessions.clear(); self.queries.clear()


class SourceOnlyMemory:
    """Simple control: the same source corpus/embedding, no native memory writer."""
    def __init__(self, engine):
        self.engine, self.sources, self.source_generate = engine, [], None
        self.recorded_calls = lambda: []

    def ingest_many(self, records):
        envs = [source_envelope(e) for e in records]
        self.sources.extend(envs)
        return dict(native_write=dict(performed=False, source_count=len(envs)))

    def ingest(self, source, *, review_changes=False):
        return self.ingest_many([source])

    def reset(self):
        self.sources.clear()
