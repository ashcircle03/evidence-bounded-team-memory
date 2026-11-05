"""Compare the shipped simple strategy's emitted citations with the same frozen key."""
from evaluation.decision_records.build import read, save
from evaluation.decision_records.packets import assemble, passages
from .trial import HERE, RESULT


def matching_paragraph(citation, options):
    if not citation or not citation["quote"]:
        return None
    for key, paragraph in options.items():
        if citation["location"] == paragraph["location"] and citation["quote"] in paragraph["text"]:
            return key
    return None


def compare():
    corpus = read(HERE / "corpus.json")
    cases = {c["id"]: c for c in corpus["cases"] if c["group"] == "unseen_git"}
    keys = read(HERE / "key.json")
    result = {}
    for run in read(RESULT / "live.json")["defaults"]:
        key = run["id"]
        cid, _ = key.split("/")
        case = cases[cid]
        chosen = run["result"]
        old, new, _ = assemble(case, corpus)
        target = passages(corpus["notes"][case["target"]]["raw"], "T")
        old_key = matching_paragraph(chosen.get("previous"), old)
        new_key = matching_paragraph(chosen.get("incoming"), new)
        gold_old, gold_new = keys.get(cid, ([], []))
        pair = (old_key is not None and new_key is not None
                and any(old[old_key] == target["T." + k] for k in gold_old)
                and int(new_key.split(".")[-1]) in gold_new)
        result[key] = dict(expected=case["action"], action=chosen["action"],
                           old=old_key, new=new_key, correct_pair=pair)
    assert len(result) == 2 * len(cases) == 16
    return result


if __name__ == "__main__":
    save(RESULT / "default-comparison.json", compare())
