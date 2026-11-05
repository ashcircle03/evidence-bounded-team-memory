from pathlib import Path
from evaluation.decision_records.build import read, save
from evaluation.pair_selection.batch_replay import recover
from evaluation.pair_selection.qa import JOBS, packets
from evaluation.pair_selection.qa_replay import historical
from .paths import OUT

if __name__ == "__main__":
    import sys
    if len(sys.argv)>1:
        rows=[p for p in recover() if JOBS[p["id"].split("/")[1]][1] is not None]
        save(Path(sys.argv[1]),rows)
    else:
        shots={r["id"]:r for r in read(OUT/"qa-generations.json")["calls"]}
        result=historical(packets()[1],shots)
        save(OUT/"qa-historical.json",result)
        print(sum(x["identical"] for x in result.values()),len(result))
