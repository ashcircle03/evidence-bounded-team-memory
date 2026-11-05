import sys
from evaluation.contrast_review.paths import OUT,HERE
from evaluation.contrast_review.score import run
from evaluation.contrast_review.report import render
from evaluation.decision_records.build import read,save
from evaluation.pair_selection.qa import packets
from evaluation.pair_selection.qa_replay import historical

def score():
    out=OUT/"validation"
    run(HERE/"validation",out)
    if (out/"qa-generations.json").exists():
        rows=read(out/"qa-generations.json")["calls"]
        hist=historical(packets()[1],{r["id"]:r for r in rows})
        save(out/"qa-historical.json",hist)
        if (out/"cases.json").exists():render(HERE/"validation",out)
if __name__=="__main__":score()
