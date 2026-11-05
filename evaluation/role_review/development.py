"""Build fixed-witness counterfactuals without exposing expected verdicts to the reader."""
import json
from pathlib import Path
from evaluation.decision_records.build import save

PROBES={
    "hook": [
        "The invoked_hook variable did not reach run_hooks_opt() from run_commit_hook(), while push_to_checkout() correctly forwarded it.",
        "The invoked_hook variable did not reach run_commit_hook() from run_hooks_opt(), while push_to_checkout() correctly forwarded it.",
        'The "invoked_hook" variable passed to run_commit_hook() wasn\'t passed forward to run_hooks_opt(), as push_to_checkout() in that commit correctly did.',
    ],
    "prompt": [
        "In default zsh, PS1 is not expanded, so the branch-name variable is shown literally.",
        "In default zsh, PS1 is expanded, so the actual branch name is shown normally.",
        "zsh does not expand PS1 by default, but that commit assumed it did.",
    ],
    "reflog": [
        "After switching to lookup_commit(), lookup of null_oid() started returning non-NULL.",
        "After switching to lookup_commit(), lookup of null_oid() started returning NULL.",
        "we also started returning non-NULL for the null_oid().",
    ],
}

def build():
    archive=json.loads(Path("results/contrast_review/validation/cases.json").read_text())
    rows=[]
    for item in archive.values():
        if (item["method"],item["view"],item["scenario"])!=("referenced-review","raw","mixed") or item["topic"] not in PROBES:
            continue
        assert item["pair"] and item["other"]
        r=item["result"]
        probes=[r["rationale"],*PROBES[item["topic"]]]
        rows.append(dict(id=item["topic"],result=r,claims=probes))
    assert len(rows)==3
    save(Path("evaluation/role_review/dev-inputs.json"),rows)

if __name__=="__main__":build()
