"""Team retrieval from candidate channels to citation witnesses.

1. candidates        CandidateSource -> named ranked lists (dense, sparse)
2. fusion            upstream QueryFusionRetriever reciprocal_rerank, unchanged
   turn reranking    reorder only the first five fused hits with transcript candidates
3. review expansion  review_evidence.expand_review_context, unchanged
4. review state      review_evidence.review_sources as typed nodes
5. citations         CitationQueryEngine citation nodes -> verbatim witnesses

The evidence budget stays in adapters/retrieval.py.

Only stage 1 is meant to be replaced, for example by vectors that records
writes at save time. Fusion reuses the upstream class instead of a copy, so
its constant (k=60), duplicate rule (node hash, later object wins) and tie
order stay byte-identical. The upstream class rewrites node scores in place,
so each channel's ranks and scores are recorded before fusion.
"""
from contextlib import contextmanager, nullcontext
from dataclasses import asdict, dataclass
from importlib.metadata import version as package_version
import time

from llama_index.core.retrievers import BaseRetriever, QueryFusionRetriever
from llama_index.core.schema import NodeWithScore, QueryBundle, TextNode


class Trace:
    """Diagnostics of one retrieval request.

    Timings stay apart from the content, so the content is the same for the
    same input. A failure records its stage and exception type only; messages
    can carry secrets. The innermost failing stage is the one recorded.
    """

    def __init__(self):
        self.data, self.timings_ms, self.failure = {}, {}, None

    @contextmanager
    def stage(self, name):
        start = time.perf_counter()
        try:
            yield
        except BaseException as exc:
            if self.failure is None:
                self.failure = dict(stage=name, exception=type(exc).__name__)
            raise
        finally:
            spent = (time.perf_counter() - start) * 1000
            self.timings_ms[name] = round(self.timings_ms.get(name, 0.0) + spent, 3)

    def record(self, key, value):
        self.data[key] = value


class _NoTrace:
    def stage(self, name):
        return nullcontext()

    def record(self, key, value):
        pass


NO_TRACE = _NoTrace()


def plain(candidates):
    """JSON form of candidates; scores become Python floats."""
    return [dict(asdict(c), score=None if c.score is None else float(c.score)) for c in candidates]


def expansion_record(retrieved_count, selected, context):
    """What stage 3 added: linked proposals and the spans appended after the retrieved nodes."""
    return dict(proposal_ids=[r['id'] for r in (context or {}).get('relations', [])],
                added=[dict(source_id=n.node.metadata['source_id'], start=n.node.metadata['parent_start'],
                            end=n.node.metadata['parent_end']) for n in selected[retrieved_count:]])


@dataclass(frozen=True)
class Candidate:
    """One ranked hit as its channel returned it."""
    channel: str
    rank: int
    score: float | None
    node_id: str
    source_id: str | None
    start: int | None
    end: int | None


def describe(channel, nodes):
    return [Candidate(channel, rank, n.score, n.node.node_id, n.node.metadata.get('source_id'),
                      n.node.metadata.get('parent_start'), n.node.metadata.get('parent_end'))
            for rank, n in enumerate(nodes, 1)]


class CandidateSource:
    """Stage 1. retrieve() returns {channel: ranked NodeWithScore list}.

    Channel order is the order fusion sees. One channel means no fusion.
    """
    name = 'abstract'
    version = '0'

    def retrieve(self, query_bundle):
        raise NotImplementedError


class LlamaIndexCandidates(CandidateSource):
    """Default stage 1: dense search over the prepared index, plus the prepared BM25.

    Both come from retrieval.indexing; nothing is rebuilt per question. With
    use_sparse the sparse channel is used as given, exactly as ask did before.
    """
    name = 'llama-index-dense-bm25'
    version = f"llama-index-core/{package_version('llama-index-core')}"

    def __init__(self, index, top_k, *, sparse=None, use_sparse=False):
        self.channels = {'dense': index.as_retriever(similarity_top_k=top_k)}
        if use_sparse:
            self.channels['sparse'] = sparse

    def retrieve(self, query_bundle):
        return {name: retriever.retrieve(query_bundle) for name, retriever in self.channels.items()}


class ThresholdedCandidates(CandidateSource):
    """Stage 1 filter for "not in the records": drop candidates no threshold vouches for.

    thresholds maps channel name to a minimum score or None. A candidate passes
    if, in some channel that has a threshold, its score is at least that value.
    Channels without a threshold cannot make a candidate pass. Passing
    candidates keep their place in every channel, so fusion still sees both
    ranks. If nothing passes, retrieval has no hits. The excluded candidates,
    with their original ranks and scores, go to the trace.
    """

    def __init__(self, inner, thresholds, *, trace=None):
        if all(value is None for value in thresholds.values()):
            raise ValueError('At least one score threshold is required')
        self.inner, self.thresholds, self.trace = inner, dict(thresholds), trace or NO_TRACE
        self.name, self.version = f'{inner.name}+thresholds', inner.version

    def retrieve(self, query_bundle):
        channels = self.inner.retrieve(query_bundle)
        passing = {n.node.node_id for name, nodes in channels.items() if self.thresholds.get(name) is not None
                   for n in nodes if n.score is not None and n.score >= self.thresholds[name]}
        self.trace.record('thresholds', dict(minimum=self.thresholds, excluded=[
            item for name, nodes in channels.items() for item in plain(describe(name, nodes))
            if item['node_id'] not in passing]))
        return {name: [n for n in nodes if n.node.node_id in passing] for name, nodes in channels.items()}


def normalized(text):
    return ' '.join(str(text).split()).casefold()


class ConditionFilteredCandidates(CandidateSource):
    """Stage 1 filter by the query's conditions against records' condition spans.

    recorded(source_id, start, end) returns the condition quotes records links
    to claims inside a candidate's span. A candidate is kept when records shows
    no condition for it, or when one of those quotes contains one of the
    requested conditions (case and spacing ignored). It is removed only when
    records shows conditions and none contains a requested one; an unstated
    condition is never treated as a mismatch. Matching is lexical: "v1" and
    "version 1" do not match. Removed candidates go to the trace.
    """

    def __init__(self, inner, requested, recorded, *, trace=None):
        self.inner, self.recorded, self.trace = inner, recorded, trace or NO_TRACE
        self.requested = [c for c in requested if normalized(c)]
        if not self.requested:
            raise ValueError('At least one requested condition is required')
        self.name, self.version = f'{inner.name}+conditions', inner.version

    def retrieve(self, query_bundle):
        channels = self.inner.retrieve(query_bundle)
        wanted = [normalized(c) for c in self.requested]
        keep, excluded = {}, []
        for nodes in channels.values():
            for n in nodes:
                node_id = n.node.node_id
                if node_id in keep:
                    continue
                meta = n.node.metadata
                found = self.recorded(meta.get('source_id'), meta.get('parent_start'), meta.get('parent_end'))
                keep[node_id] = not found or any(w in normalized(q) for q in found for w in wanted)
                if not keep[node_id]:
                    excluded.append(dict(node_id=node_id, source_id=meta.get('source_id'), start=meta.get('parent_start'),
                                         end=meta.get('parent_end'), conditions=list(found)))
        self.trace.record('condition_filter', dict(requested=list(self.requested), excluded=excluded))
        return {name: [n for n in nodes if keep[n.node.node_id]] for name, nodes in channels.items()}


class _Fixed(BaseRetriever):
    """Hand an already retrieved list to the upstream fusion class."""

    def __init__(self, nodes):
        super().__init__()
        self._nodes = nodes

    def _retrieve(self, query_bundle):
        return self._nodes


class StagedRetriever(BaseRetriever):
    """Stages 1 and 2 behind the retriever interface CitationQueryEngine expects.

    `last` keeps the source, each channel's candidates and the fused order of
    the most recent call. A new instance is built for every question.
    """

    def __init__(self, source, *, llm, fused_top_k=None, trace=None, turn_sources=None):
        super().__init__()
        self.source, self.llm, self.fused_top_k = source, llm, fused_top_k
        self.trace = trace or NO_TRACE
        self.turn_sources = turn_sources
        self.last = None

    def _retrieve(self, query_bundle):
        self.trace.record('candidate_source', dict(name=self.source.name, version=self.source.version))
        with self.trace.stage('candidates'):
            channels = self.source.retrieve(query_bundle)
        candidates = {name: describe(name, nodes) for name, nodes in channels.items()}
        self.trace.record('candidates', {name: plain(items) for name, items in candidates.items()})
        with self.trace.stage('fusion'):
            if len(channels) == 1:
                fused = next(iter(channels.values()))
            else:
                if self.fused_top_k is None:
                    raise ValueError('Fusing several candidate channels needs fused_top_k')
                fusion = QueryFusionRetriever([_Fixed(nodes) for nodes in channels.values()], llm=self.llm,
                    similarity_top_k=self.fused_top_k, num_queries=1,
                    mode='reciprocal_rerank', use_async=False)
                fused = fusion.retrieve(query_bundle)
        self.last = dict(source=dict(name=self.source.name, version=self.source.version),
                         candidates=candidates, fused=describe('fused', fused))
        self.trace.record('fused', plain(self.last['fused']))
        if self.turn_sources is not None:
            from .reranking import previous_turn_order
            with self.trace.stage('turn_reranking'):
                fused = previous_turn_order(query_bundle.query_str, fused, self.turn_sources)
            self.trace.record('reranked', plain(describe('reranked', fused)))
        return fused


def expand_review(nodes, sources, relations, temporal_scope):
    """Stage 3: follow validated proposal links from retrieved sources."""
    from .review_evidence import expand_review_context
    return expand_review_context(nodes, sources, relations, temporal_scope)


def review_state_nodes(store, context):
    """Stage 4: one typed review_state citation per linked proposal."""
    from .review_evidence import review_sources
    nodes = []
    for witness in review_sources(store, context):
        metadata = dict(source_id=witness['source_id'], record_author=witness['speaker'],
                        evidence_type='review_state', review_witness=witness)
        nodes.append(NodeWithScore(node=TextNode(text=witness['quote'], metadata=metadata,
            excluded_embed_metadata_keys=list(metadata),
            excluded_llm_metadata_keys=['source_id', 'review_witness'])))
    return nodes


def citation_nodes(splitter, metadata_mode, nodes):
    """Stage 5 split without a query engine.

    The same as CitationQueryEngine._create_citation_nodes in llama-index-core
    0.14.25 for text nodes: split each node's content, drop its id and offsets,
    and number the chunks "Source N:". Retrieval-only requests need this split
    but none of the engine's generation components.
    """
    result = []
    for node in nodes:
        chunks = splitter.split_text(node.node.get_content(metadata_mode=metadata_mode))
        data = node.node.model_dump()
        data.pop('id_', None)
        data['start_char_idx'] = None
        data['end_char_idx'] = None
        for chunk in chunks:
            item = NodeWithScore(node=TextNode.model_validate(data), score=node.score)
            item.node.set_content(f'Source {len(result) + 1}:\n{chunk}\n')
            result.append(item)
    return result


def witnesses_from_nodes(reader, retriever, splitter, metadata_mode, question, selected_nodes, sources):
    """Stage 5 for retrieval-only requests: citation split, then offsets via reader._witness."""
    nodes = retriever.retrieve(QueryBundle(question)) if selected_nodes is None else selected_nodes
    return [reader._witness(n.node, sources, i)
            for i, n in enumerate(citation_nodes(splitter, metadata_mode, nodes), 1)]
