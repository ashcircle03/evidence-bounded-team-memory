"""Replay incoming records and reviews. Old snapshots remain available through Git."""
import heapq

from .relation import merge_action
from .store import capture, digest, nonempty, record


def overlap_action(old_id, old, new):
    a, b = old["scope"], new["scope"]
    for key in a.keys() & b.keys():
        if a[key] != b[key] and "*" not in (a[key], b[key]):
            return "keep_by_condition"
    if a and b and a.keys() == b.keys() and a != b:
        if all(a[k] == b[k] or a[k] == "*" for k in a) or all(a[k] == b[k] or b[k] == "*" for k in b):
            return "keep_by_condition"  # One explicit scope specializes the other.
    if a == b and old["value"].casefold() == new["value"].casefold():
        return "duplicate"
    if a and a == b and new.get("corrects") == old_id:
        return "propose_correction"
    return "unresolved"


def decision_status(proposal, votes):
    key = digest(proposal)
    choices = [votes.get((key, actor), set()) for actor in proposal["reviewers"]]
    if any(len(choice) > 1 for choice in choices):
        return "review_conflict"
    if any("reject" in choice for choice in choices):
        return "rejected"
    if all(choice == {"approve"} for choice in choices):
        return "accepted"
    return "pending"


def intake_order(records):
    """A late source can arrive after a newer one. Preserve each sender's observed Git history."""
    children = {}
    remaining = {}
    ready = []
    for key, obj in records.items():
        parents = set(obj.get("parents", []))
        remaining[key] = len(parents)
        if not parents:
            heapq.heappush(ready, (obj["observed_at"], key))
        for parent in parents:
            if parent not in records or records[parent]["issue"] != obj["issue"]:
                raise ValueError("missing or incompatible intake parent; synchronize the complete store")
            children.setdefault(parent, []).append(key)
    ordered = []
    while ready:
        _, key = heapq.heappop(ready)
        ordered.append(key)
        for child in children.get(key, []):
            remaining[child] -= 1
            if not remaining[child]:
                heapq.heappush(ready, (records[child]["observed_at"], child))
    if len(ordered) != len(records):
        raise ValueError("cycle in intake history")
    return ordered


def replay(store):
    records = store.load("records")
    votes = {}
    bases = {}
    for vote in store.load("reviews").values():
        if "basis" in vote:
            basis = vote["basis"]
            if digest(basis) != vote["proposal"] or basis["record"] != vote["record"]:
                raise ValueError("review basis does not match its proposal")
            bases.setdefault(vote["record"], {})[vote["proposal"]] = basis
        votes.setdefault((vote["proposal"], vote["actor"]), set()).add(vote["decision"])
    view = {}
    for key in intake_order(records):
        item = record(records[key])
        targets = []
        reviewers = {item["owner"]}
        for previous_id, previous in view.items():
            if previous["status"] in ("rejected", "superseded"):
                continue
            old = previous["record"]
            action = merge_action(previous_id, old, item, overlap_action)
            if not action:
                continue
            targets.append({"target": previous_id, "action": action, "status": previous["status"]})
            if action != "duplicate":
                reviewers.add(old["owner"])
        live_basis = {"record": key, "targets": targets, "reviewers": sorted(reviewers)}
        basis = live_basis
        status = decision_status(basis, votes)
        # A completed review attests to the exact snapshot its authors saw. Pulling a
        # new pending record must not roll back their already accepted decision.
        closed = [(b, decision_status(b, votes)) for b in bases.get(key, {}).values()
                  if decision_status(b, votes) != "pending"]
        if closed:
            basis, status = sorted(closed, key=lambda pair: digest(pair[0]))[0]
            if len({state for _, state in closed}) > 1:
                status = "review_conflict"
        corrected = item.get("corrects")
        if corrected:
            old_status = view.get(corrected, {}).get("status")
            usable = old_status == "accepted" or (status == "accepted" and old_status == "superseded")
            if not usable and status not in ("rejected", "review_conflict"):
                status = "needs_rebase"
            if status == "accepted":
                view[corrected]["status"] = "superseded"
        details = []
        for target in targets:
            previous = view[target["target"]]["record"]
            details.append({"action": target["action"], "previous": {"id":target["target"], "quote":previous["quote"],"location":previous["source"]["location"],"scope":previous["scope"]},
                            "incoming":{"id":key,"quote":item["quote"],"location":item["source"]["location"],"scope":item["scope"]}})
        proposal = digest(basis)
        view[key] = {"id": key, "record": item, "status": status, "proposal": proposal,
                     "basis": basis, "targets": targets, "comparisons": details,
                     "actions": sorted({t["action"] for t in targets}) or ["add"],
                     "reviewers": basis["reviewers"],
                     "approved_by": sorted(a for a in basis["reviewers"] if votes.get((proposal, a)) == {"approve"})}
    return view


def submit(store, data):
    item = record(data)
    capture(store, item)
    records = store.load("records")
    same_issue = {k: r for k, r in records.items() if r["issue"] == item["issue"]}
    for key, existing in same_issue.items():
        if record(existing) == item:
            return replay(store)[key]
    target = item.get("corrects")
    if target:
        old = records.get(target)
        if not old or old["issue"] != item["issue"] or old["observed_at"] >= item["observed_at"]:
            raise ValueError("corrects must name an earlier record on the same issue")
        if not item["scope"] or old["scope"] != item["scope"]:
            raise ValueError("a correction requires the same explicit conditions")
    ancestors = {p for r in same_issue.values() for p in r.get("parents", [])}
    heads = sorted(same_issue.keys() - ancestors)
    key = store.put("records", dict(item, parents=heads) if heads else item)
    return replay(store)[key]


def review(store, key, proposal, actor, decision):
    row = replay(store)[key]
    if row["status"] == "needs_rebase":
        raise ValueError("correction target must be active and approved; inspect its current state")
    if proposal != row["proposal"]:
        raise ValueError("proposal changed after synchronization; inspect the new target list")
    if nonempty(actor, "actor") not in row["reviewers"]:
        raise ValueError("actor is not a reviewer for this proposal")
    if decision not in ("approve", "reject"):
        raise ValueError("invalid review decision")
    vote = {"proposal": proposal, "record": key, "actor": actor, "decision": decision, "basis": row["basis"]}
    previous = store.load("reviews").values()
    if any(v["proposal"] == proposal and v["actor"] == actor and v["decision"] != decision for v in previous):
        raise ValueError("review already submitted with a different decision")
    store.put("reviews", vote)
    return replay(store)[key]


def source_disputes(sources, focus=None):
    """Provisional comparisons for unstructured reports, including writer abstentions.
    Source pairs are proposals for their owners; unlike a reviewed record, they have no vote.
    """
    from itertools import combinations
    from .relation import SINGLE, exclusive_difference
    reports=[(k,e) for k,e in sources.items() if SINGLE.search(e['source']['text'])]
    pairs=(combinations(reports,2) if focus is None else
           (((k,a),(l,b)) for k,a in reports if k==focus for l,b in reports if l!=k))
    proposals=[]
    for (k,a),(l,b) in pairs:
        if a['source']['location']==b['source']['location']:continue
        difference=exclusive_difference(a['source']['text'],b['source']['text'])
        if not difference:continue
        sides=[dict(id=key,value=value,quote=e['source']['text'],location=e['source']['location'],
                    speaker=e['source']['speaker'],observed_at=e['observed_at']) for key,e,value in zip((k,l),(a,b),difference)]
        proposals.append(dict(kind='source_comparison',action='propose_review',status='unreviewed',sides=sides,
                              reviewers=sorted({a['owner'],b['owner']})))
    return proposals
