"""Frozen evidence, shared draft, existing Qwen; no retrieval or database writes.

The claim arm restores Table 10 decomposition, NOT the paper's full R-RAG
experiment. The AQA arm relocates our existing AQA prompt, NOT author few-shot
data or trained weights. These boundaries are deliberate experimental controls.
"""
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import sys
from threading import Lock, RLock
import time


DECOMPOSE = '''Instruction: Break down the following report into individual claims.
Report: {report}
Please identify each separate claim made in the report. A claim is a factual statement or opinion that expresses a belief or judgment.
List each claim on a new line, starting with “Claims: ”.'''


def digest(value):
    return sha256(json.dumps(value, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def parse_claims(raw):
    claims = []
    for line in raw.splitlines():
        line = re.sub(r'^\s*(?:[-*]|\d+[.)])\s*', '', line.strip())
        line = re.sub(r'^Claims?\s*:\s*', '', line, flags=re.I).strip()
        if line:
            claims.append(line)
    if not 1 <= len(claims) <= 20:
        raise ValueError('Decomposition outside frozen 1..20 claim bound')
    return claims


def claim_review(reader, question, draft):
    from llama_index.core.llms import ChatMessage
    from team_memory.reference_checked import (
        _LocalJudgeClient, evaluate_document_support, parse_judgment, review_messages)
    from team_memory.reference_qa import format_response, source_text
    from team_memory.review_context import current_judge_text, contextual_messages
    raw = reader.llm.chat([ChatMessage(role='user', content=DECOMPOSE.format(report=draft['raw']))]).message.content
    claims = parse_claims(raw)
    grouped = {}
    for number, w in enumerate(draft['citation_sources'], 1):
        group = grouped.setdefault(w['source_id'], dict(numbers=[], parts=[]))
        group['numbers'].append(number)
        text = current_judge_text(w, reader.active_review_context) if reader.active_review_context else w['quote']
        group['parts'].append(source_text(number, w, text=text))
    client = _LocalJudgeClient(reader.llm, reader.active_review_context)

    def judge(item):
        ci, claim, sid, group = item
        raw = evaluate_document_support(client, '\n\n'.join(group['parts']), claim, question, 'Qwen3-8B')
        return dict(claim_index=ci, claim=claim, source_id=sid,
                    citation_numbers=group['numbers'], label=parse_judgment(raw), raw=raw)

    with ThreadPoolExecutor(max_workers=4) as pool:
        judgments = list(pool.map(judge, [(i, c, sid, g) for i, c in enumerate(claims) for sid, g in grouped.items()]))
    out = deepcopy(draft)
    if any(j['label'] == 'CONTRADICTS' for j in judgments):
        messages = review_messages(question, draft['raw'], draft['citation_sources'], judgments)
        if reader.active_review_context:
            messages = contextual_messages(messages, reader.active_review_context)
        out = format_response(question, reader.llm.chat(messages).message.content,
                              draft['citation_sources'], allow_source_labels=True)
    valid = not any(j['label'] == 'ERROR' for j in judgments)
    counts = [dict(support=sum(j['label'] == 'SUPPORTS' for j in judgments if j['claim_index'] == i),
                   contradict=sum(j['label'] == 'CONTRADICTS' for j in judgments if j['claim_index'] == i))
              for i in range(len(claims))]
    out.update(draft_raw=draft['raw'], document_judgments=judgments,
               revised=any(j['label'] == 'CONTRADICTS' for j in judgments),
               decomposition_raw=raw, claims=claims, claim_counts=counts,
               cs_count=sum(c['support'] > 0 and c['contradict'] > 0 for c in counts)/len(counts) if valid else None,
               # No-evidence claims have no defined denominator: report coverage
               # separately instead of silently treating them as correct.
               cs_ratio_defined_claims=[c['contradict']/(c['support']+c['contradict'])
                                       for c in counts if c['support']+c['contradict']],
               judge_complete=valid)
    if not valid:
        out['status'] = 'partial'
        out.setdefault('warnings', []).append('Claim judge incomplete')
    return out


def main(folder):
    cfg = json.loads((folder/'config.json').read_text())
    assert os.environ.get('SLURMD_NODENAME')
    assert os.environ.get('CONDA_PREFIX') == cfg['conda_prefix']
    for name, h in cfg['code_sha256'].items():
        assert sha256((folder/'code'/name).read_bytes()).hexdigest() == h, name
    for name, h in cfg['data_sha256'].items():
        assert sha256((folder/name).read_bytes()).hexdigest() == h, name
    import httpx
    from transformers import AutoTokenizer
    from llama_index.llms.openai_like import OpenAILike
    from llama_index.core.llms import ChatMessage
    from team_memory.reference_qa import format_response, guard_request, source_text
    from team_memory.reference_checked import ConflictCheckedQA
    from team_memory.reference_attributed import aqa_messages, repair_omitted_answer
    from team_memory.reference_quotes import add_quote_citations
    from team_memory.review_context import contextual_templates, contextual_messages
    job = os.environ['SLURM_JOB_ID']
    out = Path(cfg['project'])/'results'/('reference-audit-'+job+'.json')
    assert not out.exists()
    record = dict(status='preparing', job_id=job, model_revision=cfg['model_revision'],
                  input_sha256=cfg['data_sha256']['inputs.json'], calls=0, rows=[], shared_drafts=[],
                  code_sha256=cfg['code_sha256'], data_sha256=cfg['data_sha256'])
    start = time.monotonic(); lock = Lock(); context = {}

    def save():
        record['seconds'] = time.monotonic()-start
        temp = out.with_suffix('.tmp'); temp.write_text(json.dumps(record, ensure_ascii=False, indent=2)); temp.replace(out)

    with out.with_suffix('.calls.jsonl').open('x') as trace:
        def request_hook(request):
            if not request.url.path.endswith('/chat/completions'):
                return
            with lock:
                if record['calls'] >= cfg['max_calls']:
                    raise RuntimeError('Frozen physical-call ceiling reached; no automatic retry')
                record['calls'] += 1
                request.extensions['audit_trace'] = dict(id=record['calls'], context=dict(context),
                                                        request=json.loads(request.content), start=time.monotonic())

        def response_hook(response):
            response.read()
            if 'audit_trace' not in response.request.extensions:
                return
            with lock:
                t = response.request.extensions['audit_trace']
                trace.write(json.dumps(dict(t, response=response.json(), seconds=time.monotonic()-t['start']), ensure_ascii=False)+'\n'); trace.flush()

        save()
        try:
            tokenizer = AutoTokenizer.from_pretrained(cfg['model_path'], local_files_only=True)
            with httpx.Client(trust_env=False, event_hooks={'request':[guard_request(tokenizer), request_hook], 'response':[response_hook]}) as client:
                llm = OpenAILike(model='Qwen3-8B', api_base=os.environ['PRACTICAL_MODEL_URL'], api_key='local-no-secret',
                    is_chat_model=True, is_function_calling_model=False, context_window=32768,
                    max_tokens=1024, tokenizer=tokenizer, temperature=0, timeout=180, max_retries=0,
                    http_client=client, additional_kwargs={'extra_body': {'chat_template_kwargs': {'enable_thinking':False}, 'seed':42}})
                reader = object.__new__(ConflictCheckedQA); reader.llm = llm; reader.lock = RLock()
                packets = json.loads((folder/'inputs.json').read_text())['packets']
                assert len(packets) == 45
                record['status'] = 'running'
                for pi, packet in enumerate(packets):
                    q, witnesses = packet['question'], packet['witnesses']
                    reader.active_review_context = packet['review_context']
                    identity = digest(dict(witnesses=witnesses, review_context=packet['review_context']))
                    assert identity == packet['evidence_sha256']
                    context.clear(); context.update(case_id=packet['id'], arm='shared_draft', evidence_sha256=identity)
                    template = reader._team_templates()[0]
                    if reader.active_review_context:
                        template = contextual_templates((template,), reader.active_review_context)[0]
                    prompt = template.format(context_str='\n\n'.join(source_text(i,w) for i,w in enumerate(witnesses,1)), query_str=q)
                    raw = llm.chat([ChatMessage(role='user', content=prompt)]).message.content
                    draft = format_response(q, raw, witnesses, allow_source_labels=True)
                    record['shared_drafts'].append(dict(case_id=packet['id'], raw=raw, sha256=digest(raw), evidence_sha256=identity))
                    save()
                    arms = ['direct','current','aqa_first','claim_review']
                    arms = arms[pi%4:]+arms[:pi%4]
                    for arm in arms:
                        context['arm'] = arm; first = record['calls']; begun = time.monotonic()
                        try:
                            answer = deepcopy(draft)
                            if arm == 'current':
                                answer = reader._review(q, answer)
                                answer = repair_omitted_answer(q, answer, llm, context=reader.active_review_context)
                            elif arm == 'claim_review':
                                answer = claim_review(reader, q, answer)
                                claim_diagnostics = deepcopy(answer)
                                answer = repair_omitted_answer(q, answer, llm, context=reader.active_review_context)
                                answer['pre_aqa_claim_review'] = claim_diagnostics
                            elif arm == 'aqa_first':
                                messages = aqa_messages(q, witnesses)
                                if reader.active_review_context:
                                    messages = contextual_messages(messages, reader.active_review_context)
                                answer = format_response(q, llm.chat(messages).message.content, witnesses, allow_source_labels=True)
                            before_citation = deepcopy(answer)
                            answer = add_quote_citations(q, answer, llm)
                            record['rows'].append(dict(case_id=packet['id'], split=packet['split'], arm=arm,
                                evidence_sha256=identity, shared_draft_sha256=digest(raw),
                                before_citation=before_citation, result=answer,
                                calls=record['calls']-first, seconds=time.monotonic()-begun))
                        except Exception as exc:
                            record['rows'].append(dict(case_id=packet['id'], split=packet['split'], arm=arm,
                                evidence_sha256=identity, error=type(exc).__name__+': '+str(exc),
                                calls=record['calls']-first, seconds=time.monotonic()-begun))
                            # An exhausted global budget/transport failure must not
                            # masquerade as completed low-quality model outputs.
                            if record['calls'] >= cfg['max_calls'] or isinstance(exc, httpx.TransportError):
                                raise
                        save(); print('AUDIT', packet['id'], arm, flush=True)
                assert len(record['rows']) == 180
                record['status'] = 'complete' if not any('error' in r for r in record['rows']) else 'complete_with_errors'
        except BaseException as exc:
            record.update(status='failed', error=type(exc).__name__+': '+str(exc)); raise
        finally:
            save()


if __name__ == '__main__':
    main(Path(sys.argv[1]))
