"""One test selection for contributors and CI; pytest also collects function tests."""
import argparse
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
REFERENCE_FILES={"test_service.py", "test_comparison_contract.py", "test_source_patch.py", "test_decision_patch.py"}


def selected(suite):
    paths=[]
    for p in sorted((ROOT/'tests').glob('test_*.py')):
        reference=p.name.startswith(('test_reference_', 'test_contextual_')) or p.name in REFERENCE_FILES
        if suite=='all' or reference==(suite=='reference'):
            paths.append(str(p))
    return paths


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('suite',choices=['core','reference','all'],nargs='?',default='all')
    parser.add_argument('--fail-on-skip',action='store_true')
    args=parser.parse_args()
    import pytest

    class Skips:
        count=0
        def pytest_runtest_logreport(self,report):
            self.count+=report.skipped

    skips=Skips()
    code=pytest.main(['-q',*selected(args.suite)],plugins=[skips])
    if args.fail_on_skip and skips.count:
        print(f'{skips.count} skipped tests: required suite is incomplete',file=sys.stderr)
        return 1
    return int(code)


if __name__=='__main__':
    sys.path.insert(0,str(ROOT))
    raise SystemExit(main())
