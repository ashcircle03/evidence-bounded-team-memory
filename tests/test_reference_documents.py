import json
import unittest
from team_memory.reference_documents import documents, answer_from_sources, DocumentQA
from tests.test_reference_connected import source, Decoder


class DocumentTests(unittest.TestCase):
    def test_sorted_display_keeps_original_ids_and_metadata(self):
        a=source(1,'Late record'); a.update(observed_at='2025-02-02 12:00:00',location='topic/Group 2/3')
        b=source(2,'Early record'); b.update(observed_at='2025-01-01 12:00:00',location='topic/Group 1/7')
        llm=Decoder(json.dumps(dict(reasoning='',answers=[dict(answer='Early.',document_ids=[2])])))
        out=answer_from_sources('Q',[a,b],llm)
        self.assertEqual([d['document_id'] for d in documents([a,b])],[2,1])
        self.assertEqual(out['answers'][0]['evidence'],[b])
        self.assertIn('topic/Group 1/7',llm.requests[0][0].content)
        self.assertEqual(len(llm.requests),1)

    def test_quote_markup_does_not_gate_answer(self):
        w=source(1,'* ``PYTHONBREAKPOINT=0`` disables debugging.\n  This is the same bullet.')
        llm=Decoder(json.dumps(dict(reasoning='',answers=[dict(answer='0.',document_ids=[1])])))
        out=answer_from_sources('Q',[w],llm)
        self.assertEqual(out['status'],'ok')
        self.assertEqual(out['answers'][0]['evidence'],[w])

    def test_invalid_citation_keeps_uncertified_answer(self):
        llm=Decoder(json.dumps(dict(reasoning='',answers=[dict(answer='0.',document_ids=[2])])))
        out=answer_from_sources('Q',[source(1,'Only record')],llm)
        self.assertEqual(out['status'],'partial')
        self.assertEqual(out['answers'][0]['evidence'],[])
        self.assertIn('0.',out['raw'])
        self.assertIn('out_of_range_document',out['warnings'])

    def test_separate_alternatives_own_separate_evidence(self):
        ws=[source(1,'Under A use X.'),source(2,'Under B use Y.')]
        llm=Decoder(json.dumps(dict(reasoning='',answers=[dict(answer='A: X.',document_ids=[1]),dict(answer='B: Y.',document_ids=[2])])))
        out=answer_from_sources('Q',ws,llm)
        self.assertEqual([a['evidence'] for a in out['answers']],[[ws[0]],[ws[1]]])

    def test_empty_sources_no_generation_and_search_is_not_optional(self):
        class Retriever:
            def retrieve(self,q):
                self.query=q
                return []
        retriever=Retriever(); llm=Decoder()
        out=DocumentQA(retriever,llm).ask('Q')
        self.assertEqual(retriever.query,'Q')
        self.assertEqual(out['status'],'insufficient')
        self.assertEqual(llm.requests,[])

    def test_bad_span_and_coerced_id_rejected(self):
        w=source(1,'Text'); w['end']+=1
        with self.assertRaises(ValueError): documents([w])
        llm=Decoder(json.dumps(dict(reasoning='',answers=[dict(answer='X',document_ids=['1'])])))
        self.assertEqual(answer_from_sources('Q',[source(1,'X')],llm)['status'],'error')


if __name__=='__main__': unittest.main()
