import copy
import json
from pathlib import Path
import unittest

from evaluation.cupmem.provenance import digest, persistent_state_hash, resolve_composer_request, resolve_grounding


def fixture():
    return {
        "sample_meta": {"uid": "offline-test"},
        "final_profile_snapshot": {
            "active_profile": {"b/t": [{"item_id": "p1", "bucket": "b", "local_track": "t",
                "value": "Generated summary, not a quote", "status": "ACTIVE", "active_strength": "WEAK",
                "source_delta_ids": ["d1"], "evidence_chunk_ids": ["c1"],
                "revision_history": [{"event": "weak_challenge", "reason": "Generated weak rationale",
                                      "source_proposal_id": "lip1", "source_delta_ids": ["d2"]}]}]},
            "stale_archive": [{"item_id": "p2", "bucket": "b", "local_track": "t",
                "status": "STALE", "evidence_chunk_ids": ["c1"], "source_delta_ids": ["d1"],
                "revision_history": [{"event": "archived", "invalidated_by_delta_id": "lip1"}]}],
            "unknown_current": [{"bucket": "b", "local_track": "t", "status": "UNKNOWN_CURRENT",
                                 "reason": "Generated unknown rationale", "invalidated_by_delta_id": "lip1"}]},
        "chunk_bank": [{"chunk_id": "c1", "session_id": "s0", "source_turn_ids": ["t0", "t4"],
                        "text": "Stitched and edited summary ... definitely not literal"},
                       {"chunk_id": "c2", "session_id": "s1", "source_turn_ids": ["t0"], "text": "A reason"}],
        "delta_store": [{"delta_id": "d1", "evidence_chunk_ids": ["c1"]},
                        {"delta_id": "d2", "evidence_chunk_ids": ["c2"]}],
        "session_logs": [
            {"session_id": "s0", "session_index": 0, "session_time": "2020-01-01",
             "user_turns": [{"turn_id": "t0", "content": "Original first turn."},
                            {"turn_id": "t2", "content": "Unselected middle turn."},
                            {"turn_id": "t4", "content": "Original last turn."}], "invalidation_logs": []},
            {"session_id": "s1", "session_index": 1, "session_time": "2020-01-02",
             "user_turns": [{"turn_id": "t0", "content": "Status-cause original turn."}],
             "invalidation_logs": [{"proposal": {"proposal_id": "lip1", "evidence_chunk_ids": ["c2"],
                                                 "trigger_delta_ids": ["d2"]}}]},
        ],
    }


def grounding(source="active", identifier="p1", status="ACTIVE_WEAK"):
    return {"decisive_basis": [{"hit_ref": {"source": source, "id": identifier, "bucket": "b", "local_track": "t"},
                                "text": "Generated value", "status_label": status}],
            "blocker_basis": [], "supporting_basis": []}


def bound_fixture():
    trace = fixture()
    label, question = "q1", "What was recorded?"
    state_hash = persistent_state_hash(trace)
    trace["query_logs"] = {label: {"query_text": question}}
    trace["memory_immutability_checks"] = [dict(phase=phase, query=label, state_sha256=state_hash)
                                           for phase in ["query_start", "query_complete"]]
    body = {"messages": [{"role": "user", "content": json.dumps({"query": question,
             "canonical_answer_grounding": grounding(), "constraint_set": None})}]}
    request = dict(event="request", request_id=1, body=body, body_sha256=digest(body),
                   context=dict(arm="cupmem", uid="offline-test", query_label=label))
    return trace, request, dict(query_label=label, query_text=question, expected_state_sha256=state_hash)


class ProvenanceTests(unittest.TestCase):
    def test_discontinuous_chunks_only_yield_original_linked_turns(self):
        trace, native = fixture(), grounding()
        before = copy.deepcopy((trace, native))
        result = resolve_grounding(native, trace)
        self.assertEqual([x["text"] for x in result["reader_payload"]["passages"]],
                         ["Original first turn.", "Original last turn."])
        self.assertEqual((trace, native), before)
        binding = result["basis_bindings"][0]
        self.assertTrue(binding["status_provenance"])
        self.assertTrue(any("audit-only" in x for x in binding["limitations"]))
        self.assertNotIn("Status-cause original turn.", [x["text"] for x in result["reader_payload"]["passages"]])
        self.assertEqual(result["unresolved"], [])

    def test_unknown_only_resolves_status_cause_not_value(self):
        result = resolve_grounding(grounding("unknown", "b/t", "UNKNOWN_CURRENT"), fixture())
        self.assertEqual(result["reader_payload"]["passages"], [])
        binding = result["basis_bindings"][0]
        self.assertEqual(binding["value_provenance"], [])
        self.assertTrue(binding["status_provenance"])
        self.assertEqual([x["text"] for x in result["original_turns_for_audit"]], ["Status-cause original turn."])

    def test_stale_value_does_not_turn_archive_reason_into_quote(self):
        result = resolve_grounding(grounding("stale", "p2", "STALE"), fixture())
        self.assertEqual(len(result["reader_payload"]["passages"]), 2)
        self.assertTrue(result["basis_bindings"][0]["status_provenance"])
        self.assertNotIn("Generated", json.dumps(result["reader_payload"]))

    def test_missing_and_ambiguous_refs_never_fall_back(self):
        result = resolve_grounding(grounding(identifier="missing"), fixture())
        self.assertEqual(result["reader_payload"]["passages"], [])
        self.assertEqual(result["unresolved"][0]["reason"], "missing_profile_record")
        trace = fixture()
        trace["final_profile_snapshot"]["active_profile"]["b/t"] *= 2
        result = resolve_grounding(grounding(), trace)
        self.assertEqual(result["reader_payload"]["passages"], [])
        self.assertEqual(result["unresolved"][0]["reason"], "ambiguous_profile_record")

    def test_missing_turn_and_cause_stay_visible(self):
        trace = fixture()
        trace["chunk_bank"][0]["source_turn_ids"].append("absent")
        trace["final_profile_snapshot"]["active_profile"]["b/t"][0]["revision_history"][0]["source_proposal_id"] = "missing-lip"
        result = resolve_grounding(grounding(), trace)
        reasons = {x["reason"] for x in result["unresolved"]}
        self.assertIn("missing_user_turn", reasons)
        self.assertIn("missing_cause_proposal", reasons)
        self.assertEqual(result["basis_bindings"][0]["resolution"], "partial")

    def test_empty_grounding_does_not_use_free_text_facts(self):
        result = resolve_grounding({"corrected_current_facts": ["Original first turn."]}, fixture())
        self.assertEqual(result["reader_payload"]["passages"], [])
        self.assertEqual(result["basis_bindings"], [])

    def test_metadata_mismatch_and_unknown_source_fail_closed(self):
        native = grounding()
        native["decisive_basis"][0]["hit_ref"]["bucket"] = "wrong"
        result = resolve_grounding(native, fixture())
        self.assertEqual(result["reader_payload"]["passages"], [])
        self.assertEqual(result["unresolved"][0]["reason"], "reference_metadata_mismatch")
        result = resolve_grounding(grounding("unobserved-source"), fixture())
        self.assertEqual(result["unresolved"][0]["reason"], "unsupported_native_reference_source")

    def test_later_snapshot_status_and_detail_mismatches_fail_closed(self):
        trace = fixture()
        trace["final_profile_snapshot"]["active_profile"]["b/t"][0]["active_strength"] = "STRONG"
        native = grounding()
        native["decisive_basis"][0]["hit_ref"]["source_detail"] = "weak_active"
        result = resolve_grounding(native, trace)
        self.assertEqual(result["reader_payload"]["passages"], [])
        self.assertEqual({x["reason"] for x in result["unresolved"]},
                         {"native_status_label_snapshot_mismatch", "native_source_detail_snapshot_mismatch"})

    def test_wrapper_requires_recorded_hash_and_uid(self):
        trace, request, args = bound_fixture()
        result = resolve_composer_request(request, trace, **args)
        self.assertTrue(result["source_expansion_ready"])
        missing = dict(args, expected_state_sha256=None)
        result = resolve_composer_request(request, trace, **missing)
        self.assertFalse(result["source_expansion_ready"])
        self.assertIn("missing_recorded_expected_state_hash", {x["reason"] for x in result["binding"]["errors"]})
        request["context"]["uid"] = "different-case"
        result = resolve_composer_request(request, trace, **args)
        self.assertEqual(result["reader_payload"]["passages"], [])
        self.assertIn("request_uid_trace_mismatch", {x["reason"] for x in result["binding"]["errors"]})

    def test_wrapper_later_same_id_snapshot_not_accepted(self):
        trace, request, args = bound_fixture()
        trace["final_profile_snapshot"]["active_profile"]["b/t"][0]["value"] = "Later value, same ID and status"
        result = resolve_composer_request(request, trace, **args)
        self.assertFalse(result["source_expansion_ready"])
        self.assertIn("persistent_state_hash_mismatch", {x["reason"] for x in result["binding"]["errors"]})

    def test_same_state_hash_does_not_identify_same_query(self):
        trace, request, args = bound_fixture()
        request["context"]["query_label"] = "q2"
        result = resolve_composer_request(request, trace, **args)
        self.assertFalse(result["source_expansion_ready"])
        self.assertIn("request_query_label_mismatch", {x["reason"] for x in result["binding"]["errors"]})
        trace, request, args = bound_fixture()
        result = resolve_composer_request(request, trace, **dict(args, query_text="Different query?"))
        self.assertFalse(result["source_expansion_ready"])
        self.assertIn("request_query_text_mismatch", {x["reason"] for x in result["binding"]["errors"]})

    def test_request_body_and_checkpoint_tampering_are_binding_errors(self):
        trace, request, args = bound_fixture()
        request["body"]["messages"][0]["content"] += " "
        result = resolve_composer_request(request, trace, **args)
        self.assertIn("request_body_hash_mismatch", {x["reason"] for x in result["binding"]["errors"]})
        trace, request, args = bound_fixture()
        trace["memory_immutability_checks"].pop()
        result = resolve_composer_request(request, trace, **args)
        self.assertIn("missing_or_inconsistent_recorded_query_state_binding", {x["reason"] for x in result["binding"]["errors"]})

    def test_actual_pilot_composer_selection(self):
        folder = Path(__file__).resolve().parents[1] / "results/cupmem/pilot-v5"
        if not (folder / "http.jsonl").exists():
            self.skipTest("Optional immutable pilot artifacts are not bundled")
        trace = json.loads((folder / "a5aa884f-29d6-40dc-a72c-e155fcbc7c79.cupmem.json").read_text())
        requests = {row["request_id"]: row for row in map(json.loads, (folder / "http.jsonl").read_text().splitlines())
                    if row["event"] == "request" and row["request_id"] in [911, 918, 924]}
        results = {}
        for rid, row in requests.items():
            payload = json.loads(row["body"]["messages"][-1]["content"])
            label = row["context"]["query_label"]
            recorded = next(x["state_sha256"] for x in trace["memory_immutability_checks"]
                            if x["query"] == label and x["phase"] == "query_start")
            results[rid] = resolve_composer_request(row, trace, query_label=label,
                query_text=payload["query"], expected_state_sha256=recorded)
            self.assertTrue(results[rid]["source_expansion_ready"])
            self.assertEqual(results[rid]["unresolved"], [])
        self.assertEqual([(x["session_id"], x["turn_id"]) for x in results[911]["reader_payload"]["passages"]],
                         [("s_000", "t_6")])
        self.assertEqual(results[918]["reader_payload"]["passages"], [])
        self.assertEqual({(x["session_id"], x["turn_id"]) for x in results[924]["reader_payload"]["passages"]},
                         {("s_038", "t_2"), ("s_038", "t_4"), ("s_038", "t_6"), ("s_000", "t_6")})
        self.assertTrue(any(x["session_id"] == "s_001" for x in results[924]["original_turns_for_audit"]))
        self.assertFalse(any(x["session_id"] == "s_001" for x in results[924]["reader_payload"]["passages"]))


if __name__ == "__main__":
    unittest.main()
