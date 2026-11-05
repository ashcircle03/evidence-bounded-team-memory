"""Package the frozen first-round Slurm driver with the follow-up strategy configuration."""
from pathlib import Path
import inspect
import zipfile
from evaluation.fixed_review.experiment import git
from evaluation.contrast_review.paths import HERE

def pack(out):
    src=(HERE/"experiment.py").read_text()
    changes={
        '("pairwise","fixed-review","contrast-review")':'("fixed-review","contrast-review","referenced-review")',
        'r["contrast-reversed"]=evaluate(row,fresh,"contrast-review",True)':'r["referenced-reversed"]=evaluate(row,fresh,"referenced-review",True)',
        'pull(after,DEFAULT_GOAL,reader,"contrast-review")':'pull(after,DEFAULT_GOAL,reader,"referenced-review")'
    }
    for old,new in changes.items():
        assert src.count(old)==1
        src=src.replace(old,new)
    with zipfile.ZipFile(out,"w",zipfile.ZIP_DEFLATED) as z:
        for p in sorted(Path("team_memory").glob("*.py")):z.write(p)
        z.writestr("fixture_git.py",inspect.getsource(git))
        z.writestr("__main__.py",src)
if __name__=="__main__":pack("/private/tmp/referenced-run.pyz")
