"""Provider-free paired cited-reader packets, separate from native CUPMem QA.

Use the existing timeline QA prompt unchanged plus the same provenance suffix
for both arms. Raw gets every visible original envelope. CUP gets only whole
original envelopes reached by the bound native-composer provenance resolver.
No relation/reviewer integration is implemented here: relations are empty and
all source assertions start reported. Passing an arbitrary approval is rejected.
"""
from __future__ import annotations

from copy import deepcopy
import json

from team_memory.store import digest as source_id
from team_memory.timeline import QA, assertion_status, witness
from .provenance import digest, resolve_composer_request
from .transfer_inputs import envelope_only


PROVENANCE_SUFFIX = """
Optional model_derived_annotations contain unverified AI-generated summaries and status labels.
They are reading aids, not original source text, independent evidence, or owner approval.
Their source_links identify only the original sources from which the selected memory was derived;
these links do not certify the summary or status as correct. Only sources contain quotable original text.
Only relations carries review status. Model-derived annotations never change review status.
"""
SYSTEM = QA + PROVENANCE_SUFFIX
SCHEMA = "cupmem-paired-cited-reader-v1"


class ReaderPacketError(ValueError):
    """Adapter input error; never score this as a native model QA failure."""


def _json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _sources(visible_sources):
    if not isinstance(visible_sources, list):
        raise ReaderPacketError("visible_sources must be the ordered original envelope list")
    try:
        return [envelope_only(source) for source in visible_sources]
    except (ValueError, TypeError, KeyError) as exc:
        raise ReaderPacketError(str(exc)) from None


def _packet(arm, sources, question, annotations, *, as_of=None, provenance=None):
    if not isinstance(question, str) or not question:
        raise ReaderPacketError("original question must be nonempty text")
    if as_of is not None and (not isinstance(as_of, str) or not as_of):
        raise ReaderPacketError("as_of must be supplied unchanged as nonempty text")
    content = dict(question=question,
                   sources=[dict(id=source_id(env), **deepcopy(env), status="reported") for env in sources],
                   relations=[], model_derived_annotations=deepcopy(annotations))
    if as_of is not None:
        content["as_of"] = as_of
    user = _json(content)
    return dict(schema=SCHEMA, ready=True, stage="cited_reader_adapter_not_native_qa", arm=arm,
                system=SYSTEM, user=user, input_sha256=digest(dict(system=SYSTEM, user=user)),
                source_ids=[source_id(env) for env in sources],
                visible_payload_sha256=digest(sources), provenance=deepcopy(provenance),
                review_status_support="not_integrated; relations empty; no owner approval inferred",
                limitations=["This cited-reader adapter is reported separately from native CUPMem QA.",
                             "Quote/answer validation checks literal support and source scope, not semantic entailment.",
                             "Whole selected source envelopes are expanded without shortening; native summaries remain explicitly model-derived."])


def build_raw_qa_packet(visible_sources, question, *, as_of=None):
    """Preserve the full current prefix in its original supplied order."""
    return _packet("raw", _sources(visible_sources), question, [], as_of=as_of)


def build_cup_qa_packet(visible_sources, question, *, request_event, trace,
                        query_label, expected_state_sha256, as_of=None):
    """Build only from bound selected attributed turns; never fall back to raw.

    A selected user turn must decode to the complete original envelope and equal
    the source at its original session position byte-for-byte in every string
    field. Session index, ID, time and turn ID must match the one-envelope-per-
    session adapter, not merely a source elsewhere in the visible prefix. A chunk
    summary, partial quotation, future source or changed metadata is an adapter
    error. Status-cause audit passages are not silently added to the reader.
    """
    visible = _sources(visible_sources)
    known = {source_id(env): env for env in visible}
    bound = resolve_composer_request(request_event, trace, query_label=query_label,
                                    query_text=question, expected_state_sha256=expected_state_sha256)
    if not bound.get("source_expansion_ready"):
        return dict(schema=SCHEMA, ready=False, arm="cupmem", stage="adapter_binding_error_not_native_qa",
                    errors=deepcopy(bound.get("binding", {}).get("errors", []) or bound.get("unresolved", [])),
                    provenance=bound, reader_packet=None)
    selected, passage_to_source, errors = [], {}, []
    for passage in bound["reader_payload"]["passages"]:
        try:
            index = passage["session_index"]
            if type(index) is not int or not 0 <= index < len(visible):
                raise ReaderPacketError("selected session index is outside the visible original prefix")
            if passage["session_id"] != f"s_{index:03d}":
                raise ReaderPacketError("selected session ID does not match its original position")
            if passage["turn_id"] != "t_0":
                raise ReaderPacketError("selected turn ID does not match the one-envelope session")
            if passage["session_time"] != visible[index]["observed_at"]:
                raise ReaderPacketError("selected session time does not match the original source")
            decoded = json.loads(passage["text"])
            env = envelope_only(decoded)
            sid = source_id(env)
            if sid not in known or env != known[sid]:
                raise ReaderPacketError("selected envelope is not an exact currently visible original source")
            if env != visible[index]:
                raise ReaderPacketError("selected envelope differs from the original source at its session position")
            selected.append(env)
            passage_to_source[passage["citation_id"]] = sid
        except (ValueError, TypeError, KeyError) as exc:
            errors.append(dict(citation_id=passage["citation_id"], error=str(exc)))
    if errors:
        return dict(schema=SCHEMA, ready=False, arm="cupmem", stage="adapter_source_mapping_error_not_native_qa",
                    errors=errors, provenance=bound, reader_packet=None)

    # Multiple selected profile references may resolve to the same exact turn;
    # the resolver already deduplicates those turns, while distinct repeated
    # arrivals remain distinct source occurrences here.
    bases = []
    for binding in bound["basis_bindings"]:
        native = binding["native_basis"]
        links = []
        for path in binding["value_provenance"]:
            link = dict(source_id=passage_to_source[path["citation_id"]],
                        original_turn_citation_id=path["citation_id"], path=deepcopy(path["path"]))
            if link not in links:
                links.append(link)
        bases.append(dict(binding_id=binding["binding_id"], role=binding["role"],
                          hit_ref=deepcopy(native["hit_ref"]), summary=native.get("text", ""),
                          native_status_label=native.get("status_label", ""),
                          source_links=links, limitations=deepcopy(binding["limitations"])))
    payload = json.loads(request_event["body"]["messages"][-1]["content"])
    grounding = payload["canonical_answer_grounding"]
    # All fields here are model-derived annotations, never promoted to relations.
    annotation = dict(origin="CUPMem native composer grounding", unverified=True, cannot_approve=True,
                      selected_bases=bases,
                      native_decision_summary={key: deepcopy(grounding[key]) for key in
                          ("corrected_current_facts", "old_premise_safe", "premise_status", "action_status")
                          if key in grounding})
    return _packet("cupmem", selected, question, [annotation], as_of=as_of,
                   provenance=dict(binding=bound["binding"], grounding_sha256=bound["grounding_sha256"],
                                   passage_to_source=passage_to_source,
                                   status_causes_excluded_from_sources=True))


def sources_from_native_record(record, *, query_label):
    """Accept only the source-only boundary produced by native_record_at."""
    if not isinstance(record, dict) or set(record) != {"uid", "haystack_session", "timestamps", "probing_queries"}:
        raise ReaderPacketError("expected source-only native record")
    sessions, dates = record["haystack_session"], record["timestamps"]
    if not isinstance(sessions, list) or len(sessions) != len(dates):
        raise ReaderPacketError("session/timestamp count mismatch")
    sources = []
    for session, date in zip(sessions, dates):
        if (not isinstance(session, list) or len(session) != 1 or
                set(session[0]) != {"role", "content"} or session[0]["role"] != "user"):
            raise ReaderPacketError("expected one attributed original user turn per session")
        try:
            env = envelope_only(json.loads(session[0]["content"]))
        except (ValueError, TypeError, KeyError) as exc:
            raise ReaderPacketError(str(exc)) from None
        if env["observed_at"] != date:
            raise ReaderPacketError("source timestamp changed")
        sources.append(env)
    question = record["probing_queries"].get(query_label)
    if not isinstance(question, str) or not question:
        raise ReaderPacketError("missing original question")
    return sources, question


def build_raw_qa_packet_from_record(record, *, query_label):
    sources, question = sources_from_native_record(record, query_label=query_label)
    return build_raw_qa_packet(sources, question)


def sources_from_legacy_payload(payload):
    """Accept legacy_inputs.model_payload, never the full evaluation artifact."""
    if not isinstance(payload, dict) or set(payload) != {"history", "question", "as_of"}:
        raise ReaderPacketError("expected legacy source-only model_payload")
    sources = []
    for row in payload["history"]:
        if set(row) != {"source_id", "owner", "observed_at", "source"}:
            raise ReaderPacketError("unexpected legacy source fields")
        env = envelope_only({key: row[key] for key in ("owner", "observed_at", "source")})
        if source_id(env) != row["source_id"]:
            raise ReaderPacketError("legacy source ID does not match exact envelope")
        sources.append(env)
    return sources, payload["question"], payload["as_of"]


def build_raw_qa_packet_from_legacy(payload):
    sources, question, as_of = sources_from_legacy_payload(payload)
    return build_raw_qa_packet(sources, question, as_of=as_of)


def _validate_packet(packet):
    if not isinstance(packet, dict) or packet.get("schema") != SCHEMA or not packet.get("ready"):
        raise ReaderPacketError("adapter packet is not ready")
    if packet.get("system") != SYSTEM:
        raise ReaderPacketError("not the shared fixed QA prompt")
    if packet.get("input_sha256") != digest(dict(system=packet["system"], user=packet["user"])):
        raise ReaderPacketError("reader packet input hash mismatch")
    data = json.loads(packet["user"])
    if set(data) not in ({"question", "sources", "relations", "model_derived_annotations"},
                         {"question", "sources", "relations", "model_derived_annotations", "as_of"}):
        raise ReaderPacketError("unexpected reader payload fields")
    if data["relations"] != []:
        raise ReaderPacketError("relation/owner adapter is not integrated; arbitrary review status is forbidden")
    by_id = {}
    ids = []
    for row in data["sources"]:
        if set(row) != {"id", "owner", "observed_at", "source", "status"} or row["status"] != "reported":
            raise ReaderPacketError("source status cannot be supplied as approval")
        env = envelope_only({key: row[key] for key in ("owner", "observed_at", "source")})
        sid = source_id(env)
        if sid != row["id"] or (sid in by_id and by_id[sid] != env):
            raise ReaderPacketError("source ID mismatch")
        ids.append(sid)
        by_id[sid] = env
    if ids != packet["source_ids"]:
        raise ReaderPacketError("source scope changed")
    return data, by_id


def parse_qa_output(raw, packet):
    """Strict JSON and existing witness/status checks; retain invalid raw output.

    Structural/exact-substring validity is separate from correctness/entailment.
    Never repair JSON, infer a missing citation, normalize a quotation, or assign
    an approval from model output or annotation text.
    """
    try:
        data, by_id = _validate_packet(packet)
    except (ValueError, KeyError, TypeError) as exc:
        return dict(kind="adapter_error", answers=[], error=str(exc), raw=raw,
                    scope="not a model QA score")
    try:
        if not isinstance(raw, str):
            raise ValueError("model output must be raw text")
        result = json.loads(raw)
        if not isinstance(result, dict) or set(result) != {"kind", "answers"}:
            raise ValueError("expected only kind and answers")
        kind, items = result["kind"], result["answers"]
        if kind not in ("single", "conditional", "conflict", "insufficient"):
            raise ValueError("answer kind")
        if not isinstance(items, list) or len(items) > 4 or bool(items) == (kind == "insufficient"):
            raise ValueError("answer cardinality")
        if kind == "single" and len(items) != 1:
            raise ValueError("single answer cardinality")
        if kind in ("conditional", "conflict") and len(items) < 2:
            raise ValueError("multiple answers required")
        answers = []
        for item in items:
            if not isinstance(item, dict) or set(item) != {"source", "quote", "answer", "condition"}:
                raise ValueError("expected only source, quote, answer, condition")
            if not isinstance(item["source"], str) or item["source"] not in by_id:
                raise ValueError("citation outside supplied source scope")
            env = by_id[item["source"]]
            cite = witness(env, item["quote"])
            condition = witness(env, item["condition"], True)
            answer = item["answer"]
            if not isinstance(answer, str) or not answer or not (answer in item["quote"] or answer == env["source"]["speaker"]):
                raise ValueError("answer not an exact cited substring or complete speaker name")
            answers.append(dict(**cite, answer=answer, condition=condition,
                                status=assertion_status(cite, answer, data["relations"])))
        if len({item["source_id"] for item in answers}) != len(answers):
            raise ValueError("duplicate answer source")
        return dict(kind=kind, answers=answers, raw=raw, input_sha256=packet["input_sha256"],
                    validation="literal source scope and format only; semantic correctness unscored",
                    stage="cited_reader_adapter_not_native_qa")
    except (ValueError, TypeError, KeyError) as exc:
        return dict(kind="invalid", answers=[], error=str(exc), raw=raw,
                    input_sha256=packet["input_sha256"], stage="cited_reader_adapter_not_native_qa")


def execute_qa(packet, generate):
    """Optional explicitly injected (system, user)->raw callback; no provider."""
    _validate_packet(packet)
    if not callable(generate):
        raise TypeError("generate must be an explicitly supplied callback")
    raw = generate(packet["system"], packet["user"])
    return parse_qa_output(raw, packet)
