"""Build model inputs from frozen original text, keeping all outcome labels offline."""
import argparse
from hashlib import sha256
import json
import re
from pathlib import Path
from evaluation.decision_records.build import read, save

WRITER = """From only these past work records, write one concise decision note for a teammate. Say what was chosen or set aside, why, under which observed conditions, and which numbered passage supports it. Preserve uncertainty; never invent conditions or results. Do not anticipate later developments. Use at most 90 words."""
REVIEW = """Decide whether the incoming record warrants reopening one past decision or testing it under a changed condition. The earlier observation can remain true. A related topic alone is insufficient. Choose review or keep. Cite one OLD passage and one NEW passage that actually support your explanation, even for keep. Optional notes are contextual aids only. Respond with one JSON object: {"action":"review or keep","old":"passage ID","new":"passage ID","reason":"one concrete explanation"}. Use exact IDs from the raw material."""
QA = """Answer the question using the supplied records. Optional notes are contextual aids. Cite the raw passage directly supporting the answer. Pay attention to who spoke, limits and the precise property asked about. Respond with one JSON object: {"answer":"short answer","source":"single raw passage ID"}. Do not add alternatives unless the question requires them."""


def passages(raw, prefix):
    out={}
    for i,doc in enumerate(raw,1):
        blocks=[b.strip() for b in re.split(r"\n\s*\n", doc["text"]) if b.strip()]
        for j,b in enumerate(blocks,1):
            key=f"{prefix}.{i}.{j}"
            out[key]=dict(text=b, author=doc.get("author", doc.get("speaker","")),location=doc["location"])
    return out


def display(ps):
    return [{"id":key,"speaker":p["author"],"text":p["text"]} for key,p in ps.items()]


def packet(id_,system,content,cap):
    text=json.dumps(content,ensure_ascii=False)
    return dict(id=id_,system=system,content=text,max_output_tokens=cap,
                sha256=sha256((system+"\n"+text).encode()).hexdigest())


def writers(data):
    return [packet("write/"+t, WRITER, display(passages(n["raw"],"P")),176) for t,n in data["notes"].items()]


def assemble(c,data):
    old={}
    for i,t in enumerate(c["topics"],1):
        old.update(passages(data["notes"][t]["raw"],f"O{i}"))
    later=passages([c["incoming"]],"N")
    extra=passages(c.get("raw",[]),"E")
    return old,later,extra


def judgments(data,log):
    expected=writers(data)
    rows={x["id"]:x for x in log["calls"]}
    if len(rows)!=len(expected) or any(rows[p["id"]]["sha256"]!=p["sha256"] for p in expected):
        raise ValueError("writer inputs changed")
    out=[]
    for c in data["cases"]:
        old,new,extra=assemble(c,data)
        for arm in "ABC":
            if arm=="C" and any(data["notes"][t]["human"] is None for t in c["topics"]):
                continue
            notes=[]
            if arm!="A":
                for i,t in enumerate(c["topics"],1):
                    if arm=="C":
                        note=data["notes"][t]["human"]["text"]
                    else:
                        note=rows["write/"+t]["raw"]
                        note=re.sub(r'\bP\.(\d+)\.(\d+)\b',rf'O{i}.\1.\2',note)
                    notes.append(dict(old_record=f"O{i}",note=note))
            payload=dict(old=display(old),incoming=display(new),notes=notes)
            if c["task"]=="qa":
                payload.update(reference_material=display(extra),question=c["question"])
            out.append(packet(c["id"]+"/"+arm,QA if c["task"]=="qa" else REVIEW,payload,160))
    return out


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("data",type=Path); p.add_argument("output",type=Path); p.add_argument("--writer-log",type=Path)
    a=p.parse_args();d=read(a.data)
    save(a.output,judgments(d,read(a.writer_log)) if a.writer_log else writers(d))
