import importlib.util
import unittest



@unittest.skipUnless(importlib.util.find_spec('llama_index'), 'reference QA dependencies required')
class ReferenceFormatTests(unittest.TestCase):
    def test_control_whitespace_roundtrips_without_repairing_broken_structure(self):
        from team_memory.reference_claims import Selection
        from team_memory.reference_format import parse_model_json
        body = '{"segments":[{"source_id":1,"quote":"Born\t27 August\n1968"}]}'
        self.assertEqual(parse_model_json(Selection, body).segments[0].quote, 'Born\t27 August\n1968')
        for invalid in [body[:-1], body.replace('Born', '\x00Born'), '{"segments":[{"quote":"missing source"}]}']:
            with self.assertRaises(ValueError):
                parse_model_json(Selection, invalid)

    def test_rst_returns_original_offsets_and_rejects_semantic_edits(self):
        from team_memory.reference_format import locate_quote
        text = 'Overview\n\nEnable ``strict=True`` and raise a ``ValueError``.'
        source = {'location':'file.rst#example', 'quote':text}
        span = locate_quote('Enable strict=True and raise a ValueError.', source)
        self.assertIsNotNone(span)
        self.assertEqual(text[slice(*span)], text.split('\n\n')[1])
        for quote in ['Enable strict=False and raise a ValueError.', 'Enable strict==True and raise a ValueError.']:
            self.assertIsNone(locate_quote(quote, source))
        for value in [dict(source, location='code.py'), dict(source, quote=text+'\n\n'+text),
                      dict(source, quote='Example::\n\n    '+text.split('\n\n')[1])]:
            self.assertIsNone(locate_quote('Enable strict=True and raise a ValueError.',value))
