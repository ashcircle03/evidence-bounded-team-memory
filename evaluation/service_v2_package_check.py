"""Exercise the shipped archive outside the checkout before allocating a GPU."""
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile


def main(archive):
    root = Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory(prefix='team-memory-package-') as temp:
        folder = Path(temp)
        with tarfile.open(archive) as tar:
            for member in tar.getmembers():
                rel = Path(member.name)
                if not member.isfile() or rel.is_absolute() or '..' in rel.parts:
                    raise ValueError('Archive must contain only explicit relative files')
                dest = folder/rel; dest.parent.mkdir(parents=True,exist_ok=True)
                dest.write_bytes(tar.extractfile(member).read())
        tests = folder/'tests'; tests.mkdir()
        (tests/'__init__.py').write_text('')
        for name in ('test_service.py', 'test_reference_qa.py', 'test_reference_review_citations.py'):
            shutil.copyfile(root/'tests'/name, tests/name)
        (folder/'.cache').symlink_to(root/'.cache', target_is_directory=True)
        env = dict(os.environ, PYTHONPATH=str(folder), TOKENIZERS_PARALLELISM='false')
        code = '''import unittest
suite=unittest.TestLoader().loadTestsFromNames(['tests.test_service', 'tests.test_reference_review_citations'])
result=unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(not result.wasSuccessful() or bool(result.skipped))
'''
        subprocess.run([sys.executable, '-c', code], cwd=folder, env=env, check=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    main(parser.parse_args().archive.resolve())
