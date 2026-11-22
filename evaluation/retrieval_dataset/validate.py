"""Audit ids, partitions, Unicode offsets and per-task visibility in the frozen dataset."""
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "v1"


def load(name):
    rows = [json.loads(s) for s in (ROOT / f"{name}.jsonl").read_text().splitlines()]
    indexed = {r["id"]: r for r in rows}
    assert len(rows) == len(indexed), name
    return indexed


def check_span(anchor, docs):
    text = docs[anchor["source_id"]]
    a, b = anchor["start"], anchor["end"]
    assert 0 <= a < b <= len(text) and text[a:b] == anchor["quote"]


def main():
    corpora, cases, gold = (load(n) for n in ("corpora", "cases", "gold"))
    assert cases.keys() == gold.keys()
    counts, source_counts = Counter(), Counter()
    seen_docs, seen_queries = {}, {}
    for corpus in corpora.values():
        pool = corpus["documents"]
        assert len({d["id"] for d in pool}) == len(pool)
        for doc in pool:
            # Identical raw text across partitions could leak examples, even under a fresh ID.
            sig = hashlib.sha256(doc["text"].encode()).digest()
            assert seen_docs.setdefault(sig, corpus["split"]) == corpus["split"]
        source_counts[corpus["id"].split("-")[0]] += len(pool)
    for cid, item in cases.items():
        corpus = corpora[item["corpus"]]
        docs = {d["id"]: d["text"] for d in corpus["documents"]}
        family = corpus["id"].split("-")[0]
        counts[family, item["task"], corpus["split"]] += 1
        expected = gold[cid]
        assert not ({"required", "category", "required_review_ids"} & item.keys())
        if item["task"] == "F02":
            history = set(item["history"])
            assert history == set(docs) - {item["incoming"]} and item["incoming"] in docs
            docs = {sid: docs[sid] for sid in history}
        else:
            assert item["query"].strip()
            assert seen_queries.setdefault(item["query"], corpus["split"]) == corpus["split"]
            states = {s["id"]: s for s in item.get("reviews", [])}
            assert set(expected.get("required_review_ids", [])) <= states.keys()
            for state in states.values():
                for side in ("previous", "incoming"):
                    check_span(state[side], docs)
        for alternatives in expected["required"]:
            assert alternatives
            for anchor in alternatives:
                check_span(anchor, docs)
    assert counts == {("sim", t, s): 50 for t in ("F02", "F05") for s in ("dev", "evaluation")} | {
        ("sq", "F05", "dev"): 100, ("sq", "F05", "evaluation"): 100, ("aimers", "F05", "diagnostic"): 3}
    for k, v in sorted(counts.items()):
        print(*k, v)
    print("Documents per source:", dict(source_counts))
    print("Distinct raw texts:", len(seen_docs))
    print("Cases with no relevant span:", Counter(cases[c]["task"] for c in cases if not gold[c]["required"]))


if __name__ == "__main__":
    main()
