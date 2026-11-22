"""Canonical JSON Schema builder. Export: python -m team_memory.contracts.schema.

The committed schema.json is generated from this small source, not maintained
separately. additionalProperties=False makes missing/renamed fields visible.
"""

import json
from .ports import MODULES, VERSION


def obj(**fields):
    return {"type": "object", "properties": fields, "required": list(fields),
            "additionalProperties": False}


def arr(item):
    return {"type": "array", "items": item}


def ref(name):
    return {"$ref": f"#/$defs/{name}"}


def enum(*values):
    return {"enum": list(values)}


def nullable(value):
    return {"anyOf": [value, {"type": "null"}]}


S = {"type": "string", "minLength": 1}
TEXT = {"type": "string"}
N = {"type": "integer", "minimum": 0}
TIME = {"type": "string", "format": "date-time"}
B = {"type": "boolean"}

OPERATIONS = {
    "record.append": "records", "proposal.submit": "records",
    "review.apply": "records", "snapshot.get": "records",
    "relations.compare": "relations", "evidence.retrieve": "retrieval", "evidence.prepare": "retrieval", "history.search": "retrieval",
    "answer.generate": "answering", "gateway.ask": "gateway",
    "gateway.ingest": "gateway", "gateway.review": "gateway",
}


def build_schema():
    d = {}
    d["span"] = obj(source_id=S, start=N, end=N, quote=S)
    d["source"] = obj(id=S, owner=S, speaker=S, observed_at=TIME,
                      location=S, text=S)
    argument_span = obj(start=N, end=N, quote=S)
    argument_link = obj(predicate=argument_span, role_question=S, argument=argument_span)
    argument_link["properties"]["role_template"] = S
    d["source"]["properties"]["record_arguments"] = obj(
        version={"const": "records.arguments/v1"}, producer=S, skipped=N,
        qualification={"const": "model_extracted_unverified"},
        links=arr(argument_link))
    d['record_graph_unit']=obj(id=S,index=N,start=N,end=N,quote=S,window_start=N,window_end=N)
    d['record_graph_claim']=obj(id=S,claim=arr(S),condition=arr(S),basis=arr(S),time=arr(S),subject=arr(S),
        stance=enum('observation','decision','proposal','uncertainty','question','unknown'),
        qualification={'const':'model_extracted_unverified'})
    d['record_graph_edge']=obj(source=S,target=S,kind=enum('contains','next','derived_from','claim','condition','basis','time','subject'))
    d['record_graph']=obj(version={'const':'records.graph/v1'},source_id=S,source_fingerprint=S,builder=S,model=S,
        status=enum('not_run','annotated','failed'),units=arr(ref('record_graph_unit')),claims=arr(ref('record_graph_claim')),
        errors=arr(S),edges=arr(ref('record_graph_edge')))
    from copy import deepcopy
    d['record_graph_claim_v2']=deepcopy(d['record_graph_claim'])
    d['record_graph_claim_v2']['properties']['basis_annotations']=arr(obj(unit_id=S,kind=enum('stated','inferred','unspecified')))
    d['record_graph_claim_v2']['required'].append('basis_annotations')
    d['record_graph_v2']=deepcopy(d['record_graph'])
    d['record_graph_v2']['properties'].update(version={'const':'records.graph/v2'},claims=arr(ref('record_graph_claim_v2')))
    d['record_graph_claim_v3']=deepcopy(d['record_graph_claim_v2'])
    d['record_graph_claim_v3']['properties']['assertions']=arr(obj(unit_ids=arr(S),stance=enum('observation','decision','proposal','uncertainty','question','unknown'),kind=enum('assertion','qualification','method','continuation')))
    d['record_graph_claim_v3']['required'].append('assertions')
    d['record_graph_v3']=deepcopy(d['record_graph_v2'])
    d['record_graph_v3']['properties'].update(version={'const':'records.graph/v3'},claims=arr(ref('record_graph_claim_v3')),status=enum('not_run','annotated','partial','failed'),diagnostics=arr(obj(path=S,reason=S)),excluded=arr(obj(start=N,end=N,quote=S,kind=enum('salutation','acknowledgement','formatting'))))
    cell = obj(start=N,end=N,quote=TEXT)
    d['record_graph_v3']['properties']['layout'] = arr({'oneOf': [
        obj(kind={'const':'table'}, start=N,end=N,cells=arr(cell),headers=arr(cell)),
        obj(kind={'const':'list'}, start=N,end=N,cells=arr(cell),label=cell)]})
    d['record_graph_v3']['required'].extend(['diagnostics','excluded'])
    d['record_context_binding']=obj(id=S,target_start=N,target_end=N,context_start=N,context_end=N,
        role=enum('condition','basis'),basis_kind=enum('stated','unspecified'))
    d['record_graph_v4']=deepcopy(d['record_graph_v3'])
    d['record_graph_v4']['properties'].update(version={'const':'records.graph/v4'},context_bindings=arr(ref('record_context_binding')))
    d['record_graph_v4']['required'].append('context_bindings')
    d["source"]["properties"]["record_graph"] = {'oneOf':[ref('record_graph'),ref('record_graph_v2'),ref('record_graph_v3'),ref('record_graph_v4')]}
    d["candidate"] = obj(
        kind=enum("coexist", "conflict", "correction", "reconsider"),
        previous=ref("span"), incoming=ref("span"), reason=S,
        previous_assertion=nullable(ref("span")),
        incoming_assertion=nullable(ref("span")))
    d['candidate']['properties'].update(comparison_snapshot_id=S,history_source_ids=arr(S))
    d["proposal"] = obj(
        id=S, candidate=ref("candidate"), reviewer=S,
        status=enum("informational", "pending", "approved", "rejected", "review_conflict"),
        effect=enum("none", "replace_assertion", "authorize_reconsideration"),
        decided_at=nullable(TIME))
    d['proposal']['properties']['history_source_ids']=arr(S)
    d["snapshot"] = obj(id=S, revision=N, as_of=TIME,
                        sources=arr(ref("source")), proposals=arr(ref("proposal")))
    d["query"] = obj(text=S, time_scope=enum("current", "historical", "unspecified"),
                     as_of=nullable(TIME), conditions=arr(S))
    d['query']['allOf'] = [{
        'if': {'properties': {'time_scope': {'const': 'historical'}}},
        'then': {'properties': {'as_of': TIME}},
        'else': {'properties': {'as_of': {'type': 'null'}}},
    }]
    d["state_record"] = obj(proposal_id=S, snapshot_id=S, text=S)
    d["evidence"] = obj(
        id=S, kind=enum("source", "review_state"),
        source_id=nullable(S), state_record=nullable(ref("state_record")),
        start=N, end=N, quote=S,
        owner=nullable(S), speaker=nullable(S), observed_at=nullable(TIME),
        location=nullable(S), conditions=arr(S))
    d["bundle"] = obj(
        snapshot=ref("snapshot"), query=ref("query"), evidence=arr(ref("evidence")),
        coverage=enum("hits", "no_hits", "incomplete"),
        unresolved_proposal_ids=arr(S))
    d["claim"] = obj(
        id=S, text=S, kind=enum("reported_fact", "state", "inference", "uncertainty"),
        evidence_ids=arr(S), conditions=arr(S), alternative_group=nullable(S))
    d['claim']['properties']['record_claim_id'] = S
    d['claim']['properties']['answer_span']=obj(start=N,end=N)
    d["answer"] = obj(
        snapshot_id=S, outcome=enum("answered", "conditional", "conflict", "abstained", "needs_clarification"),
        claims=arr(ref("claim")), reason=nullable(S))
    d['answer']['properties'].update(original_text=TEXT,
        unattributed=arr(obj(start=N,end=N,text=S)))
    d['answer']['properties']['unverified_revision']=obj(original_text=TEXT,candidate_text=TEXT,
        original_evidence_ids=arr(S),acceptance_basis={'const':'source_id_coverage_only'})
    d["issue"] = obj(
        code=enum("INVALID_INPUT", "FORBIDDEN", "NOT_FOUND", "STALE_SNAPSHOT",
                  "IDEMPOTENCY_CONFLICT", "IO_FAILURE", "MODEL_TIMEOUT",
                  "MODEL_OUTPUT_INVALID", "RETRIEVAL_FAILED", "INDEX_STALE",
                  "QUERY_UNRESOLVED", "TIME_SCOPE_UNAVAILABLE", "EVIDENCE_INVALID",
                  "UNSUPPORTED_CLAIM", "BUDGET_EXCEEDED"),
        message=S, retryable=B, item_id=nullable(S))
    d["receipt"] = obj(snapshot=ref("snapshot"), object_id=S, replayed=B)
    mutation = dict(idempotency_key=S, expected_revision=N)
    requests = {
        "record.append": obj(source=ref("source"), **mutation),
        "proposal.submit": obj(candidate=ref("candidate"), **mutation),
        "review.apply": obj(proposal_id=S, choice=enum("approve", "reject"), **mutation),
        "snapshot.get": obj(snapshot_id=nullable(S)),
        "relations.compare": obj(snapshot=ref("snapshot"), incoming_source_id=S,
                                 history_source_ids=arr(S)),
        "history.search": obj(snapshot=ref("snapshot"), incoming_source_id=S, limit={"type":"integer","minimum":1}),
        "evidence.prepare": obj(snapshot=ref("snapshot")),
        "evidence.retrieve": obj(snapshot=ref("snapshot"), query=ref("query"),
                                 max_evidence={"type": "integer", "minimum": 1}),
        "answer.generate": obj(bundle=ref("bundle")),
        "gateway.ask": obj(query=ref("query"), snapshot_id=nullable(S)),
        "gateway.ingest": obj(source=ref("source"), **mutation),
        "gateway.review": obj(proposal_id=S, choice=enum("approve", "reject"), **mutation),
    }
    requests["relations.compare"]["properties"]["history_spans"] = arr(ref("span"))
    results = {
        "record.append": ref("receipt"), "proposal.submit": ref("receipt"),
        "review.apply": ref("receipt"), "snapshot.get": ref("snapshot"),
        "relations.compare": obj(snapshot_id=S, candidates=arr(ref("candidate"))),
        "history.search": obj(snapshot_id=S, candidates=arr(ref("span"))),
        "evidence.prepare": obj(snapshot_id=S,index_key=S,source_count=N,prepared_documents=N,reused_documents=N),
        "evidence.retrieve": ref("bundle"), "answer.generate": ref("answer"),
        "gateway.ask": obj(bundle=ref("bundle"), answer=ref("answer")),
        "gateway.ingest": obj(receipt=ref("receipt"), proposal_ids=arr(S)),
        "gateway.review": ref("receipt"),
    }
    envelope = dict(contract_version={"const": VERSION}, request_id=S, workspace_id=S)
    request_variants, response_variants = [], []
    for operation, module in OPERATIONS.items():
        request = obj(**envelope, operation={"const": operation}, payload=requests[operation])
        d[f"request:{operation}"] = request
        request_variants.append(ref(f"request:{operation}"))
        statuses = ("ok", "invalid", "error") if module == 'records' else ("ok", "partial", "invalid", "error")
        for status in statuses:
            issues = arr(ref("issue"))
            issues["maxItems" if status == "ok" else "minItems"] = 0 if status == "ok" else 1
            response_variants.append(obj(
                **envelope, module={"const": module}, operation={"const": operation},
                status={"const": status}, errors=issues,
                data=results[operation] if status in ("ok", "partial") else {"type": "null"}))
    d["request"] = {"oneOf": request_variants}
    d["response"] = {"oneOf": response_variants}
    return {"$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": VERSION, "$defs": d, "oneOf": [ref("request"), ref("response")]}


if __name__ == "__main__":
    print(json.dumps(build_schema(), ensure_ascii=False, indent=2))
