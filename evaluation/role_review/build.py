"""Five unseen Git regression reports; freeze role and contrast criteria before inference."""
from pathlib import Path
from unittest.mock import patch
from evaluation.contrast_review import corpus
from evaluation.decision_records.build import read,save,ROOT

HERE=Path(__file__).parent
CASES=[
    ("http-index","b1b8dfde69","7655b4119d","e941c48d49","63aca3f7f1",[1,2,5,9],[2,3,10],[1,2,3],
     "A dumb HTTP fetch with a remote v1 pack index fails after collision checks; the local index can conflict with the downloaded one. At minimum connect the failure/condition and prior collision check.",
     "The alternative counts downloaded objects to display progress during dumb HTTP fetches; the regression concerns storing/overwriting the index."),
    ("make-info","dad9cd7d518","4c64fb5aad","56da21392b","8af0699b7a",[1,2,3,7],[2,4,7,8,9,10],[1,2,4,5,10],
     "Sharing the cleared suffix list breaks make info's explicit rule because its use of $* depended on a recognized suffix. Must identify that dependency, not merely show a Makefile regression.",
     "The alternative establishes parent-directory prerequisites for parallel lint-docs directories; the regression is suffix expansion for make info."),
    ("freebsd-cwd","7333ed17","f4c21e89d7","3efe5d1d32","a54e938e5b",[1,2],[2,3,4],[1,3,4],
     "Changing the old cwd buffer to strbuf causes failure on long, permission-restricted FreeBSD paths; a smaller buffer can hit EACCES even though a larger one succeeds. Link the buffer change, condition and result.",
     "The alternative handles slashes in nonexistent top-level paths; it does not set the getcwd buffer or retry limit."),
    ("fsck-empty","3ba7a065527a","eb726f2d76","a3ed7552d6","33e42de0d2",[1,2],[2,3,4,5,6],[1,2],
     "Changing read-error/corruption classification leads fsck to misreport empty loose object files as a read/invalid argument error. Empty loose file, reporting behavior, and connection to the earlier decision are required.",
     "Writing an empty blob with fwrite in the alternative is distinct from reading/mapping an empty loose object file to diagnose corruption."),
    ("dir-diff","9ec26e7977","366f9cea18","1f197a1de4","86defcbe3f",[1,2,3],[2,4,5],[1,2,3],
     "Constructing the temporary left index from a subdirectory fails to add top-level-relative paths after the subdirectory argument change; distinguish the changed working directory from unmerged duplicate entries.",
     "The alternative deduplicates unmerged and modified entries for one path in dir-diff; the new report concerns the directory used to construct the temporary index."),
]
QUESTIONS={
    "freebsd-cwd":"Which error code can FreeBSD getcwd return when the buffer is too small and read permissions are missing?",
    "make-info":"Which suffix did the make info rule expect to be in the default list?"
}
def build():
    with patch.object(corpus,"CASE",CASES):
        rows,key=corpus.build()
    prior=[ROOT/"evaluation"/f for f in ("contrast_review/inputs.json","contrast_review/validation/inputs.json","fixed_review/inputs.json","pair_selection/corpus.json")]
    archives=" ".join(p.read_text() for p in prior)
    for row in rows:
        k=key[row["id"]]
        assert k["report"].split("/")[-1][:10] not in archives
        if k["topic"] in QUESTIONS and k["scenario"]=="mixed" and k["view"]=="raw":
            row["qa"]=QUESTIONS[k["topic"]]
    save(HERE/"inputs.json",rows);save(HERE/"key.json",key)

if __name__=="__main__":build()
