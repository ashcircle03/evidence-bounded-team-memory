"""Hold the two checkout excerpts and the explainer fixed, varying only its focus sentence."""
from hashlib import sha256
import json
from pathlib import Path
import re

from team_memory.fixed_review import EXPLAIN
from team_memory.sync import DEFAULT_GOAL
from evaluation.decision_records.build import read, save
from .diagnose import HERE


def build():
    c=next(v for v in read(HERE/"inputs.json") if v["id"]=="development-checkout")
    old=c["fixed_old"]["quote"];new=c["fixed_new"]["quote"]
    spans=re.split(r"(?<=[.!?])\s+(?=[A-Z가-힣\x60])",new)
    assert len(spans)==3
    rows=[]
    for label,span in zip(("condition","cost","reference","empty"),spans+[""]):
        x=json.dumps(dict(goal=DEFAULT_GOAL,earlier=old,report=new,selected_report_sentence=span),ensure_ascii=False)
        rows.append(dict(id=label,layout=label,slot=0,system=EXPLAIN,content=x,max_output_tokens=96,
                         sha256=sha256((EXPLAIN+"\n"+x).encode()).hexdigest()))
    return rows


if __name__=="__main__":save(Path("/private/tmp/fixed-focus.json"),build())
