"""Resolve only native composer-selected CUPMem references to original turns.

Pure offline plumbing, not retrieval, entailment checking or a citation score.
The native canonical grounding points to active/stale/unknown profile records;
their chunk/delta links are followed literally. Chunk summaries are NEVER used
as quotations, including chunks that stitch discontinuous source turns.

Status-cause lineage is exposed separately for audit. It is not automatically
passed to a cited reader: a native status label is not a selection of the source
passages supporting that status. No missing link falls back to the full history.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json


BASIS_ROLES = ("blocker_basis", "decisive_basis", "supporting_basis")


def digest(value):
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode()).hexdigest()


def persistent_state_hash(trace):
    """Same fields and canonical encoding as the pinned pilot's state_hash."""
    return digest({key: trace[key] for key in
                   ("final_profile_snapshot", "chunk_bank", "delta_store")})


def _index(rows, key):
    indexed = {}
    for row in rows:
        if isinstance(row, dict) and isinstance(row.get(key), str):
            indexed.setdefault(row[key], []).append(row)
    return indexed


def resolve_grounding(canonical_answer_grounding, trace):
    """Return value-only reader passages plus separate, unvalidated status audit.

    Call with the *exact* canonical_answer_grounding from the final native
    composer request and the trace snapshot used for that query. Supplying a
    later snapshot is a caller error; input hashes preserve the actual inputs.
    An empty selection returns no passages, even if corrected_current_facts,
    top-k candidates or full history contain a potentially useful answer.
    """
    if not isinstance(canonical_answer_grounding, dict) or not isinstance(trace, dict):
        raise ValueError("grounding and trace must be objects")
    snapshot = trace.get("final_profile_snapshot")
    if not isinstance(snapshot, dict):
        raise ValueError("trace requires the query-time final_profile_snapshot")
    active = snapshot.get("active_profile", {})
    if not isinstance(active, dict):
        raise ValueError("active_profile must use the upstream track-to-items schema")
    active_items = [item for items in active.values() for item in items]
    profiles = {"active": _index(active_items, "item_id"),
                "stale": _index(snapshot.get("stale_archive", []), "item_id")}
    unknowns = {}
    for row in snapshot.get("unknown_current", []):
        if isinstance(row, dict):
            key = f"{row.get('bucket', '')}/{row.get('local_track', '')}"
            unknowns.setdefault(key, []).append(row)
    profiles["unknown"] = unknowns
    chunks = _index(trace.get("chunk_bank", []), "chunk_id")
    deltas = _index(trace.get("delta_store", []), "delta_id")
    sessions = _index(trace.get("session_logs", []), "session_id")
    proposals = _index([entry["proposal"] for session in trace.get("session_logs", [])
                        for entry in session.get("invalidation_logs", [])
                        if isinstance(entry.get("proposal"), dict)], "proposal_id")
    passages, passage_order, bindings, unresolved = {}, [], [], []

    def missing(binding, path, reason, ref):
        row = dict(binding_id=binding["binding_id"], path=path, reason=reason, reference=ref)
        unresolved.append(row)
        binding["unresolved"].append(row)

    def unique(index, identifier, binding, path, kind):
        matches = index.get(identifier, [])
        if len(matches) != 1:
            missing(binding, path, "missing_" + kind if not matches else "ambiguous_" + kind, identifier)
            return None
        return matches[0]

    def walk_chunk(identifier, binding, path, purpose):
        path = path + [f"chunk:{identifier}"]
        chunk = unique(chunks, identifier, binding, path, "chunk")
        if chunk is None:
            return
        sid = chunk.get("session_id", "")
        session = unique(sessions, sid, binding, path + [f"session:{sid}"], "session")
        if session is None:
            return
        tids = chunk.get("source_turn_ids", [])
        if not isinstance(tids, list) or not tids:
            missing(binding, path, "missing_source_turn_ids", identifier)
            return
        turns = _index(session.get("user_turns", []), "turn_id")
        for tid in tids:
            turn_path = path + [f"session:{sid}", f"user_turn:{tid}"]
            turn = unique(turns, tid, binding, turn_path, "user_turn")
            if turn is None:
                continue
            if not isinstance(turn.get("content"), str):
                missing(binding, turn_path, "non_text_original_turn", tid)
                continue
            identity = dict(uid=trace.get("sample_meta", {}).get("uid"), session_id=sid,
                            turn_id=tid, content_sha256=hashlib.sha256(turn["content"].encode()).hexdigest())
            citation_id = "cupturn-" + digest(identity)[:20]
            if citation_id not in passages:
                passages[citation_id] = dict(citation_id=citation_id, **identity,
                                            session_index=session.get("session_index"),
                                            session_time=session.get("session_time"),
                                            text=turn["content"], uses=[])
                passage_order.append(citation_id)
            use = dict(binding_id=binding["binding_id"], purpose=purpose)
            if use not in passages[citation_id]["uses"]:
                passages[citation_id]["uses"].append(use)
            link = dict(citation_id=citation_id, path=turn_path,
                        chunk_text_is_not_a_quote=True)
            target = binding["value_provenance"] if purpose == "value" else binding["status_provenance"]
            if link not in target:
                target.append(link)

    def walk_delta(identifier, binding, path, purpose):
        path = path + [f"delta:{identifier}"]
        delta = unique(deltas, identifier, binding, path, "delta")
        if delta is None:
            return
        ids = delta.get("evidence_chunk_ids", [])
        if not ids:
            missing(binding, path, "missing_delta_evidence_chunks", identifier)
        for chunk_id in ids:
            walk_chunk(chunk_id, binding, path, purpose)

    def walk_cause(identifier, binding, path):
        # Actual upstream revision fields may point to a delta or a proposal.
        # Never infer an identifier or source passage by searching reason text.
        if identifier in deltas and identifier in proposals:
            missing(binding, path, "ambiguous_cause_kind", identifier)
            return
        if identifier in deltas:
            walk_delta(identifier, binding, path, "status_cause")
            return
        proposal = unique(proposals, identifier, binding, path + [f"proposal:{identifier}"], "cause_proposal")
        if proposal is None:
            return
        path = path + [f"proposal:{identifier}"]
        if not proposal.get("evidence_chunk_ids") and not proposal.get("trigger_delta_ids"):
            missing(binding, path, "missing_proposal_evidence", identifier)
        for chunk_id in proposal.get("evidence_chunk_ids", []):
            walk_chunk(chunk_id, binding, path, "status_cause")
        for delta_id in proposal.get("trigger_delta_ids", []):
            walk_delta(delta_id, binding, path, "status_cause")

    for role in BASIS_ROLES:
        selected = canonical_answer_grounding.get(role, [])
        if not isinstance(selected, list):
            raise ValueError(f"{role} must be a list")
        for position, basis in enumerate(selected):
            binding = dict(binding_id=f"{role}:{position}", role=role, position=position,
                           native_basis=deepcopy(basis), value_provenance=[], status_provenance=[],
                           status_events=[], unresolved=[], limitations=[])
            bindings.append(binding)
            if not isinstance(basis, dict) or not isinstance(basis.get("hit_ref"), dict):
                missing(binding, [], "missing_hit_ref", None)
                continue
            ref = basis["hit_ref"]
            source, identifier = ref.get("source"), ref.get("id")
            path = [f"{role}[{position}].hit_ref", f"{source}:{identifier}"]
            if source not in profiles:
                missing(binding, path, "unsupported_native_reference_source", source)
                continue
            item = unique(profiles[source], identifier, binding, path, "profile_record")
            if item is None:
                continue
            for key in ["bucket", "local_track"]:
                if ref.get(key) and ref[key] != item.get(key):
                    missing(binding, path, "reference_metadata_mismatch", key)
            expected_record_status = {"active": "ACTIVE", "stale": "STALE", "unknown": "UNKNOWN_CURRENT"}[source]
            if item.get("status") != expected_record_status:
                missing(binding, path, "record_status_container_mismatch", item.get("status"))
            expected_label = expected_record_status
            expected_detail = {"stale": "stale", "unknown": "unknown_current"}.get(source)
            if source == "active":
                weak = str(item.get("active_strength", "STRONG")).upper() == "WEAK"
                expected_label = "ACTIVE_WEAK" if weak else "ACTIVE_STRONG"
                expected_detail = "weak_active" if weak else "strong_active"
            if basis.get("status_label") != expected_label:
                missing(binding, path, "native_status_label_snapshot_mismatch",
                        {"native": basis.get("status_label"), "snapshot": expected_label})
            if "source_detail" in ref and ref["source_detail"] != expected_detail:
                missing(binding, path, "native_source_detail_snapshot_mismatch",
                        {"native": ref["source_detail"], "snapshot": expected_detail})
            if binding["unresolved"]:
                continue
            binding["resolved_record_status"] = item.get("status")
            binding["resolved_active_strength"] = item.get("active_strength")
            if source != "unknown":
                for chunk_id in item.get("evidence_chunk_ids", []):
                    walk_chunk(chunk_id, binding, path + ["item.evidence_chunk_ids"], "value")
                for delta_id in item.get("source_delta_ids", []):
                    walk_delta(delta_id, binding, path + ["item.source_delta_ids"], "value")
                if not item.get("evidence_chunk_ids") and not item.get("source_delta_ids"):
                    missing(binding, path, "missing_value_evidence_links", identifier)
                events = item.get("revision_history", [])
            else:
                events = [item]
                binding["limitations"].append("Unknown-current records express a status, not an observed value; they supply no value-support passage.")
            for event_index, event in enumerate(events):
                event_path = path + ["unknown_record" if source == "unknown" else f"revision_history[{event_index}]"]
                binding["status_events"].append(dict(event=deepcopy(event),
                                                      role="stored_status_rationale_not_a_source_quote",
                                                      selected_causal_passages_by_native=False))
                ids = list(event.get("source_delta_ids", []))
                ids += [event[key] for key in ["source_proposal_id", "invalidated_by_delta_id"] if event.get(key)]
                if not ids:
                    missing(binding, event_path, "missing_status_cause_reference", identifier)
                for cause_id in dict.fromkeys(ids):
                    walk_cause(cause_id, binding, event_path)
            if events or basis.get("status_label") in ["ACTIVE_WEAK", "STALE", "UNKNOWN_CURRENT"]:
                binding["limitations"].append("The native grounding names a status but does not select its causal source passages; resolved status causes are audit-only and excluded from reader_payload.")
            binding["limitations"].append("Lineage does not establish that the original turns entail the generated value, status, or answer.")

    for binding in bindings:
        any_links = bool(binding["value_provenance"] or binding["status_provenance"])
        binding["resolution"] = ("partial" if any_links else "unresolved") if binding["unresolved"] else "resolved"
    value_ids = {link["citation_id"] for binding in bindings for link in binding["value_provenance"]}
    all_passages = [passages[cid] for cid in passage_order]
    reader_passages = [{key: deepcopy(value) for key, value in passage.items() if key != "uses"}
                       for passage in all_passages if passage["citation_id"] in value_ids]
    return dict(schema_version=1, status="offline_provenance_resolution_only",
                grounding_sha256=digest(canonical_answer_grounding), trace_sha256=digest(trace),
                basis_bindings=bindings, original_turns_for_audit=all_passages, unresolved=unresolved,
                reader_payload=dict(passages=reader_passages,
                                    policy="Only original turns linked to native-selected value records; status-cause audit passages are not automatically added."),
                limitations=["No semantic validation or citation-success score is produced.",
                             "Status labels/reasons and generated chunks are not original quotations.",
                             "No unselected history, neighboring turn, corrected_current_fact or top-k candidate is added.",
                             "Whole linked original turns may contain more detail than the native summary; this explicit citation adapter is separate from native CUPMem QA.",
                             "reader_payload is source-expansion preparation, not a complete fair cited-QA prompt. A later reader must explicitly decide how to present native status/summary annotations as model-derived information; stripping them could degrade CUPMem artificially.",
                             "Resolver or binding failure is an adapter failure, never a native CUPMem QA error."])


def resolve_composer_request(request_event, trace, *, query_label, query_text,
                             expected_state_sha256=None):
    """Bind an audited final composer request to a recorded query-time state.

    expected_state_sha256 MUST come from the recorded checkpoint for this query,
    not a hash freshly computed to bless the supplied snapshot. Both query-start
    and query-complete records, UID, request body hash, query label and literal
    query text must match. A state hash alone does not identify the query.

    This wrapper prepares evidence after native QA completes. Its ready flag
    concerns source expansion only, not a finished fair reader prompt or score.
    """
    errors = []

    def fail(reason, **details):
        errors.append(dict(reason=reason, **details))

    if not isinstance(request_event, dict) or request_event.get("event") != "request":
        fail("not_an_audited_request_event")
        request_event = request_event if isinstance(request_event, dict) else {}
    context = request_event.get("context", {})
    body = request_event.get("body", {})
    if not isinstance(context, dict):
        fail("missing_request_context")
        context = {}
    if not isinstance(body, dict):
        fail("missing_request_body")
        body = {}
    if not isinstance(trace, dict):
        fail("missing_trace")
        trace = {}
    uid = trace.get("sample_meta", {}).get("uid")
    if not isinstance(uid, str) or not uid or context.get("uid") != uid:
        fail("request_uid_trace_mismatch", request_uid=context.get("uid"), trace_uid=uid)
    if context.get("arm") != "cupmem":
        fail("request_arm_not_cupmem", observed=context.get("arm"))
    if not isinstance(query_label, str) or not query_label or context.get("query_label") != query_label:
        fail("request_query_label_mismatch", request_label=context.get("query_label"), expected_label=query_label)
    if not isinstance(query_text, str) or not query_text:
        fail("missing_expected_query_text")
    if request_event.get("body_sha256") != digest(body):
        fail("request_body_hash_mismatch")
    payload = {}
    try:
        message = body["messages"][-1]
        if message.get("role") != "user":
            fail("composer_payload_not_user_message")
        payload = json.loads(message["content"])
        if not isinstance(payload, dict):
            raise ValueError("payload must be an object")
    except (KeyError, IndexError, TypeError, ValueError):
        fail("missing_json_composer_payload")
        payload = {}
    if not isinstance(payload.get("canonical_answer_grounding"), dict) or "constraint_set" not in payload:
        fail("final_composer_payload_schema_mismatch")
    if payload.get("query") != query_text:
        fail("request_query_text_mismatch")
    query_log = trace.get("query_logs", {}).get(query_label, {})
    if not isinstance(query_log, dict) or query_log.get("query_text") != query_text:
        fail("trace_query_text_mismatch")
    valid_hash = (isinstance(expected_state_sha256, str) and len(expected_state_sha256) == 64
                  and all(ch in "0123456789abcdef" for ch in expected_state_sha256))
    if not valid_hash:
        fail("missing_recorded_expected_state_hash")
    try:
        actual_hash = persistent_state_hash(trace)
    except KeyError:
        actual_hash = None
        fail("missing_persistent_state_fields")
    if valid_hash and actual_hash != expected_state_sha256:
        fail("persistent_state_hash_mismatch", expected=expected_state_sha256, actual=actual_hash)
    checks = [row for row in trace.get("memory_immutability_checks", [])
              if isinstance(row, dict) and row.get("query") == query_label]
    if (len(checks) != 2 or {row.get("phase") for row in checks} != {"query_start", "query_complete"}
            or any(row.get("state_sha256") != expected_state_sha256 for row in checks)):
        fail("missing_or_inconsistent_recorded_query_state_binding")
    binding = dict(verified=not errors, query_label=query_label, query_text=query_text,
                   uid=uid, request_id=request_event.get("request_id"),
                   request_body_sha256=request_event.get("body_sha256"),
                   expected_state_sha256=expected_state_sha256,
                   actual_state_sha256=actual_hash, errors=errors)
    if errors:
        return dict(status="adapter_binding_error_not_model_error", source_expansion_ready=False,
                    binding=binding, reader_payload={"passages": []},
                    limitations=["The request/snapshot association is unverified; do not score native QA or call a reader from this adapter result."])
    resolved = resolve_grounding(payload["canonical_answer_grounding"], trace)
    resolved["binding"] = binding
    resolved["source_expansion_ready"] = not resolved["unresolved"]
    if resolved["unresolved"]:
        resolved["status"] = "adapter_resolution_incomplete_not_model_error"
    else:
        resolved["status"] = "bound_offline_source_expansion_only"
    return resolved
