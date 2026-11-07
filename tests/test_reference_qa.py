"""Integration regressions with actual LlamaIndex and a fake decoder, not QA scores."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

TOKENIZER = Path(__file__).resolve().parents[1] / '.cache/qwen-tokenizer'
AVAILABLE = importlib.util.find_spec('llama_index') is not None and (TOKENIZER/'tokenizer.json').exists()


@unittest.skipUnless(AVAILABLE, 'Optional reference dependencies and cached Qwen tokenizer required')
class ReferenceQAIntegration(unittest.TestCase):
    def setUp(self):
        import httpx
        from transformers import AutoTokenizer
        from llama_index.core.embeddings import MockEmbedding
        from llama_index.llms.openai_like import OpenAILike
        from team_memory.reference_qa import ReferenceQA, guard_request
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.tokenizer = AutoTokenizer.from_pretrained(str(TOKENIZER), local_files_only=True)
        self.calls = []
        self.responder = None
        self.output = 'A ValueError is raised when an argument is exhausted before the others. [1]'

        def transport(request):
            body = json.loads(request.content)
            self.calls.append(body)
            return httpx.Response(200, json=dict(id='test', object='chat.completion', created=0,
                model='Qwen3-8B', choices=[dict(index=0, message=dict(role='assistant', content=self.responder(body) if self.responder else self.output),
                                               finish_reason='stop')],
                usage=dict(prompt_tokens=1, completion_tokens=1, total_tokens=2)))
        client = httpx.Client(transport=httpx.MockTransport(transport),
            event_hooks={'request': [guard_request(self.tokenizer, 4096)]})
        self.addCleanup(client.close)
        self.llm = OpenAILike(model='Qwen3-8B', api_base='http://localhost:9999/v1', api_key='fake',
            http_client=client, is_chat_model=True, tokenizer=self.tokenizer, context_window=4096,
            max_tokens=256, max_retries=0)
        self.embed = MockEmbedding(embed_dim=8)
        self.options = dict(llm=self.llm, embed_model=self.embed, tokenizer=self.tokenizer,
                            context_window=4096, num_output=256)
        self.service = ReferenceQA(self.temp.name, **self.options)

    def source(self, text, location='test:pep'):
        return dict(owner='author', observed_at='2026-01-01T00:00:00Z',
                    source=dict(text=text, speaker='author', location=location))

    def test_hard_wrapped_complete_citation_and_restart(self):
        from team_memory.reference_qa import ReferenceQA
        text = 'When enabled, a ``ValueError`` is\nraised if one of the arguments is exhausted before the others.'
        self.service.import_history([self.source(text)])
        self.assertEqual(self.calls, [])  # no native writer prerequisite
        result = self.service.ask('When does zip strict raise an error?')
        self.assertEqual(result['status'], 'ok')
        self.assertEqual(result['answers'][0]['evidence'][0]['quote'], text)
        self.assertEqual(result['alce']['docs'][0]['text'], text)
        restarted = ReferenceQA(self.temp.name, **self.options)
        self.assertEqual(restarted.ask('When does it raise?')['citation_sources'], result['citation_sources'])

    def test_joint_profile_uses_existing_retrieval_and_one_generation(self):
        from team_memory.reference_joint import JointSourceQA
        service=JointSourceQA(self.temp.name,**self.options)
        service.import_history([self.source('The color is amber. The second observation reports blue.')])
        self.output=json.dumps(dict(answers=[dict(answer='The first observation is amber',citations=[dict(source_id=1,quote='The color is amber.')]),dict(answer='The second observation is blue',citations=[dict(source_id=1,quote='The second observation reports blue.')])]))
        result=service.ask('What colors are recorded?')
        self.assertEqual(result['status'],'ok')
        self.assertEqual(len(result['answers']),2)
        self.assertEqual(len(self.calls),1)

    def test_document_judge_failure_returns_existing_draft(self):
        from unittest.mock import patch
        from team_memory.reference_checked import ConflictCheckedQA
        service=ConflictCheckedQA(self.temp.name,**self.options)
        service.import_history([self.source('The color is amber.')])
        self.output='The color is amber [1].'
        with patch('team_memory.reference_checked.evaluate_document_support',side_effect=TimeoutError('injected')):
            result=service.ask('What color?')
        self.assertEqual(result['raw'],self.output)
        self.assertTrue(result['answers'][0]['evidence'])
        self.assertEqual(result['status'],'partial')
        self.assertEqual(result['stage_failures'][0]['stage'],'document_review')

    def test_claims_profile_runs_selection_then_generation_with_provenance(self):
        from team_memory.reference_claims import ClaimEvidenceQA
        service=ClaimEvidenceQA(self.temp.name,**self.options)
        service.import_history([self.source('Amber is recorded. Blue is recorded.')])
        selection=dict(segments=[dict(source_id=1,quote='Amber is recorded.'),dict(source_id=1,quote='Blue is recorded.')])
        generated=dict(claims=[dict(text='Amber is recorded.',evidence=[1]),dict(text='Blue is recorded.',evidence=[2])])
        self.responder=lambda body:json.dumps(selection if len(self.calls)==1 else generated)
        result=service.ask('What is recorded?')
        self.assertEqual(result['status'],'ok');self.assertEqual(len(self.calls),2)
        self.assertEqual(len(result['claims']),2)
        self.assertIn('record_author',str(self.calls[0]['messages']))
        self.assertIn('2026-01-01',str(self.calls[1]['messages']))
        self.assertEqual(result['claims'][0]['evidence'][0]['quote'],'Amber is recorded.')

    def test_whole_document_is_not_expanded_and_exact_chat_fits(self):
        text = '\n'.join(f'Record {i}: the platform has a different documented configuration and behavior.'
                         for i in range(4000))
        self.service.import_history([self.source(text)])
        result = self.service.ask('What is documented about configuration?')
        self.assertEqual(result['status'], 'ok')
        self.assertLess(sum(len(c['quote']) for c in result['citation_sources']), len(text)//10)
        for call in self.calls:
            n = len(self.tokenizer.apply_chat_template(call['messages'], tokenize=True,
                add_generation_prompt=True, enable_thinking=False))
            self.assertLessEqual(n + call['max_tokens'], 4096)
            self.assertNotIn('source_id', json.dumps(call['messages']))

    def test_bad_citation_is_not_reported_as_verified(self):
        self.service.import_history([self.source('Some documented fact.')])
        self.output = 'A claim. [999]'
        result = self.service.ask('What fact?')
        self.assertEqual(result['status'], 'partial')
        self.assertEqual(result['answers'], [])
        self.assertTrue(result['warnings'])

    def test_failed_derived_index_does_not_poison_originals(self):
        from unittest.mock import patch
        self.service.import_history([self.source('A preserved original.')])
        with patch('team_memory.reference_qa.VectorStoreIndex', side_effect=RuntimeError('failed index')):
            with self.assertRaises(RuntimeError):
                self.service.ask('What is preserved?')
        self.assertEqual(len(self.service.store.load('sources')), 1)
        self.assertEqual(self.service.ask('What is preserved?')['status'], 'ok')

    def test_oversized_question_is_rejected_before_transport(self):
        self.service.import_history([self.source('A fact.')])
        with self.assertRaises(ValueError):
            self.service.ask('Huge question content. ' * 5000)
        self.assertEqual(self.calls, [])

    def test_team_author_metadata_and_two_original_citations_survive_restart(self):
        from team_memory.reference_qa import ReferenceQA
        self.service = ReferenceQA(self.temp.name, profile='team', **self.options)
        first = self.source('@Recipient: the tested value is amber.', 'test:first')
        first['source']['speaker'] = 'Actual Author'
        second = self.source('Under the same conditions the value is blue.', 'test:second')
        self.service.import_history([first, second])
        self.output = 'The records conflict: amber [1], blue [2].'
        result = self.service.ask('What value was tested?')
        self.assertEqual(result['status'], 'ok')
        self.assertEqual({w['quote'] for w in result['citation_sources']},
                         {first['source']['text'], second['source']['text']})
        rendered = json.dumps(self.calls[-1]['messages'])
        self.assertIn('record_author: Actual Author', rendered)
        self.assertIn('recorded_at: 2026-01-01', rendered)
        self.assertNotIn('source_id', rendered)
        self.assertEqual(len(result['answers'][0]['evidence']), 2)
        # The decoder is mocked: this tests provenance wiring, not conflict accuracy.
        restarted = ReferenceQA(self.temp.name, profile='team', **self.options)
        again = restarted.ask('What value was tested?')
        self.assertEqual(again['citation_sources'], result['citation_sources'])

    def test_team_sparse_search_recovers_outside_dense_candidates(self):
        from team_memory.reference_qa import ReferenceQA
        self.service = ReferenceQA(self.temp.name, profile='team', **self.options)
        self.service.import_history([self.source(f'Catalogue entry keynumber{i} is a preserved record.',
                                               f'test:catalogue/{i}') for i in range(20)])
        sources = self.service.store.load('sources')
        index = self.service._index(sources)
        dense = index.as_retriever(similarity_top_k=4).retrieve('Catalogue entry')
        seen = {n.node.metadata['source_id'] for n in dense}
        target = next(sid for sid in sources if sid not in seen)
        question = sources[target]['source']['text']
        # Mock embeddings are constant; sparse retrieval must supply this exact term.
        result = self.service.ask(question)
        selected = {w['source_id'] for w in result['citation_sources']}
        self.assertIn(target, selected)
        self.assertTrue(seen <= selected)
        self.assertEqual(len(self.calls), 1)
        self.assertLessEqual(len(selected), 8)

    def test_source_number_label_maps_without_rewriting_model_answer(self):
        from team_memory.reference_qa import ReferenceQA
        self.service = ReferenceQA(self.temp.name, profile='team', **self.options)
        self.service.import_history([self.source('The value is amber.')])
        self.output = 'Source 1: The value is amber.'
        result = self.service.ask('What value?')
        self.assertEqual(result['raw'], self.output)
        self.assertEqual(result['answers'][0]['evidence'][0]['quote'], 'The value is amber.')
        self.output = 'Source 999: The value is amber.'
        self.assertEqual(self.service.ask('What value?')['status'], 'partial')

    def test_upstream_judge_feedback_reuses_original_numbered_evidence(self):
        from team_memory.reference_checked import ConflictCheckedQA
        self.service = ConflictCheckedQA(self.temp.name, **self.options)
        self.service.import_history([self.source('The value is amber.', 'test:amber'),
                                     self.source('The value is blue.', 'test:blue')])
        def respond(body):
            text = '\n'.join(m['content'] for m in body['messages'])
            if text.startswith('# Document-Claim Conflict Detection'):
                document = text.split('# Document to evaluate against\n',1)[1].split('# Output format',1)[0]
                return json.dumps(dict(answer='CONTRADICTS' if 'blue' in document else 'SUPPORTS',
                                       document_snippet=document.strip(),reasoning='Mock judgment'))
            if 'DOCUMENT JUDGMENTS:' in text:
                return 'The records disagree; both source claims remain recorded [1] [2].'
            return 'The value is amber [1].'
        self.responder = respond
        result = self.service.ask('What value?')
        self.assertTrue(result['revised'])
        self.assertEqual(len(result['document_judgments']),2)
        self.assertEqual(len(self.calls),4)
        self.assertEqual(len(result['answers'][0]['evidence']),2)
        self.assertTrue(any('DOCUMENT JUDGMENTS:' in m['content'] for c in self.calls for m in c['messages']))

    def test_upstream_label_fallback_handles_unescaped_newlines(self):
        from team_memory.reference_checked import parse_judgment
        raw = '{"claim":"A line\nA second line", "answer": "CONTRADICTS"}'
        with self.assertRaises(json.JSONDecodeError):json.loads(raw)
        self.assertEqual(parse_judgment(raw),'CONTRADICTS')
        self.assertEqual(parse_judgment('```json\n{"answer":"SUPPORTS"}\n```'),'SUPPORTS')
        self.assertEqual(parse_judgment('<answer>IRRELEVANT</answer>'),'IRRELEVANT')
        self.assertEqual(parse_judgment('The claim might contradict this.'),'ERROR')

    def test_upstream_accumulate_keeps_both_document_outputs(self):
        from team_memory.reference_checked import accumulate_omitted_records
        from team_memory.reference_qa import format_response
        w=[dict(source_id='a',quote='The value is amber.',speaker='A',location='test:a',start=0,end=19),
           dict(source_id='b',quote='The value is blue.',speaker='B',location='test:b',start=0,end=18)]
        result=format_response('What value?','The value is amber [1].',w)
        result.update(draft_raw=result['raw'],revised=True,document_judgments=[
            dict(source_id='a',label='SUPPORTS',citation_numbers=[1]),
            dict(source_id='b',label='CONTRADICTS',citation_numbers=[2])])
        self.responder=lambda body: 'The value is blue [2].' if 'The value is blue.' in str(body['messages']) else 'The value is amber [1].'
        out=accumulate_omitted_records('What value?',result,self.llm,self.tokenizer)
        self.assertEqual(len(self.calls),2)
        self.assertEqual(out['generation_segments'],['The value is amber [1].','The value is blue [2].'])
        self.assertEqual(out['cited_numbers'],[1,2])
        self.assertEqual(out['generation_kind'],'llama-index-accumulate')

    @unittest.skipUnless(importlib.util.find_spec('sklearn'), 'Optional ALCE retrieval dependency required')
    def test_alce_addition_preserves_answer_bytes_and_existing_sources(self):
        from team_memory.reference_attributed import add_missing_citations
        from team_memory.reference_qa import format_response
        import nltk
        nltk.data.path.insert(0,str(TOKENIZER.parent/'reference-nltk'))
        w=[dict(source_id='a',quote='The drawing color is amber.',speaker='A',location='test:a',start=0,end=27),
           dict(source_id='b',quote='The configured delay is seven days.',speaker='B',location='test:b',start=0,end=35)]
        raw='The drawing color is amber [1].\nThe configured delay is seven days.'
        before=format_response('What color and delay?',raw,w)
        out=add_missing_citations(before)
        self.assertEqual(out['raw'],'The drawing color is amber [1].\n[2] The configured delay is seven days.')
        self.assertEqual(out['pre_citation_raw'],raw)
        self.assertEqual(out['cited_numbers'],[1,2])
        self.assertEqual(before['raw'],raw)
        self.assertFalse(out['citation_entailment_verified'])
        self.assertEqual(self.calls,[])

    @unittest.skipUnless(importlib.util.find_spec('sklearn'), 'Optional ALCE retrieval dependency required')
    def test_aqa_uses_all_contexts_and_rejects_lost_original_evidence(self):
        from team_memory.reference_attributed import repair_omitted_answer
        from team_memory.reference_qa import format_response
        w=[dict(source_id='a',quote='The value is amber.',speaker='A',location='test:a',start=0,end=19),
           dict(source_id='b',quote='The value is blue.',speaker='B',location='test:b',start=0,end=18)]
        before=format_response('What value?','The value is amber [1].',w)
        before.update(draft_raw=before['raw'],revised=True,document_judgments=[
            dict(source_id='a',label='SUPPORTS',citation_numbers=[1]),
            dict(source_id='b',label='CONTRADICTS',citation_numbers=[2])])
        self.output='The value is blue [2].'
        rejected=repair_omitted_answer('What value?',before,self.llm)
        self.assertFalse(rejected['aqa_candidate_accepted'])
        self.assertEqual(rejected['raw'],before['raw'])
        self.output='Source1 gives amber [1]; Source2 gives blue [2].'
        accepted=repair_omitted_answer('What value?',before,self.llm)
        self.assertTrue(accepted['aqa_candidate_accepted'])
        prompt=str(self.calls[-1]['messages'])
        for witness in w:self.assertIn(witness['quote'],prompt)
        self.assertNotIn('gold',prompt)

    def test_quote_attribution_preserves_answer_and_rejects_fabricated_quote(self):
        from team_memory.reference_quotes import add_quote_citations
        from team_memory.reference_qa import format_response
        import nltk
        nltk.data.path.insert(0,str(TOKENIZER.parent/'reference-nltk'))
        w=[dict(source_id='a',quote='The color is amber.',speaker='A',location='test:a',start=0,end=19),
           dict(source_id='b',quote='The delay is seven days.',speaker='B',location='test:b',start=0,end=24)]
        raw='The color is amber [1]. The delay is seven days.'
        self.output=json.dumps(dict(question='Color and delay?',answer=[dict(fact='The delay is seven days.',substring_quote=['The delay is seven days.'])]))
        out=add_quote_citations('Color and delay?',format_response('Color and delay?',raw,w),self.llm)
        self.assertEqual(out['raw'],'The color is amber [1]. [2] The delay is seven days.')
        self.assertIn(raw,str(self.calls[-1]['messages']))
        self.assertEqual(out['cited_numbers'],[1,2])
        self.output=self.output.replace('"substring_quote": ["The delay is seven days."]','"substring_quote": ["The delay is eight days."]')
        bad=add_quote_citations('Color and delay?',format_response('Color and delay?',raw,w),self.llm)
        self.assertEqual(bad['raw'],raw)
        self.assertEqual(bad['attribution_status'],'partial')
        self.output='not JSON'
        malformed=add_quote_citations('Color and delay?',format_response('Color and delay?',raw,w),self.llm)
        self.assertEqual(malformed['raw'],raw)
        self.assertTrue(malformed['quote_attribution_error'])

    def test_quote_offsets_tolerate_layout_but_not_changed_code(self):
        from team_memory.reference_quotes import quote_span
        source='Setting: ``sample[3]``\n  enables the amber\n mode.'
        quote='``sample[3]`` enables the amber mode.'
        span=quote_span(quote,source)
        self.assertIsNotNone(span)
        self.assertEqual(source[span[0]:span[1]].split(),quote.split())
        self.assertIsNone(quote_span(quote.replace('sample[3]','sample3'),source))
        self.assertIsNone(quote_span(quote.replace('amber','blue'),source))

    @unittest.skipUnless(importlib.util.find_spec('sklearn'), 'Optional ALCE retrieval dependency required')
    def test_nli_filters_attribution_without_editing_answer(self):
        from team_memory.reference_attributed import add_missing_citations
        from team_memory.reference_qa import format_response
        import nltk
        nltk.data.path.insert(0,str(TOKENIZER.parent/'reference-nltk'))
        w=[dict(source_id='a',quote='Amber drawing color mentioned in an unrelated question.',speaker='A',location='test:a',start=0,end=58),
           dict(source_id='b',quote='The actual drawing color is amber.',speaker='B',location='test:b',start=0,end=33)]
        class Verifier:
            def verify(self,docs,claim):
                return [dict(label='neutral',probabilities=[.01,.01,.98],truncated=False),
                        dict(label='entailment',probabilities=[.01,.98,.01],truncated=False)]
        raw='The drawing color is amber.'
        out=add_missing_citations(format_response('Color?',raw,w),Verifier())
        self.assertEqual(out['raw'],'[2] '+raw)
        self.assertEqual(out['pre_citation_raw'],raw)
        self.assertEqual(out['nli_citation_reviews'][0]['judgments'][1]['label'],'entailment')
        self.assertFalse(out['citation_entailment_verified'])


if __name__ == '__main__':
    unittest.main()
