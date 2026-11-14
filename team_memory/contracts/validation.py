"""Structural and referential checks, deliberately not semantic entailment."""

from functools import lru_cache
from datetime import datetime
import re
from jsonschema import Draft202012Validator, FormatChecker
from .schema import build_schema, OPERATIONS


class ContractError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise ContractError(message)


@lru_cache(maxsize=None)
def validator(kind):
    schema = build_schema()
    schema["oneOf"] = [{"$ref": f"#/$defs/{kind}"}]
    formats = FormatChecker()

    @formats.checks('date-time', raises=(ValueError, TypeError))
    def timestamp(value):
        if not isinstance(value, str):
            return True  # The type validator supplies that error.
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}[Tt]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:[Zz]|[+-]\d{2}:\d{2})', value):
            return False
        return datetime.fromisoformat(value.upper().replace('Z', '+00:00')).tzinfo is not None

    return Draft202012Validator(schema, format_checker=formats)


def validate(kind, value):
    errors = list(validator(kind).iter_errors(value))
    if errors:
        # Bound diagnostics: the full oneOf error can embed every input document.
        error = errors[0]
        path = "/".join(str(p) for p in error.absolute_path) or "<root>"
        raise ContractError(f"{kind}: invalid {path} ({error.validator})")


def sources(snapshot):
    return {source["id"]: source for source in snapshot["sources"]}


def check_span(span, source_map):
    require(span["source_id"] in source_map, "unknown source")
    text = source_map[span["source_id"]]["text"]
    start, end = span["start"], span["end"]
    require(type(start) is int and type(end) is int, "offsets must be integers")
    require(0 <= start < end <= len(text), "span outside original text")
    require(text[start:end] == span["quote"], "quote differs from original text")


def check_candidate(candidate, snapshot):
    validate("candidate", candidate)
    source_map = sources(snapshot)
    for key in ("previous", "incoming"):
        check_span(candidate[key], source_map)
    require(candidate["previous"]["source_id"] != candidate["incoming"]["source_id"],
            "candidate must link different records")
    for key in ("previous", "incoming"):
        child, parent = candidate[key + "_assertion"], candidate[key]
        if candidate["kind"] == "correction":
            require(child is not None, "correction requires both exact assertion spans")
            check_span(child, source_map)
            require(child["source_id"] == parent["source_id"] and
                    parent["start"] <= child["start"] < child["end"] <= parent["end"],
                    "assertion must be inside its context span")
        else:
            require(child is None, "only correction can request assertion replacement")


def check_snapshot(snapshot):
    validate("snapshot", snapshot)
    require(len(sources(snapshot)) == len(snapshot["sources"]), "duplicate source ID")
    require(len({p['id'] for p in snapshot['proposals']}) == len(snapshot['proposals']),
            "duplicate proposal ID")
    for proposal in snapshot["proposals"]:
        candidate = proposal["candidate"]
        check_candidate(candidate, snapshot)
        require(proposal["reviewer"] == sources(snapshot)[candidate["previous"]["source_id"]]["owner"],
                "reviewer must be derived from original record owner")
        kind, status = candidate["kind"], proposal["status"]
        require((kind == "coexist") == (status == "informational"), "coexist is informational")
        expected = {"correction": "replace_assertion", "reconsider": "authorize_reconsideration"}
        effect = expected.get(kind, "none") if status == "approved" else "none"
        require(proposal["effect"] == effect, "approval effect exceeds relation authority")
        if status in ("pending", "informational", "review_conflict"):
            require(proposal["decided_at"] is None, "unresolved proposal has decision timestamp")


def render_state(proposal, snapshot_id):
    """Canonical evidence text for a recorded state, never a source quotation."""
    return (f"snapshot={snapshot_id}; proposal={proposal['id']}; "
            f"kind={proposal['candidate']['kind']}; status={proposal['status']}; "
            f"effect={proposal['effect']}; reviewer={proposal['reviewer']}; "
            f"decided_at={proposal['decided_at'] or 'unknown'}")


def check_bundle(bundle):
    validate("bundle", bundle)
    snapshot = bundle["snapshot"]
    check_snapshot(snapshot)
    source_map = sources(snapshot)
    proposals = {p["id"]: p for p in snapshot["proposals"]}
    ids = [e["id"] for e in bundle["evidence"]]
    require(len(ids) == len(set(ids)), "duplicate evidence ID")
    if bundle["coverage"] == "no_hits":
        require(not ids, "no_hits cannot contain evidence")
    if bundle["coverage"] == "hits":
        require(bool(ids), "hits requires evidence")
    for pid in bundle["unresolved_proposal_ids"]:
        require(pid in proposals, "unknown unresolved proposal")
        require(proposals[pid]["status"] in ("pending", "review_conflict") or
                (proposals[pid]["candidate"]["kind"] == "conflict" and
                 proposals[pid]["status"] == "approved"), "resolved proposal listed as unresolved")
    for evidence in bundle["evidence"]:
        if evidence["kind"] == "source":
            require(evidence["state_record"] is None, "source must not contain synthetic state")
            check_span(evidence, source_map)
            original = source_map[evidence["source_id"]]
            for key in ("owner", "speaker", "observed_at", "location"):
                require(evidence[key] == original[key], f"lost or changed source {key}")
        else:
            require(all(evidence[k] is None for k in
                        ("source_id", "owner", "speaker", "observed_at", "location")),
                    "state evidence must not masquerade as source metadata")
            state = evidence["state_record"]
            require(state is not None and state["proposal_id"] in proposals, "unknown state proposal")
            require(state["snapshot_id"] == snapshot["id"], "stale state evidence")
            require(state["text"] == render_state(proposals[state["proposal_id"]], snapshot["id"]),
                    "state text differs from recorded state")
            check_span({**evidence, "source_id": "state"}, {"state": {"text": state["text"]}})


def check_answer(answer, bundle):
    validate("answer", answer)
    check_bundle(bundle)
    require(answer["snapshot_id"] == bundle["snapshot"]["id"], "answer uses a different snapshot")
    evidence = {e["id"]: e for e in bundle["evidence"]}
    claims = answer["claims"]
    require(len({c['id'] for c in claims}) == len(claims), "duplicate claim ID")
    if answer["outcome"] in ("abstained", "needs_clarification"):
        require(answer["reason"] is not None, "abstention needs a reason")
    else:
        require(bool(claims), "successful answer needs claims")
    groups = {}
    for claim in claims:
        citations = claim["evidence_ids"]
        require(len(citations) == len(set(citations)), "duplicate claim citation")
        require(all(cid in evidence for cid in citations), "claim cites absent evidence")
        if claim["kind"] != "uncertainty":
            require(bool(citations), "claim has no evidence")
        if claim["kind"] == "reported_fact":
            require(any(evidence[cid]["kind"] == "source" for cid in citations), "fact needs original source")
        if claim["kind"] == "state":
            require(any(evidence[cid]["kind"] == "review_state" for cid in citations), "state needs state evidence")
        if claim["alternative_group"] is not None:
            groups.setdefault(claim["alternative_group"], []).append(claim)
    if answer["outcome"] == "conflict":
        require(any(len(group) >= 2 and len({tuple(c['evidence_ids']) for c in group}) >= 2
                    for group in groups.values()), "conflict requires separately cited alternatives")


def validate_exchange(request, response):
    """Validate wires and referential invariants; not persistence or truth."""
    validate("request", request)
    validate("response", response)
    for key in ("contract_version", "request_id", "workspace_id", "operation"):
        require(request[key] == response[key], f"response changed {key}")
    operation, payload = request["operation"], request["payload"]
    require(response["module"] == OPERATIONS[operation], "wrong module")
    # Even failed responses do not excuse malformed snapshot/evidence input.
    if "snapshot" in payload:
        check_snapshot(payload["snapshot"])
    if "bundle" in payload:
        check_bundle(payload["bundle"])
    if response["status"] in ("invalid", "error"):
        return
    data = response["data"]
    if operation == "snapshot.get":
        check_snapshot(data)
        if payload['snapshot_id'] is not None:
            require(data['id'] == payload['snapshot_id'], "wrong requested snapshot")
    elif operation in ("record.append", "proposal.submit", "review.apply", "gateway.review"):
        check_snapshot(data["snapshot"])
        if not data["replayed"]:
            require(data["snapshot"]["revision"] == payload["expected_revision"] + 1,
                    "mutation must advance exactly one revision")
        if operation == 'record.append':
            require(data['object_id'] == payload['source']['id'], 'append receipt has wrong object ID')
            require(payload['source'] in data['snapshot']['sources'], 'append receipt lost the source')
        else:
            proposals = {p['id']:p for p in data['snapshot']['proposals']}
            require(data['object_id'] in proposals, 'receipt refers to absent proposal')
            if operation == 'proposal.submit':
                require(proposals[data['object_id']]['candidate'] == payload['candidate'], 'stored candidate differs')
                expected_status = 'informational' if payload['candidate']['kind'] == 'coexist' else 'pending'
                require(proposals[data['object_id']]['status'] == expected_status, 'submit cannot approve candidate')
            else:
                require(data['object_id'] == payload['proposal_id'], 'review changed a different proposal')
    elif operation == "relations.compare":
        snapshot = payload["snapshot"]
        require(data["snapshot_id"] == snapshot["id"], "comparison uses wrong snapshot")
        require(payload['incoming_source_id'] in sources(snapshot), "unknown incoming source")
        require(all(s in sources(snapshot) for s in payload['history_source_ids']), "unknown history source")
        if response['status'] == 'partial':
            require(bool(data['candidates']), 'partial comparison must preserve a usable candidate')
        for candidate in data["candidates"]:
            check_candidate(candidate, snapshot)
            require(candidate['previous']['source_id'] in payload['history_source_ids'] and
                    candidate['incoming']['source_id'] == payload['incoming_source_id'],
                    "candidate outside requested comparison pairs")
    elif operation == "evidence.retrieve":
        check_bundle(data)
        require(data["snapshot"] == payload["snapshot"], "retrieval altered snapshot")
        require(data["query"] == payload["query"], "retrieval altered query")
        require(len(data["evidence"]) <= payload["max_evidence"], "retrieval exceeded budget")
        require((response['status'] == 'partial') == (data['coverage'] == 'incomplete'),
                'incomplete retrieval must be partial')
    elif operation == "answer.generate":
        check_answer(data, payload["bundle"])
    elif operation == "gateway.ask":
        check_answer(data["answer"], data["bundle"])
        require(data['bundle']['query'] == payload['query'], "gateway altered query")
        if payload['snapshot_id'] is not None:
            require(data['bundle']['snapshot']['id'] == payload['snapshot_id'], "gateway changed snapshot")
    elif operation == "gateway.ingest":
        check_snapshot(data['receipt']['snapshot'])
