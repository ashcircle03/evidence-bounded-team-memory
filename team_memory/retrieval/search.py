"""LlamaIndex source QA, with an optional reference-backed team-record profile.

The adapter only connects immutable source envelopes and numbered citations.
This is a historical/source reader, NOT an approval-aware current-state reader
or a replacement for semantic reconsideration. See docs/reference-reuse.md.
"""
from hashlib import sha256
import json
from pathlib import Path
import re
from threading import RLock

from llama_index.core.indices.prompt_helper import PromptHelper
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.query_engine import CitationQueryEngine
from llama_index.core.query_engine.citation_query_engine import CITATION_QA_TEMPLATE, CITATION_REFINE_TEMPLATE
from llama_index.core.response_synthesizers import get_response_synthesizer
from llama_index.core.schema import MetadataMode

from team_memory.storage.objects import Store, capture, digest, source_envelope
from team_memory.retrieval.retriever import Retriever


class ReferenceQA(Retriever):
    """Retrieval (inherited from Retriever) plus answer generation.

    Constructor and ask() are unchanged; ask(retrieve_only=True) is Retriever.retrieve.
    Answering readers (team_memory.readers) extend this class.
    """

    def __init__(self, store, *, llm, embed_model, tokenizer, top_k=4,
                 chunk_size=512, chunk_overlap=64, context_window=32768,
                 num_output=1024, index_dir=None, profile='standard', index_unit='chunks', rerank_turns=True):
        if profile not in ('standard', 'team'):
            raise ValueError('Unknown source-QA profile')
        if index_unit not in ('chunks', 'records'):
            raise ValueError('Unknown index unit')
        if not 0 <= chunk_overlap < chunk_size or top_k < 1:
            raise ValueError('Positive retrieval and valid chunk bounds required')
        if num_output <= 0 or context_window <= num_output + 512:
            raise ValueError('Insufficient context budget')
        if llm.metadata.num_output != num_output or llm.metadata.context_window < context_window:
            raise ValueError('LLM metadata and requested token budget must agree')
        super().__init__(store, embed_model=embed_model, tokenizer=tokenizer, llm=llm, top_k=top_k,
                         chunk_size=chunk_size, chunk_overlap=chunk_overlap, index_dir=index_dir,
                         profile=profile, index_unit=index_unit, rerank_turns=rerank_turns)
        self.context_window, self.num_output = context_window, num_output

    def ask(self, question, *, retrieve_only=False, trace=None):
        if retrieve_only:
            return self.retrieve(question, trace=trace)
        if not isinstance(question, str) or not question.strip():
            raise ValueError('Nonempty question required')
        from team_memory.retrieval import stages
        trace = trace or stages.NO_TRACE
        with self.lock:
            plan = self._plan(question, trace)
            if plan is None:
                return dict(status='insufficient', answers=[], citation_sources=[], raw='')
            qa_template, refine_template = CITATION_QA_TEMPLATE, CITATION_REFINE_TEMPLATE
            if self.profile == 'team':
                qa_template, refine_template = self._team_templates()
            if plan['context']:
                from team_memory.readers.context import contextual_templates
                qa_template, refine_template = contextual_templates((qa_template, refine_template), plan['context'])
            # Use the upstream packing algorithm with the REAL model tokenizer.
            # Leave a chat-template margin; the HTTP boundary also counts the
            # exact rendered chat before sending it. Compact may refine in >1 call.
            helper = PromptHelper(context_window=self.context_window-256, num_output=self.num_output,
                tokenizer=lambda text: self.tokenizer.encode(text, add_special_tokens=False))
            synthesizer = get_response_synthesizer(llm=self.llm, prompt_helper=helper,
                text_qa_template=qa_template, refine_template=refine_template,
                response_mode='compact')
            engine = CitationQueryEngine(plan['retriever'], llm=self.llm, response_synthesizer=synthesizer,
                text_splitter=plan['citation_splitter'], metadata_mode=plan['metadata_mode'])
            if plan['selected_nodes'] is None:
                result = engine.query(question)
            else:
                from llama_index.core.schema import QueryBundle
                result = engine.synthesize(QueryBundle(question), plan['selected_nodes'])
            raw = str(result)
            witnesses = [self._witness(n.node, plan['sources'], i) for i, n in enumerate(result.source_nodes, 1)]
            return self._format_response(question, raw, witnesses)

    def generate_scoped(self, query, evidence):
        from team_memory.readers.scoped import generate_scoped
        return generate_scoped(self.llm, query, evidence)

    def generate_evidence(self, question, witnesses, context=None):
        """Synthesize over fixed citation spans without retrieval or state writes.

        Rebuild the upstream citation node representation, including the same
        provenance headers. This is the split counterpart of ask, not a new QA
        prompt. Callers run their existing review/attribution stages afterwards.
        """
        from llama_index.core.schema import TextNode,NodeWithScore,QueryBundle
        self.active_review_context=context
        if not witnesses:return dict(status='insufficient',answers=[],citation_sources=[],raw='')
        nodes=[]
        for number,w in enumerate(witnesses,1):
            metadata={};hidden=[]
            if self.profile=='team':
                metadata['record_author']=w['speaker']
                if w.get('evidence_type')=='review_state':metadata['evidence_type']='review_state'
                else:
                    metadata['recorded_at']=w['observed_at']
                    if w.get('conditions'):
                        metadata['evidence_conditions']=json.dumps(w['conditions'],ensure_ascii=False)
                    if context:
                        from team_memory.retrieval.review_evidence import assertion_reviews
                        reviews=assertion_reviews(w,context)
                        if reviews:metadata['reviewed_assertions']=json.dumps([
                            dict(quote=r['quote'],status=r['status'],review_status=r['review_status'])
                            for r in reviews],ensure_ascii=False)
            if w.get("record_arguments", {}).get("links"):
                metadata["record_arguments"] = json.dumps(w["record_arguments"], ensure_ascii=False)
            if w.get('record_context') is not None:
                metadata['record_context']=json.dumps(w['record_context'],ensure_ascii=False)
            node=TextNode(text=w['quote'],metadata=metadata,
                          excluded_embed_metadata_keys=list(metadata),excluded_llm_metadata_keys=hidden)
            body=node.get_content(metadata_mode=MetadataMode.LLM if self.profile=='team' else MetadataMode.NONE)
            node.set_content(f'Source {number}:\n{body}\n')
            nodes.append(NodeWithScore(node=node))
        templates=self._team_templates() if self.profile=='team' else (CITATION_QA_TEMPLATE,CITATION_REFINE_TEMPLATE)
        if context:
            from team_memory.readers.context import contextual_templates
            templates=contextual_templates(templates,context)
        helper=PromptHelper(context_window=self.context_window-256,num_output=self.num_output,
                            tokenizer=lambda t:self.tokenizer.encode(t,add_special_tokens=False))
        synth=get_response_synthesizer(llm=self.llm,prompt_helper=helper,text_qa_template=templates[0],
                                      refine_template=templates[1],response_mode='compact')
        result=synth.synthesize(query=QueryBundle(question),nodes=nodes)
        return self._format_response(question,str(result),witnesses)

    def _format_response(self,question,raw,witnesses):
        return format_response(question,raw,witnesses,allow_source_labels=self.profile=='team')

    def _team_templates(self):
        from team_memory.readers.prompts import TEAM_QA_TEMPLATE, TEAM_REFINE_TEMPLATE
        return TEAM_QA_TEMPLATE, TEAM_REFINE_TEMPLATE


def source_text(number, witness, *, text=None):
    """Use the same recorded provenance in every active reader stage."""
    header = f"Source {number}:\nrecord_author: {witness['speaker']}\n"
    if witness.get('observed_at') is not None:
        header += f"recorded_at: {witness['observed_at']}\n"
    return header + (witness['quote'] if text is None else text)


def format_response(question, raw, witnesses, *, allow_source_labels=False):
    numbers = re.findall(r'\[(\d+)\]', raw)
    if allow_source_labels:
        # Representation glue only: preserve the physical model text and map its
        # explicit Source N labels to the same numbered source table. No claims,
        # citations, or evidence are invented when no label is present.
        numbers += re.findall(r'\bSource\s+(\d+)\b', raw, re.IGNORECASE)
    cited = sorted({int(n) for n in numbers})
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
    from contextlib import redirect_stdout
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--store', required=True)
    parser.add_argument('--model-path', required=True)
    parser.add_argument('--embedding-path', required=True)
    parser.add_argument('--api-base', required=True)
    parser.add_argument('--profile', choices=['standard', 'team', 'checked', 'attributed', 'joint', 'claims', 'contextual', 'connected'], default='standard')
    args = parser.parse_args()
    output = sys.stdout
    # Process boundary only: this CLI owns a sequential request loop. Library
    # classes never redirect global stdout around concurrent caller operations.
    with redirect_stdout(sys.stderr):
        parts = local_components(args.model_path, args.embedding_path, args.api_base)
        if args.profile == 'connected':
            from team_memory.experiments.readers.connected import ConnectedQA
            service = ConnectedQA(args.store, **parts)
        elif args.profile == 'contextual':
            from team_memory.experiments.readers.contextual import ContextualQA
            service = ContextualQA(args.store, **parts)
        elif args.profile == 'claims':
            from team_memory.experiments.readers.claims import ClaimEvidenceQA
            service = ClaimEvidenceQA(args.store,**parts)
        elif args.profile == 'joint':
            from team_memory.experiments.readers.joint import JointSourceQA
            service = JointSourceQA(args.store,**parts)
        elif args.profile == 'attributed':
            from team_memory.readers.attribution import AttributedQA
            service = AttributedQA(args.store,**parts)
        elif args.profile == 'checked':
            from team_memory.readers.checking import ConflictCheckedQA
            service = ConflictCheckedQA(args.store, **parts)
        else:
            service = ReferenceQA(args.store, profile=args.profile, **parts)
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
            print(json.dumps(result, ensure_ascii=False), file=output, flush=True)


if __name__ == '__main__':
    main()
