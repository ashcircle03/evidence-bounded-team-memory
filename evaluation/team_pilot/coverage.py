"""Inspect the frozen input for a registered answer string and source, without model outputs."""

import argparse
import hashlib
import json
from pathlib import Path
import re
from collections import defaultdict

HERE = Path(__file__).resolve().parent


def contains(text, aliases):
    words = " ".join(text.casefold().split())
    return any(
        re.search(r"(?<!\w)" + re.escape(a.casefold()) + r"(?!\w)", words)
        for a in aliases
    )


def inspect(path):
    data = path.read_bytes()
    freeze = json.loads((HERE / "freeze.json").read_text())
    if hashlib.sha256(data).hexdigest() != freeze["packet_sha256"]:
        raise ValueError("expected original frozen inputs")
    cases = json.loads((HERE / "cases.json").read_text())
    queries = {f"pep-{q['pep']}": q for q in cases["qa"]}
    rows = []
    for r in json.loads(data):
        case, phase, arm = r["id"].split("/")
        content = json.loads(r["content"])
        if case in queries:
            c = queries[case]
            suffix = f"pep-{c['pep']:04}.rst"
            matches = [
                e["id"]
                for e in content["evidence"]
                if e["source"].endswith(suffix) and contains(e["excerpt"], c["answers"])
            ]
            counter = [
                e["id"]
                for e in content["evidence"]
                if e["source"].startswith("casebook://messages/")
                and contains(e["excerpt"], c["other"])
            ]
            covered = bool(matches and (phase != "conflict" or counter))
        elif phase == "review":
            c = cases["review"][int(case.split("-")[1]) - 1]
            if c["actions"] == ["keep"]:
                continue
            matches = [
                e["id"]
                for e in content["previous"]
                if c["old_cue"].casefold() in e["excerpt"].casefold()
                and e["excerpt"] in c["previous"]
            ]
            counter = [
                e["id"]
                for e in content["new"]
                if c["new_cue"].casefold() in e["excerpt"].casefold()
            ]
            covered = bool(matches and counter)
        else:
            continue
        rows.append(
            dict(
                case=case,
                phase=phase,
                arm=arm,
                primary=matches,
                secondary=counter,
                covered=covered,
            )
        )
    summary = defaultdict(dict)
    for r in rows:
        counts = summary[r["phase"]].setdefault(r["arm"], dict(covered=0, total=0))
        counts["covered"] += int(r["covered"])
        counts["total"] += 1
    return dict(
        measure="source and registered string visible; no generated answers scored",
        summary=summary,
        rows=rows,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packets", type=Path)
    print(json.dumps(inspect(parser.parse_args().packets), indent=2))
