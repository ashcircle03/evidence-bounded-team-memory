"""Recover original successful reader configurations, independently of the new selector."""
from pathlib import Path
from evaluation.decision_records.build import ROOT,WORK,read,save
from evaluation.pair_selection.trial import RESULT

CAMPAIGN=WORK/"campaigns/speakermem-dev"
# Names identify complete reader outcomes, never a known answer in the prompt.
FINAL=["q04-ordinary/legacy","q05-ordinary/simple","q06-ordinary/simple","q07-ordinary/premise","q08-ordinary/simple","d01/premise","d07/premise"]
FINAL += [f"old-pep-{n}-clean/premise" for n in (615,572,597,618,669,654,553)]
FINAL += [f"old-pep-{n}-conflict/premise" for n in (572,618)]
EVER=[f"F_SH_Top01_{n}/premise" for n in ("002","013","033")]
JOBS={
    "revision-final-v1":("119273",FINAL),
    "revision-dev-v3":("119272",EVER),
    "pull-pilot-v1":("119269",["pep-680/clean/candidate"]),
    "records-read-v1":("119280",None),
    "records-read-v3":("119283",None)
}

def packets():
    all_packets=[]; references={}
    for version,(job,prefixes) in JOBS.items():
        source=read(CAMPAIGN/"source"/version/"packets.json")
        original={r["id"]:r for r in read(CAMPAIGN/"results"/f"sm-{job}.json")["calls"]}
        for p in source:
            uid=p["id"]
            if prefixes is None:
                # Replay every arm of the most recent QA interference suite.
                if not (version=="records-read-v3" or uid.startswith(("q","pep-","F_SH","related-"))):
                    continue
                group=uid
            else:
                group=next((k for k in prefixes if uid==k or uid.startswith(k+"/")),None)
                if group is None:continue
            old=original[uid]
            assert p["sha256"]==old["sha256"]
            mapped="qa/"+version+"/"+uid
            new=dict(p,id=mapped,group="qa/"+version+"/"+p.get("group",uid))
            if "max_output_tokens" not in new:
                new["max_output_tokens"]=64 if version=="pull-pilot-v1" else 192
            all_packets.append(new)
            references[mapped]=dict(version=version,group=group,original=old)
    return all_packets,references

if __name__=="__main__":
    qs,ref=packets()
    save(Path("/private/tmp/pair-qa.json"),qs)
    print(len(qs),len({(r['version'],r['group']) for r in ref.values() if JOBS[r['version']][1]}))
