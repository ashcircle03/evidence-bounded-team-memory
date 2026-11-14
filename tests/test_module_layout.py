"""Keep storage/state independent of the model reader and ship nested sources."""
import ast
import importlib
from pathlib import Path
import tempfile
import unittest

from team_memory.packaging import build, source_paths

ROOT=Path(__file__).resolve().parents[1]


class ModuleLayoutTests(unittest.TestCase):
    def test_storage_and_review_do_not_import_reader_or_service(self):
        for folder in ('storage','review'):
            for path in (ROOT/'team_memory'/folder).glob('*.py'):
                for node in ast.walk(ast.parse(path.read_text())):
                    names=([node.module or ''] if isinstance(node,ast.ImportFrom)
                           else [a.name for a in node.names] if isinstance(node,ast.Import) else [])
                    for name in names:
                        self.assertFalse(name.startswith(('team_memory.readers','team_memory.service','team_memory.experiments')),
                                         (path,name))

    def test_core_legacy_paths_share_one_implementation(self):
        for old,new in [('store','storage.objects'),('source_store','storage.sources'),('timeline','review.state'),
                        ('source_comparison','review.comparison'),('review_policy','review.policy'),('timeline_cli','review.cli')]:
            self.assertIs(importlib.import_module('team_memory.'+old),importlib.import_module('team_memory.'+new))

    def test_source_packet_includes_nested_code_and_licenses_only(self):
        names=source_paths(ROOT)
        for name in ['team_memory/storage/sources.py','team_memory/readers/checking.py',
                     'team_memory/experiments/readers/claims.py','team_memory/_vendor/langchain_citation/LICENSE']:
            self.assertIn(Path(name),names)
        self.assertFalse(any('__pycache__' in str(n) or '.safetensors' in str(n) for n in names))
        with tempfile.TemporaryDirectory() as directory:
            archive=Path(directory)/'code.tar.gz';manifest=build(ROOT,archive)
            self.assertEqual(set(manifest),set(map(str,names)))
            with self.assertRaises(FileExistsError):build(ROOT,archive)


if __name__=='__main__':unittest.main()
