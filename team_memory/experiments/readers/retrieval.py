"""One feedback query expansion using the installed LlamaIndex RRF retriever.

Only original records and the user's question enter retrieval. No answers,
benchmark IDs, evidence labels or prior model answers are supplied.
"""
from copy import deepcopy
import json

from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.retrievers import QueryFusionRetriever
from llama_index.retrievers.bm25 import BM25Retriever


QUERY_PROMPT = '''Generate {num_queries} concise, different search queries to
find missing evidence needed for the user's question. Use the initial search
records to resolve the relevant person, project or event. Use only names, dates
and rule identifiers present in the question or those records. Do not guess
an answer. Search for missing companion events or applicable conditions and
exceptions, not paraphrases of the same retrieved fact. If the person is known
only through metadata, use the record_author rather than an @mention.
For an interval, seek both endpoints for the same person and task. Do not
restrict all searches to the date of the first event. For a current policy,
seek its explicit applicability or later exception without assuming newer wins.
Return exactly {num_queries} queries, one per line, without numbering or prose.
Question: {query}
Initial records:
'''


class FeedbackRetriever:
    def __init__(self, sources, tokenizer, llm, *, top_k=8):
        self.originals = {source['source_id']: deepcopy(source) for source in sources}
        self.llm, self.top_k = llm, top_k
        documents = [Document(id_=sid, text=w['quote']) for sid, w in self.originals.items()]
        splitter = SentenceSplitter(chunk_size=512, chunk_overlap=64, include_metadata=False,
            tokenizer=lambda text: tokenizer.encode(text, add_special_tokens=False))
        nodes = splitter.get_nodes_from_documents(documents)
        self.original = BM25Retriever.from_defaults(nodes=nodes, similarity_top_k=top_k)
        # BM25 uses MetadataMode.EMBED. The search key contains actual provenance;
        # the returned quote remains a slice of the untouched source body.
        metadata_nodes = deepcopy(nodes)
        for node in metadata_nodes:
            witness = self.originals[node.ref_doc_id]
            node.metadata.update(record_author=witness['speaker'],
                                 recorded_at=witness.get('observed_at') or 'unknown')
        self.metadata = BM25Retriever.from_defaults(nodes=metadata_nodes, similarity_top_k=top_k)

    def witnesses(self, nodes):
        result = []
        for match in nodes:
            node = match.node
            original = self.originals[node.ref_doc_id]
            start = original['quote'].find(node.text, node.start_char_idx or 0)
            if start < 0:
                raise ValueError('Retrieved node is not an original source slice')
            result.append(dict(original, quote=node.text,
                start=original['start']+start, end=original['start']+start+len(node.text)))
        return result

    def retrieve(self, question):
        initial = self.witnesses(self.original.retrieve(question))
        context = json.dumps([dict(record_author=w['speaker'],
            recorded_at=w.get('observed_at'), text=w['quote']) for w in initial], ensure_ascii=False)
        prompt = QUERY_PROMPT + context.replace('{', '{{').replace('}', '}}')
        fusion = QueryFusionRetriever([self.metadata], llm=self.llm, num_queries=4,
            similarity_top_k=self.top_k, mode='reciprocal_rerank',
            use_async=False, query_gen_prompt=prompt)
        retrieved = self.witnesses(fusion.retrieve(question))
        return dict(sources=retrieved, trace=dict(
            initial_sources=initial, initial_query=question,
            query_generation_prompt=prompt.format(num_queries=3, query=question),
            algorithm='llama-index-core/0.14.25 QueryFusionRetriever reciprocal_rerank',
            num_queries=4, top_k=self.top_k, provenance_in_search_key=True))
