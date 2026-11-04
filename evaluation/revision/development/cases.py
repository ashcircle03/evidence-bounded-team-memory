"""Replay order is explicit. Synthetic cases and original Aimers passages are kept separate."""
import json
from pathlib import Path

GOAL = "Find a better eligible candidate for the current release."
OLD = "We excluded the cobalt encoder from the release because it gave no gain in the standard configuration."
NEW = "In the sparse configuration we measured the cobalt encoder against the release baseline. Accuracy improved from 71 to 79 on the same split."
BLOCK = " The release policy still forbids shipping any encoder. The policy remains in effect for this release."
OPEN = " A controlled comparison of this sparse cobalt encoder against that baseline is already approved and underway."
HOPE = "We wonder whether the sparse cobalt encoder might improve accuracy. The comparison has not been run."

def source(owner, path, text, day):
    return {"owner":owner, "observed_at":f"2026-01-{day:02}T12:00:00Z",
            "source":{"speaker":owner,"location":path,"text":text}}

def cases(folder):
    decoy = source("other","notes/billing","We deferred the invoice export because the finance audit is incomplete.",1)
    for label,old,new in (("r1",OLD,NEW),("r2",OLD+BLOCK,NEW),("r3",OLD+OPEN,NEW),("r4",OLD,HOPE)):
        yield label,GOAL,[decoy,source("author","notes/decision",old,1)],source("colleague","notes/new",new,2)
    old,new=[json.loads((Path(folder)/(name+".json")).read_text()) for name in ("jaewon","seonghun")]
    yield "r5","대회 모델의 검증 성능을 높일 다음 비교를 고른다.",[decoy,old],new
