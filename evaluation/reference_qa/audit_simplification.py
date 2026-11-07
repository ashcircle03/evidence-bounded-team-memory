"""Offline audit of frozen outputs and real failure paths; no model/network calls.

Preserve original evaluations. Write audit artifacts to a separate directory.
Failure probes intentionally demonstrate current defects, not passing claims.
"""
from contextlib import redirect_stdout
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
from io import StringIO
import json
from pathlib import Path
from threading import Lock, RLock
from types import SimpleNamespace
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'results/reference-qa/simplify-audit-v1'


def main():
    import nltk
    nltk.data.path.insert(0, str(ROOT / '.cache/reference-nltk'))
    from team_memory.reference_qa import ReferenceQA, format_response
    from team_memory.reference_checked import ConflictCheckedQA, missing_opposing_sources
    from team_memory.reference_attributed import AttributedQA, repair_omitted_answer
    from team_memory.reference_quotes import add_quote_citations
    from llama_index.llms.openai_like import OpenAILike
    adapter = OpenAILike(model='Qwen3-8B', api_base='http://127.0.0.1:1/v1',
                         api_key='audit-no-network', max_tokens=1024, is_chat_model=True)

    read = lambda p: json.loads(p.read_text())
    latest = ROOT / 'results/reference-qa/simplify-v2'
    selected = ROOT / 'results/reference-qa/quote-normalized-v1'
    cfg = read(latest / 'config.json')
    freeze = read(latest / 'freeze.json')
    for name, expected in {**cfg['code_sha256'], **freeze['evaluation_sha256']}.items():
        assert sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
    for name, expected in freeze['previous_sha256'].items():
        assert sha256((selected / name).read_bytes()).hexdigest() == expected, name

    # Re-execute the complete post-retrieval path, including actual document
    # judgment/revision calls skipped by the earlier17-call enrichment replay.
    old_cards = read(selected / 'cards.json')
    old_calls = [json.loads(line) for line in (selected / 'calls.jsonl').read_text().splitlines()]
    used, drafts, replayed = [], [], []
    used_lock = Lock()
    for cid, card in old_cards.items():
        context = dict(case_id=card['case_id'], label=card['label'])
        physical = [c for c in old_calls if c['context'] == context]
        first = min(physical, key=lambda c: c['id'])
        expected = card['result']
        assert first['response']['choices'][0]['message']['content'] == expected['draft_raw']
        drafts.append(first['id'])

        class Replay:
            def chat(self, messages, **kwargs):
                actual = [dict(role=m.role.value, content=m.content) for m in messages]
                matches = [c for c in physical if c['request']['messages'] == actual]
                assert len(matches) == 1, (cid, len(matches))
                call = matches[0]
                if 'max_tokens' in kwargs:
                    # Audit the installed adapter's effective HTTP setting. Its
                    # instance max_tokens overrides the per-chat384 request.
                    effective = adapter._get_model_kwargs(**kwargs)['max_tokens']
                    assert effective == call['request']['max_tokens']
                with used_lock:
                    assert call['id'] not in used
                    used.append(call['id'])
                return SimpleNamespace(message=SimpleNamespace(
                    content=call['response']['choices'][0]['message']['content']))

        question = expected['alce']['question']
        draft = format_response(question, expected['draft_raw'], expected['citation_sources'],
                                allow_source_labels=True)
        service = object.__new__(AttributedQA)
        service.lock, service.llm = RLock(), Replay()
        with patch.object(ReferenceQA, 'ask', return_value=deepcopy(draft)):
            result = service.ask(question)
        assert result['raw'] == expected['raw'], cid
        assert result['answers'] == expected['answers'], cid
        assert result['status'] == expected['status'], cid
        replayed.append(cid)
    assert len(replayed) == 20
    assert set(used + drafts) == {c['id'] for c in old_calls}

    witness = dict(source_id='audit-a', speaker='A', location='audit:a',
                   start=0, end=18, quote='Amber is recorded.')
    previous = format_response('What is recorded?', 'Amber is recorded. Answer: Amber [1].', [witness])

    class Broken:
        def chat(self, *args, **kwargs):
            raise TimeoutError('offline injected timeout')

    # Exercise the unmodified vendor's real exception handler, rather than
    # monkeypatching evaluate_document_support to throw past that handler.
    stdout = StringIO()
    service = object.__new__(ConflictCheckedQA)
    service.lock, service.llm = RLock(), Broken()
    with redirect_stdout(stdout), patch.object(ReferenceQA, 'ask', return_value=deepcopy(previous)):
        failed_review = service.ask('What is recorded?')
    transport = dict(status=failed_review['status'],
                     answer_preserved=failed_review['answers'] == previous['answers'],
                     stdout=stdout.getvalue(),
                     stdout_is_empty=not stdout.getvalue(),
                     judge_labels=[j['label'] for j in failed_review['document_judgments']])

    class InvalidJSON:
        def chat(self, *args, **kwargs):
            return SimpleNamespace(message=SimpleNamespace(content='not-json'))

    malformed = add_quote_citations('What is recorded?', deepcopy(previous), InvalidJSON())
    malformed_probe = {k: malformed.get(k) for k in
                       ['status', 'warnings', 'attribution_status', 'quote_attribution_error', 'stage_failures']}
    malformed_probe['answer_preserved'] = malformed['answers'] == previous['answers']

    # An accepted AQA candidate can reset a prior incomplete-review status.
    other = dict(witness, source_id='audit-b', speaker='B', location='audit:b',
                 quote='Blue is recorded.', end=17)
    partial = format_response('What?', 'Amber [1].', [witness, other])
    partial.update(status='partial', warnings=['Conflict review incomplete'],
                   draft_raw=partial['raw'], revised=True,
                   document_judgments=[dict(source_id='audit-a', label='ERROR'),
                                       dict(source_id='audit-b', label='CONTRADICTS')])

    class Both:
        def chat(self, *args, **kwargs):
            return SimpleNamespace(message=SimpleNamespace(content='Amber [1]. Blue [2].'))

    repaired = repair_omitted_answer('What?', partial, Both())
    partial_probe = dict(before_status=partial['status'], after_status=repaired['status'],
                         after_warnings=repaired['warnings'], accepted=repaired['aqa_candidate_accepted'],
                         remaining_error_labels=[j for j in repaired['document_judgments'] if j['label']=='ERROR'])

    cards = read(latest / 'cards.json')
    calls = [json.loads(line) for line in (latest / 'calls.jsonl').read_text().splitlines()]
    assert len(cards) == 44 and len(calls) == 83
    assert all(c['response']['choices'][0]['finish_reason'] != 'length' for c in calls)
    pairs = []
    for cid in read(ROOT / 'evaluation/reference_qa/simplify/inputs.json')['cases']:
        name = cid['id']
        a, b = (cards[f'transfer/{name}/{arm}']['result'] for arm in ['attributed', 'joint'])
        assert a['citation_sources'] == b['citation_sources']
        pairs.append(name)
    observed_schema_errors = {}
    for label, collection in [('old20', old_cards), ('comparison44', cards)]:
        observed_schema_errors[label] = [dict(id=cid, status=c['result']['status'],
            attribution_status=c['result'].get('attribution_status'), error=c['result']['quote_attribution_error'])
            for cid, c in collection.items() if c['result'].get('quote_attribution_error')]
    row = cards['transfer/new-conflict-one-source/attributed']['result']
    within_source_guard = dict(raw=row['raw'], missing_opposing_sources=missing_opposing_sources(row),
                               document_judgments=row['document_judgments'])
    assert within_source_guard['missing_opposing_sources'] == []

    summary = dict(checked_at=datetime.now(timezone.utc).isoformat(), model_calls=0, gpu_minutes=0,
        source_and_evaluation_hashes_match=True, original_selected_cards_and_ratings_unchanged=True,
        complete_post_retrieval_replay=dict(cases=20, exact_model_calls_replayed=len(used),
            original_draft_calls_verified=len(drafts), all132_historical_calls_accounted_for=True,
            scope='All post-retrieval stages replayed; retrieval itself not re-executed and no fresh model inference'),
        new_run=dict(cases=44, calls=83, paired_retrieval_equal_cases=len(pairs), truncated_outputs=0),
        probes=dict(judge_timeout_stdout=transport, quote_schema_failure=malformed_probe,
                    partial_review_reset_by_aqa=partial_probe, within_source_guard=within_source_guard),
        judge_token_override=dict(requested_in_code=384,
            effective_adapter_max_tokens=adapter._get_model_kwargs(max_tokens=384)['max_tokens'],
            observed_old_judge_requests=[c['request']['max_tokens'] for c in old_calls
                if c['request']['messages'][0]['content'].startswith('# Document-Claim')],
            observed_new_judge_requests=[c['request']['max_tokens'] for c in calls
                if c['request']['messages'][0]['content'].startswith('# Document-Claim')]),
        observed_schema_errors=observed_schema_errors,
        inspected_code_sha256={n:sha256((ROOT/n).read_bytes()).hexdigest() for n in [
            'team_memory/reference_checked.py','team_memory/reference_attributed.py',
            'team_memory/reference_quotes.py','team_memory/reference_fallback.py','team_memory/reference_joint.py']})
    OUT.mkdir(exist_ok=True)
    (OUT/'checks.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k not in ['probes','inspected_code_sha256']}, indent=2))
    print('PROBES', json.dumps({k:v for k,v in summary['probes'].items() if k!='within_source_guard'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
