"""Check each independent public input through the command boundary and a cold restart."""
import argparse
from collections import Counter
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from team_memory.adapters.base import request
from team_memory.adapters.records import RecordsAdapter
from team_memory.adapters.reader_bridge import evidence_from, claim_views
from team_memory.contracts.ports import CallContext
from team_memory.records.arguments import with_arguments
from team_memory.readers.scoped import model_passage


def verify(panel, reference, current):
    docs = json.loads(panel.read_text())["documents"]
    ref = json.loads(reference.read_text())
    base = {r["id"]:r["graph"] for r in map(json.loads,current.read_text().splitlines())}
    assert set(base)==set(ref["rows"])=={s["id"] for s in docs}
    actor = "public-corpus"
    ctx = CallContext("public",actor,frozenset(["records:write","records:read"]))
    counts = Counter()
    for doc in docs:
        sid = doc["id"]
        source = dict(doc, owner=actor,speaker="unknown",observed_at="2026-11-19T00:00:00Z",
                      location=sid,record_graph=base[sid])
        source = with_arguments(source,ref["rows"][sid],ref["model"]+"@"+ref["revision"])
        with TemporaryDirectory() as folder:
            def call(op,payload):
                result = RecordsAdapter(folder,"public").handle(
                    request(op,payload,workspace_id="public",request_id=op),context=ctx)
                assert result["status"]=="ok", (sid,result.get("errors"))
                return result["data"]
            call("record.append",dict(source=source,expected_revision=0,idempotency_key=sid))
            snap = call("snapshot.get",dict(snapshot_id=None))
        assert snap["sources"]==[source] and snap["proposals"]==[], sid
        hit=evidence_from(dict(source_id=sid,start=0,end=len(doc["text"]),quote=doc["text"]),snap,1)
        packets=[model_passage(v,("source_id","quote","location")) for v in claim_views([hit],snap)]
        links=[link for p in packets for link in p.get("record_arguments",{}).get("links",[])]
        assert all(l in links for l in source["record_arguments"]["links"]),sid
        counts.update(documents=1,accepted=len(source["record_arguments"]["links"]),
                      skipped=source["record_arguments"]["skipped"])
    return counts


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    for name in ("panel","reference","current"):
        parser.add_argument(name,type=Path)
    args=parser.parse_args()
    print(json.dumps(verify(args.panel,args.reference,args.current),indent=2))
