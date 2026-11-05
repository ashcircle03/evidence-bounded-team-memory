import inspect
import sys
import zipfile
from pathlib import Path
from evaluation.fixed_review.experiment import git
from evaluation.contrast_review.paths import HERE

LOCAL=Path(__file__).parent

def pack(kind,out):
    src=(HERE/'experiment.py').read_text()
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(Path('team_memory').glob('*.py')):z.write(p)
        z.writestr('fixture_git.py',inspect.getsource(git))
        if kind=='dev':
            z.writestr('base_experiment.py',src)
            z.write(LOCAL/'reader.py','diagnostic_reader.py')
            z.write(LOCAL/'dev_runner.py','__main__.py')
        else:
            assert kind=='git'
            for old,new in {
                '("pairwise","fixed-review","contrast-review")':'("referenced-review","role-review","context-review")',
                'r["contrast-reversed"]=evaluate(row,fresh,"contrast-review",True)':'r["context-reversed"]=evaluate(row,fresh,"context-review",True)',
                'pull(after,DEFAULT_GOAL,reader,"contrast-review")':'pull(after,DEFAULT_GOAL,reader,"context-review")',
                'review=Reader(local_generator(args.model,max_new_tokens=96))':'review=Reader(local_generator(args.model,max_new_tokens=192))'
            }.items():
                assert src.count(old)==1
                src=src.replace(old,new)
            z.writestr('__main__.py',src)

if __name__=='__main__':pack(*sys.argv[1:])
