"""LlamaIndex source QA. No native memory writer, new retriever, or custom QA prompt.

The adapter only connects immutable source envelopes and numbered citations.
This is a historical/source reader, NOT an approval-aware current-state reader
or a replacement for semantic reconsideration. See docs/reference-reuse.md.
"""
from hashlib import sha256
import json
from pathlib import Path
import re
from threading import RLock

from llama_index.core import Document, StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.core.indices.prompt_helper import PromptHelper
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.query_engine import CitationQueryEngine
from llama_index.core.query_engine.citation_query_engine import CITATION_QA_TEMPLATE, CITATION_REFINE_TEMPLATE
from llama_index.core.response_synthesizers import get_response_synthesizer
from llama_index.core.schema import MetadataMode

from .store import Store, capture, digest, source_envelope


class ReferenceQA:
    def __init__(self, store, *, llm, embed_model, tokenizer, top_k=4,
                 chunk_size=512, chunk_overlap=64, context_window=32768,
                 num_output=1024, index_dir=None):
        if not 0 <= chunk_overlap < chunk_size or top_k < 1:
            raise ValueError('Positive retrieval and valid chunk bounds required')
        if num_output <= 0 or context_window <= num_output + 512:
            raise ValueError('Insufficient context budget')
        if llm.metadata.num_output != num_output or llm.metadata.context_window < context_window:
            raise ValueError('LLM metadata and requested token budget must agree')
        self.store = store if isinstance(store, Store) else Store(store)
        self.llm, self.embed_model, self.tokenizer = llm, embed_model, tokenizer
        self.top_k, self.context_window, self.num_output = top_k, context_window, num_output
        self.index_dir = Path(index_dir) if index_dir else self.store.root / 'reference-index'
        self.lock = RLock()
        self.splitter = SentenceSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap,
            tokenizer=lambda text: tokenizer.encode(text, add_special_tokens=False), include_metadata=False)
        self.index_config = dict(backend='llama-index-core/0.14.25', chunk_size=chunk_size,
            chunk_overlap=chunk_overlap, embedding=embed_model.to_dict(),
            tokenizer_sha256=sha256(tokenizer.backend_tokenizer.to_str().encode()).hexdigest())
        self.index = None
        self.index_key = None

    def import_history(self, records):
        # Validate the complete input before capturing anything. This operation
        # does not invoke either an LLM or CUPMem. Indexing can be retried later.
        envs = [source_envelope(e) for e in records]
        with self.lock:
            ids = [capture(self.store, e) for e in envs]
        return dict(status='ok', source_ids=ids, llm_calls=0)

    def _index(self, sources):
        key = digest(dict(config=self.index_config, sources=sorted(sources)))
        if self.index_key == key:
            return self.index
        directory = self.index_dir / key
        if (directory / 'complete.json').exists():
            index = load_index_from_storage(StorageContext.from_defaults(persist_dir=str(directory)),
                                             embed_model=self.embed_model)
        else:
            docs = [Document(id_=sid, text=e['source']['text'], metadata={'source_id': sid},
                excluded_embed_metadata_keys=['source_id'], excluded_llm_metadata_keys=['source_id'])
                for sid, e in sorted(sources.items())]
            nodes = self.splitter.get_nodes_from_documents(docs)
            for node in nodes:
                # CitationQueryEngine deliberately clears offsets when it splits
                # nodes again. Retain the parent bounds outside model-visible text.
                node.metadata.update(source_id=node.ref_doc_id,
                                     parent_start=node.start_char_idx, parent_end=node.end_char_idx)
                node.excluded_embed_metadata_keys = list(node.metadata)
                node.excluded_llm_metadata_keys = list(node.metadata)
            index = VectorStoreIndex(nodes, embed_model=self.embed_model)
            index.storage_context.persist(persist_dir=str(directory))
            (directory / 'complete.json').write_text(json.dumps(dict(key=key, config=self.index_config)))
        self.index, self.index_key = index, key
        return index

    @staticmethod
    def _witness(node, sources, number):
        text = node.get_content(metadata_mode=MetadataMode.NONE)
        prefix = f'Source {number}:\n'
        if not text.startswith(prefix) or not text.endswith('\n'):
            raise ValueError('Unexpected upstream citation format')
        quote = text[len(prefix):-1]
        sid = node.metadata['source_id']
        src = sources[sid]['source']
        start = src['text'].find(quote, node.metadata['parent_start'], node.metadata['parent_end'])
        if not quote or start < 0:
            raise ValueError('Citation text is not verbatim inside its original parent chunk')
        return dict(source_id=sid, quote=quote, start=start, end=start+len(quote),
                    location=src['location'], speaker=src['speaker'])

    def ask(self, question):
        if not isinstance(question, str) or not question.strip():
            raise ValueError('Nonempty question required')
        with self.lock:
            sources = self.store.load('sources')
            if not sources:
                return dict(status='insufficient', answers=[], citation_sources=[], raw='')
            index = self._index(sources)
            # Use the upstream packing algorithm with the REAL model tokenizer.
            # Leave a chat-template margin; the HTTP boundary also counts the
            # exact rendered chat before sending it. Compact may refine in >1 call.
            helper = PromptHelper(context_window=self.context_window-256, num_output=self.num_output,
                tokenizer=lambda text: self.tokenizer.encode(text, add_special_tokens=False))
            synthesizer = get_response_synthesizer(llm=self.llm, prompt_helper=helper,
                text_qa_template=CITATION_QA_TEMPLATE, refine_template=CITATION_REFINE_TEMPLATE,
                response_mode='compact')
            engine = CitationQueryEngine(index.as_retriever(similarity_top_k=self.top_k), llm=self.llm,
                response_synthesizer=synthesizer, text_splitter=self.splitter, metadata_mode=MetadataMode.NONE)
            result = engine.query(question)
            raw = str(result)
            witnesses = [self._witness(n.node, sources, i) for i, n in enumerate(result.source_nodes, 1)]
            cited = sorted({int(n) for n in re.findall(r'\[(\d+)\]', raw)})
            valid = [i for i in cited if 1 <= i <= len(witnesses)]
            warnings = []
            if not cited:
                warnings.append('No numbered citation; semantic abstention is not inferred')
            if valid != cited:
                warnings.append('Output contains an out-of-range citation number')
            return dict(status='partial' if warnings else 'ok', raw=raw, warnings=warnings,
                answers=[dict(text=raw, evidence=[witnesses[i-1] for i in valid])] if valid else [],
                citation_sources=witnesses, cited_numbers=cited,
                verification='Verbatim source/offset checks only; entailment is NOT verified',
                alce=dict(question=question, output=raw,
                          docs=[dict(title=w['location'], text=w['quote']) for w in witnesses]))


def local_components(model_path, embedding_path, api_base, *, context_window=32768,
                     num_output=1024, http_client=None):
    """Use official local-model adapters; never fall back to a paid provider."""
    from urllib.parse import urlparse
    import httpx
    from transformers import AutoTokenizer
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding
    from llama_index.llms.openai_like import OpenAILike
    url = urlparse(api_base)
    if url.scheme != 'http' or url.hostname not in ('127.0.0.1', 'localhost', '::1'):
        raise ValueError('Explicit loopback model endpoint required')
    tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
    if http_client is None:
        http_client = httpx.Client(trust_env=False)
    http_client.event_hooks.setdefault('request', []).append(guard_request(tokenizer, context_window))
    embed_model = HuggingFaceEmbedding(model_name=embedding_path, device='cpu',
        query_instruction='', text_instruction='', embed_batch_size=32, local_files_only=True)
    llm = OpenAILike(model='Qwen3-8B', api_base=api_base, api_key='local-no-secret',
        is_chat_model=True, is_function_calling_model=False, context_window=context_window,
        max_tokens=num_output, tokenizer=tokenizer, temperature=0, timeout=90, max_retries=0,
        http_client=http_client,
        additional_kwargs={'extra_body': {'chat_template_kwargs': {'enable_thinking': False}}})
    return dict(llm=llm, embed_model=embed_model, tokenizer=tokenizer,
                context_window=context_window, num_output=num_output)


def guard_request(tokenizer, context_window=32768, observe=None):
    """Thin transport check, not a context truncation/repacking algorithm."""
    def check(request):
        if not request.url.path.endswith('/chat/completions'):
            return
        body = json.loads(request.content)
        prompt_tokens = len(tokenizer.apply_chat_template(body['messages'], tokenize=True,
            add_generation_prompt=True, enable_thinking=False))
        if prompt_tokens + body['max_tokens'] > context_window:
            raise ValueError('Rendered chat plus reserved output exceeds model context; nothing sent')
        if observe:
            observe(body, prompt_tokens)
    return check


def main():
    """A JSON-lines source QA process for callers; no web UI/MCP server."""
    import argparse
    import sys
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--store', required=True)
    parser.add_argument('--model-path', required=True)
    parser.add_argument('--embedding-path', required=True)
    parser.add_argument('--api-base', required=True)
    args = parser.parse_args()
    service = ReferenceQA(args.store, **local_components(args.model_path, args.embedding_path, args.api_base))
    for line in sys.stdin:
        try:
            req = json.loads(line)
            if req['operation'] == 'import_history':
                result = service.import_history(req['records'])
            elif req['operation'] == 'ask':
                result = service.ask(req['question'])
            else:
                raise ValueError('Only import_history and source QA are supported')
        except Exception as exc:
            result = dict(status='error', error_type=type(exc).__name__, error=str(exc))
        print(json.dumps(result, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
