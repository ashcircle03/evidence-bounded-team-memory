"""Retrieval split into stages without changing what ReferenceQA returns.

1. candidates        CandidateSource -> named ranked lists (dense, sparse)
2. fusion            upstream QueryFusionRetriever reciprocal_rerank, unchanged
3. review expansion  readers.context.expand_review_context, unchanged
4. review state      readers.state_citations.review_sources as typed nodes
5. citations         CitationQueryEngine citation nodes -> verbatim witnesses

The evidence budget stays in adapters/retrieval.py.

Only stage 1 is meant to be replaced, for example by vectors that records
writes at save time. Fusion reuses the upstream class instead of a copy, so
its constant (k=60), duplicate rule (node hash, later object wins) and tie
order stay byte-identical. The upstream class rewrites node scores in place,
so each channel's ranks and scores are recorded before fusion.
"""
from dataclasses import dataclass
from importlib.metadata import version as package_version

from llama_index.core.retrievers import BaseRetriever, QueryFusionRetriever
from llama_index.core.schema import NodeWithScore, QueryBundle, TextNode


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

    Both come from readers.indexing; nothing is rebuilt per question. With
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

    def __init__(self, source, *, llm, fused_top_k=None):
        super().__init__()
        self.source, self.llm, self.fused_top_k = source, llm, fused_top_k
        self.last = None

    def _retrieve(self, query_bundle):
        channels = self.source.retrieve(query_bundle)
        candidates = {name: describe(name, nodes) for name, nodes in channels.items()}
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
        return fused


def expand_review(nodes, sources, relations, temporal_scope):
    """Stage 3: follow validated proposal links from retrieved sources."""
    from team_memory.readers.context import expand_review_context
    return expand_review_context(nodes, sources, relations, temporal_scope)


def review_state_nodes(store, context):
    """Stage 4: one typed review_state citation per linked proposal."""
    from team_memory.readers.state_citations import review_sources
    nodes = []
    for witness in review_sources(store, context):
        metadata = dict(source_id=witness['source_id'], record_author=witness['speaker'],
                        evidence_type='review_state', review_witness=witness)
        nodes.append(NodeWithScore(node=TextNode(text=witness['quote'], metadata=metadata,
            excluded_embed_metadata_keys=list(metadata),
            excluded_llm_metadata_keys=['source_id', 'review_witness'])))
    return nodes


def citation_witnesses(reader, engine, question, selected_nodes, sources):
    """Stage 5: CitationQueryEngine's own split, then offsets via reader._witness."""
    nodes = engine._create_citation_nodes(
        engine.retrieve(QueryBundle(question)) if selected_nodes is None else selected_nodes)
    return [reader._witness(n.node, sources, i) for i, n in enumerate(nodes, 1)]
