from pathlib import Path
from evaluation.contrast_review import corpus
from evaluation.decision_records.build import save,read
from evaluation.contrast_review.paths import HERE

CASES=[
 ("hook","a8cc5943338","f443246b9f","bbd837f040","4369e3a1a3",[1,3,5,6],[2,3],[1,2],
  "The invoked_hook flag/output is not forwarded from run_commit_hook to run_hooks_opt; later code therefore cannot reliably tell if the hook ran.",
  "The alternative migrates the pre-commit and prepare-commit-msg hooks to hook.h; library migration is distinct from passing back the invoked flag."),
 ("header","3b6a8db3b03","5848fb11acd","d21f842690","4627c67fa6",[1,2,3],[3,4,5],[1,2,3],
  "The enum error from unpacking is mishandled: fsck/caller tries to parse an uninitialized header or reports a parse failure instead of an unpack failure.",
  "The alternative distinguishes the oversized-header result (and the allow-unknown-type fallback); it is not the handling of generic unpack failure before parsing."),
 ("reflog","daf1d8285ee","c809798b2a","3c8150497f","57be9c6dee",[1,2,3,4],[1,2,3],[1,2,3],
  "The switch to lookup_commit makes null_oid yield non-NULL for an empty reflog, leading to an erroneous parse/error; preserve empty reflog handling.",
  "The alternative tolerates missing referenced objects in --stale-fix mode, distinct from handling a null OID while expiring an empty reflog."),
 ("prompt","8976500","1f6806cf2d","15981f4eec","1e4119c81b",[1,2],[2,3],[1,2,3],
  "The protected branch-name indirection assumes the shell expands PS1, but default zsh does not and shows the literal variable; condition the indirection on expansion.",
  "The alternative displays an optional upstream branch name rather than changing whether the shell expands PS1."),
 ("range","73a834e9e2","87f1b2d45c","8d5ccb59de","4624185a67",[1,2,3,4],[1,2,3],[1,2],
  "Moving diff configuration into range-diff stopped forwarding flags such as --no-patch or --stat; propagate caller options again.",
  "The alternative sends output to diff_option.file instead of always stdout; output destination is distinct from option propagation.")
]

def build():
    # Use exactly the round-one pairing and masking algorithm, with a new case list.
    from unittest.mock import patch
    with patch.object(corpus,"CASE",CASES):
        data,key=corpus.build()
    first=str(read(HERE/"inputs.json"))
    for c in key.values():
        assert c["report"].split("/")[-1] not in first
    for row in data:
        k=key[row["id"]]
        if k["scenario"]=="mixed" and k["view"]=="raw":
            if k["topic"]=="prompt":row["qa"]="Which shell does not expand PS1 by default?"
            if k["topic"]=="hook":row["qa"]="Which variable passed to run_commit_hook() was not forwarded to run_hooks_opt()?"
    return data,key

if __name__=="__main__":
    p=Path(__file__).parent;rows,key=build();save(p/"inputs.json",rows);save(p/"key.json",key)
