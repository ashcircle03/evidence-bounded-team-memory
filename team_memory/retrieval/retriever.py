"""Retrieval only: index records snapshots and return verbatim evidence (witnesses).

Split out of ReferenceQA (retrieval/search.py) so retrieval needs no answer model
and imports nothing from answering (team_memory.answering). ReferenceQA now extends
Retriever and adds generation; its constructor and ask() behave as before.

Stages (retrieval/stages.py): candidates -> reciprocal-rank fusion -> optional
previous-turn reranking (reranking.py) -> optional review-state expansion ->
citation split with verbatim offsets.
"""
from hashlib import sha256
from pathlib import Path
from threading import RLock

from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import MetadataMode

from team_memory.storage.objects import Store, digest, source_envelope


class Retriever:
    def __init__(self, store, *, embed_model, tokenizer, llm=None, top_k=4, chunk_size=512, chunk_overlap=64,
                 index_dir=None, profile='standard', index_unit='chunks', rerank_turns=True):
        """llm is optional and never called here: fusion runs with num_queries=1.

        Without one, a LlamaIndex MockLLM keeps fusion from resolving a default model.
        """
        if profile not in ('standard', 'team'):
            raise ValueError('Unknown source-QA profile')
        if index_unit not in ('chunks', 'records'):
            raise ValueError('Unknown index unit')
        self.rerank_turns = rerank_turns
        self.profile = profile
        if not 0 <= chunk_overlap < chunk_size or top_k < 1:
            raise ValueError('Positive retrieval and valid chunk bounds required')
        self.store = store if isinstance(store, Store) else Store(store)
        if llm is None:
            from llama_index.core.llms import MockLLM
            llm = MockLLM()
        self.llm, self.embed_model, self.tokenizer = llm, embed_model, tokenizer
        self.top_k = top_k
        self.index_dir = Path(index_dir) if index_dir else self.store.root / 'reference-index'
        self.lock = RLock()
        self.splitter = SentenceSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap,
            id_func=lambda i,doc: "node:"+digest([doc.id_,i]),
            tokenizer=lambda text: tokenizer.encode(text, add_special_tokens=False), include_metadata=False)
        self.index_config = dict(backend='llama-index-core/0.14.25', node_ids='source-chunk/v1', chunk_size=chunk_size,
            chunk_overlap=chunk_overlap, embedding=embed_model.to_dict(),
            tokenizer_sha256=sha256(tokenizer.backend_tokenizer.to_str().encode()).hexdigest())
        if profile == 'team':
            self.index_config['metadata_profile'] = 'author-recorded-at-v1'
        if index_unit == 'records':
            # Opt-in: index records' claim spans where a record_graph exists (retrieval.indexing).
            # The default adds nothing, so existing index keys and output stay the same.
            from .indexing import RECORD_INDEX_UNIT
            self.index_config['index_unit'] = RECORD_INDEX_UNIT
        self.index = None
        self.index_key = None
        self.sparse = None

    def import_history(self, records, *, prepare=True):
        # Validate the complete input before capturing anything. This operation
        # does not invoke either an LLM or CUPMem. Indexing can be retried later.
        validate = getattr(self.store, 'source_envelope', source_envelope)
        envs = [validate(e) for e in records]
        with self.lock:
            ids = [self.store.put('sources', e) for e in envs]
        prepared=self.prepare_index() if prepare else None
        return dict(status='ok', source_ids=ids, llm_calls=0, index_preparation=prepared)

    def prepare_index(self):
        """Explicit write-side preparation, never called by ask()."""
        from .indexing import prepare
        with self.lock:return prepare(self,self.store.load('sources'))

    def _index(self, sources):
        """Load only. A missing/stale generation must not trigger ingestion."""
        from .indexing import load
        return load(self,sources)

    @staticmethod
    def _witness(node, sources, number):
        text = node.get_content(metadata_mode=MetadataMode.NONE)
        prefix = f'Source {number}:\n'
        if not text.startswith(prefix) or not text.endswith('\n'):
            raise ValueError('Unexpected upstream citation format')
        quote = text[len(prefix):-1]
        if 'record_author' in node.metadata:
            header = node.get_metadata_str(mode=MetadataMode.LLM) + '\n\n'
            if not quote.startswith(header):
                raise ValueError('Citation split its provenance header; cannot map it safely')
            quote = quote[len(header):]
        sid = node.metadata['source_id']
        if 'review_witness' in node.metadata:
            # State is a separately typed, immutable citation source. It is not
            # an original report, and its offset belongs to the snapshot render.
            witness = dict(node.metadata['review_witness'])
            start = witness['quote'].find(quote)
            if not quote or start < 0:
                raise ValueError('Review citation is not verbatim in its snapshot')
            return dict(witness, quote=quote, start=start, end=start+len(quote))
        src = sources[sid]['source']
        start = src['text'].find(quote, node.metadata['parent_start'], node.metadata['parent_end'])
        if not quote or start < 0:
            raise ValueError('Citation text is not verbatim inside its original parent chunk')
        return dict(source_id=sid, quote=quote, start=start, end=start+len(quote),
                    location=src['location'], speaker=src['speaker'],
                    observed_at=sources[sid]['observed_at'])

    def _plan(self, question, trace):
        """Stages 1-4 under self.lock. None when the store has no sources.

        Returns the retriever, the selected nodes (review expansion, else None),
        the review context and the citation split settings. Sets
        self.active_review_context for readers that consume it.
        """
        from team_memory.retrieval import stages
        self.active_review_context = None
        sources = self.store.load('sources')
        if not sources:
            return None
        with trace.stage('index'):
            index = self._index(sources)
        team = self.profile == 'team'
        # Stage 1 (candidates) is replaceable. The default is the prepared index
        # plus, for the team profile, the BM25 that preparation persisted.
        make_source = getattr(self, 'candidate_source', None)
        source = make_source(index) if make_source else stages.LlamaIndexCandidates(
            index, self.top_k, sparse=self.sparse, use_sparse=team)
        # Stage 2. Retain the union: top4 dense + top4 sparse => at most8. Upstream
        # RRF ranks the union; no extra query generation or answer-key terms.
        retriever = stages.StagedRetriever(source, llm=self.llm,
            fused_top_k=2*self.top_k if team else None, trace=trace,
            turn_sources=sources if team and self.rerank_turns else None)
        citation_splitter, metadata_mode = self.splitter, MetadataMode.NONE
        if team:
            metadata_mode = MetadataMode.LLM
            # A retrieval chunk plus its short source header is one citation.
            citation_splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=0,
                tokenizer=lambda t: self.tokenizer.encode(t, add_special_tokens=False),
                include_metadata=False)
        selected_nodes, context = None, None
        if getattr(self, 'review_relations', None):
            # Stage 3: follow proposal links from the retrieved sources.
            retrieved = retriever.retrieve(question)
            with trace.stage('review_expansion'):
                selected_nodes, context = stages.expand_review(
                    retrieved, sources, self.review_relations,
                    getattr(self, 'temporal_scope', 'current'))
            trace.record('review_expansion', stages.expansion_record(len(retrieved), selected_nodes, context))
            self.active_review_context = context
            if context:
                # Stage 4. Review state as numbered, separately typed citation sources.
                with trace.stage('review_state'):
                    state_nodes = stages.review_state_nodes(self.store, context)
                trace.record('review_state', [n.node.metadata['review_witness']['proposal_id'] for n in state_nodes])
                selected_nodes.extend(state_nodes)
        return dict(sources=sources, retriever=retriever, selected_nodes=selected_nodes, context=context,
                    citation_splitter=citation_splitter, metadata_mode=metadata_mode)

    def retrieve(self, question, *, trace=None):
        """Evidence for one question: {witnesses: [...], context: review context or None}."""
        if not isinstance(question, str) or not question.strip():
            raise ValueError('Nonempty question required')
        from team_memory.retrieval import stages
        # Optional per-request diagnostics (retrieval.stages.Trace); none by default.
        trace = trace or stages.NO_TRACE
        with self.lock:
            plan = self._plan(question, trace)
            if plan is None:
                return dict(witnesses=[], context=None)
            # Stage 5: the citation split and verbatim offsets, without generation components.
            with trace.stage('citations'):
                witnesses = stages.witnesses_from_nodes(self, plan['retriever'], plan['citation_splitter'],
                                                        plan['metadata_mode'], question, plan['selected_nodes'],
                                                        plan['sources'])
            return dict(witnesses=witnesses, context=self.active_review_context)
