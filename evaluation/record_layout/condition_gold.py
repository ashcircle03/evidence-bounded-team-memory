"""Conservative development subset: one explicit simple conditional with one consequent."""
from collections import Counter
from pathlib import Path
import json
import sys

from nltk.tree import Tree


def prepare(path):
    cases, excluded = [], Counter()
    for number, line in enumerate(Path(path).read_text().splitlines(), 1):
        try:
            tree = Tree.fromstring(line)
        except ValueError:
            excluded["unparseable"] += 1
            continue
        rel = list(tree.subtrees(lambda t: t.label() == "13"))
        if len(rel) != 1:
            excluded["nested_or_multiple_relations"] += 1
            continue
        cause = list(rel[0].subtrees(lambda t: t.label() == "11"))
        if len(cause) != 1 or cause[0].leaves()[0].lower() not in {"if", "unless"}:
            excluded["no_single_explicit_if_unless"] += 1
            continue
        statements = [t for t in rel[0].subtrees(lambda t: t.label() == "10")
                      if not any(t is child for child in cause[0].subtrees())]
        if len(statements) != 1:
            excluded["ambiguous_consequent"] += 1
            continue
        text = " ".join(tree.leaves())
        condition = " ".join(cause[0].leaves())
        action = " ".join(statements[0].leaves())
        if text.count(action) != 1 or text.count(condition) != 1:
            excluded["ambiguous_span"] += 1
            continue
        cases.append(dict(id=f"requirements-dev-{number}", text=text, condition=condition, action=action))
    return dict(cases=cases, excluded=excluded)


if __name__ == "__main__":
    print(json.dumps(prepare(sys.argv[1]), ensure_ascii=False))
