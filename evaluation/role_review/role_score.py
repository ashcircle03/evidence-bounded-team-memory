"""Present role text without strategy labels. Keep semantic ratings separate from pointer validity."""
from evaluation.contrast_review.score import card
from evaluation.decision_records.build import read,save
from .verify import OUT,HERE
from team_memory.role_review import valid_ledger

def main():
    cards={};rows={}
    def add(key,r,criterion):
        if "role_evidence" not in r:return
        if not valid_ledger(r):raise ValueError(key)
        case={}
        for role,link in r["role_evidence"].items():
            case[role]=card(cards,role,criterion,
                        [r["incoming"]["quote"],r["previous"]["quote"]],
                        {"asserted":link["assertion"]["quote"],"bound":link["evidence"]["quote"]})
        rows[key]=case
    dev=read(OUT/"development-final.json")["results"]
    devkey=read(HERE.parent/"contrast_review/validation/key.json")
    for topic,v in dev.items():
        criterion=next(k["rubric"] for k in devkey.values() if k["topic"]==topic)
        add("dev/"+topic,v["revised"],criterion)
    raw=read(OUT/"comparison.json")["results"];cases=read(HERE/"key.json")
    for cid,methods in raw.items():
        add(cid,methods["role-review"]["result"],cases[cid]["rubric"])
    save(OUT/"role-cards.json",dict(sorted(cards.items())))
    save(OUT/"role-index.json",rows)
    if (OUT/"role-ratings.json").exists():
        ratings=read(OUT/"role-ratings.json")
        assert set(ratings)==set(cards)
        result={k:{role:ratings[c]["ok"] for role,c in ids.items()} for k,ids in rows.items()}
        save(OUT/"roles.json",result)
if __name__=="__main__":main()
