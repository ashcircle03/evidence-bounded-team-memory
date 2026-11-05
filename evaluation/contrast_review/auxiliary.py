from .corpus import CASE, paragraphs
from .paths import HERE
from evaluation.decision_records.build import read,save
from pathlib import Path

# Locked before opening the primary model outputs; each index denotes a paragraph
# in the unaltered document. All mixed and no-match runs share the same report.
OFFSETS={"scheduler":(3,4,2,3),"manual":(2,2,2,2),"reverse-index":(2,3,3,2),
         "difftool":(3,2,2,2),"quiet":(3,1,3,2),"slab":(1,2,2,12)}

def build():
    k=read(HERE/"key.json");results=[]
    for r in read(HERE/"inputs.json"):
        c=k[r["id"]]
        if c["scenario"]=="foil-only":continue
        a,b,d,n=OFFSETS[c["topic"]]
        earlier=[]
        for doc in r["prior"]:
            src=doc["source"];loc=src["location"]
            i=a if loc==c["earlier"] else b if loc==c["alternative"] else d
            earlier.append(dict(location=loc,text=paragraphs(src["text"])[i-1]))
        results.append(dict(id=r["id"],earlier=earlier,report=paragraphs(r["incoming"]["source"]["text"])[n-1]))
    return results
if __name__=="__main__":save(Path("/private/tmp/contrast-fixed.json"),build())
