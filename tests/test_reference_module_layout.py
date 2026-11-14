"""Old imports, private functions and monkeypatches resolve to canonical modules."""
import importlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]


class ReferenceLayoutTests(unittest.TestCase):
    def test_all_compatibility_names_preserve_module_identity(self):
        mapping=json.loads((ROOT/'docs/module-paths.json').read_text())['compatibility']
        for old,new in mapping.items():
            with self.subTest(old=old):
                self.assertIs(importlib.import_module(old),importlib.import_module(new))

    def test_legacy_patch_targets_still_reach_actual_reader(self):
        canonical=importlib.import_module('team_memory.readers.checking')
        with patch('team_memory.reference_checked.evaluate_document_support',return_value='sentinel'):
            self.assertEqual(canonical.evaluate_document_support(),'sentinel')

    def test_experimental_resources_resolve_after_move(self):
        claims=importlib.import_module('team_memory.experiments.readers.claims')
        expected=json.loads((ROOT/'team_memory/_vendor/attribute_first/prompts.json').read_text())
        self.assertEqual(claims._UPSTREAM,expected)


if __name__=='__main__':unittest.main()
