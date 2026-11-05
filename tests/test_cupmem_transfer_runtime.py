"""Deterministic orchestration checks using the pinned official serializer."""
from copy import deepcopy
import importlib.util
import json
import os
from pathlib import Path
import unittest

from evaluation.cupmem.transfer_inputs import attributed_session, native_record_at
from evaluation.cupmem.transfer_runtime import IncrementalTransferRun, TransferInterrupted, run_case
from evaluation.cupmem.provenance import digest, persistent_state_hash, resolve_composer_request


ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = Path(os.environ.get("CUPMEM_UPSTREAM_ROOT", ROOT.parent / "campaigns/cupmem-stale/upstream"))
SERIALIZER = UPSTREAM / "cup_mem/core/sample_runner.py"
if not SERIALIZER.is_file():
    raise unittest.SkipTest("Pinned CUPMem source is optional locally; see CONTRIBUTING.md for CUPMEM_UPSTREAM_ROOT")
SPEC = importlib.util.spec_from_file_location("pinned_cupmem_sample_runner_for_test", SERIALIZER)
PINNED = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PINNED)


class Item:
    def __init__(self, value):
        self.value = value

    def to_dict(self):
        return self.value


class Store:
    def __init__(self):
        self.values = []

    def to_snapshot(self):
        return dict(active_profile={"test/native": self.values}, stale_archive=[],
                    unknown_current=[], stale_support_links=[])


class StopBudget(BaseException):
    pass


class Engine(PINNED.SampleRunnerMixin):
    """No model; official method signatures and official result serializer."""
    def __init__(self, *, mutate_query=False, fail_session=None, fail_serialize=False):
        self.store = Store()
        self.chunk_bank = []
        self.delta_store = []
        self.writes, self.reads, self.resets = [], [], 0
        self.mutate_query = mutate_query
        self.fail_session = fail_session
        self.fail_serialize = fail_serialize

    def reset(self):
        self.resets += 1
        self.store = Store()
        self.chunk_bank, self.delta_store = [], []

    def _chunk_trace_dict(self, item):
        data = deepcopy(item.to_dict())
        data.pop("change_signal_summary", None)  # Native non-debug trace behavior.
        return data

    def _delta_trace_dict(self, item):
        data = deepcopy(item.to_dict())
        data.pop("op_hint", None)  # Native trace helpers do not equal raw to_dict.
        return data

    def _build_sample_result(self, **kwargs):
        if self.fail_serialize:
            raise ValueError("serializer failed")
        return super()._build_sample_result(**kwargs)

    def process_session(self, *, session, session_index, session_time):
        call = dict(session=deepcopy(session), session_index=session_index, session_time=session_time)
        self.writes.append(call)
        self.store.values.append(deepcopy(call))
        self.chunk_bank.append(Item(dict(chunk_id=f"c_{session_index:05d}", text=session[0]["content"],
                                         change_signal_summary="auxiliary chunk field")))
        self.delta_store.append(Item(dict(delta_id=f"d_{session_index:05d}", op_hint="auxiliary delta field")))
        if session_index == self.fail_session:
            raise StopBudget("ERROR_MESSAGE_MUST_NOT_BE_LOGGED")
        return dict(session_id=f"s_{session_index:03d}", session_index=session_index,
                    session_time=session_time, user_turns=deepcopy(session),
                    full_writer_details={"retained_original": session[0]["content"]},
                    profile_snapshot_after_session=self.store.to_snapshot())

    def answer_query(self, *, query_label, query_text):
        self.reads.append(dict(query_label=query_label, query_text=query_text))
        if self.mutate_query:
            self.store.values.append({"illegal_query_memory": query_text})
        return dict(query_label=query_label, query_text=query_text,
                    answer={"answer": "fake answer", "brief_rationale": "fake rationale"},
                    relevant_context={"visible_records": len(self.store.values)},
                    debug_trace={"fake_exact_trace": query_text})


def source(text, date="2025-01-01T00:00:00Z"):
    return dict(owner="Original author", observed_at=date,
                source=dict(speaker="Original author", text=text, location="source://" + text))


def case():
    return dict(case_id="opaque-case", events=[
        dict(op="ingest", event_id="e0", source=source("FIRST_SOURCE")),
        dict(op="ask", event_id="e1", question="FIRST_QUESTION"),
        dict(op="ingest", event_id="e2", source=source("FUTURE_SOURCE", "2025-01-02T00:00:00Z")),
        dict(op="ask", event_id="e3", question="FUTURE_QUESTION"),
    ])


class TransferRuntimeTest(unittest.TestCase):
    def test_incremental_exact_prefix_and_full_traces_without_future_or_answer_ingestion(self):
        fixture = case()
        engine, raw_calls, progress = Engine(), [], []
        def raw(record):
            raw_calls.append(deepcopy(record))
            return dict(raw="baseline answer", original_input=deepcopy(record))
        run = IncrementalTransferRun(fixture, engine=engine, raw_reader=raw, progress_callback=progress.append)
        first = run.advance()
        first_query = run.advance()
        self.assertNotIn("FUTURE_SOURCE", json.dumps(first_query))
        self.assertNotIn("FUTURE_QUESTION", json.dumps(first_query))
        result = run.run()
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["completed_events"], 4)
        self.assertEqual(result["completed_native_sessions"], 2)
        self.assertEqual(result["completed_paired_queries"], 2)
        self.assertEqual([w["session"] for w in engine.writes],
                         [attributed_session(fixture["events"][i]["source"]) for i in (0, 2)])
        self.assertEqual(raw_calls, [native_record_at(fixture, i) for i in (1, 3)])
        self.assertEqual([r["query_text"] for r in engine.reads], ["FIRST_QUESTION", "FUTURE_QUESTION"])
        self.assertEqual(first["final_persistent_state"]["final_profile_snapshot"]["active_profile"]["test/native"],
                         [engine.writes[0]])
        for row in result["event_traces"]:
            if row["op"] == "ask":
                self.assertEqual(row["persistent_before_sha256"], row["persistent_after_native_query_sha256"])
                self.assertEqual(row["persistent_before_sha256"], row["persistent_after_raw_query_sha256"])
                self.assertEqual(row["persistent_before_sha256"], row["persistent_after_sha256"])
                self.assertIn("debug_trace", row["native_query_trace"])
            else:
                self.assertIn("full_writer_details", row["native_session_trace"])
        native = result["native_result"]
        self.assertEqual(native["completed_session_count"], 2)
        self.assertEqual(native["completed_query_count"], 2)
        self.assertIsNone(native["sample_meta"]["M_old"])
        self.assertTrue(progress)

    def test_query_mutation_stops_before_raw_and_preserves_mutated_state_and_answer(self):
        engine, raw_calls = Engine(mutate_query=True), []
        with self.assertRaises(TransferInterrupted) as raised:
            run_case(case(), engine=engine, raw_reader=raw_calls.append)
        report = raised.exception.report
        self.assertEqual(report["status"], "interrupted")
        self.assertEqual(report["interruption"]["error_type"], "StateMutationError")
        self.assertEqual(report["completed_events"], 1)
        self.assertEqual(report["completed_native_queries"], 1)
        self.assertEqual(report["completed_paired_queries"], 0)
        self.assertEqual(raw_calls, [])
        row = report["event_traces"][-1]
        self.assertNotEqual(row["persistent_before_sha256"], row["persistent_after_native_query_sha256"])
        self.assertEqual(row["native_query_trace"]["answer"]["answer"], "fake answer")

    def test_query_time_trace_binds_early_composer_after_future_ingest_with_distinct_hash_scopes(self):
        fixture = case()
        report = run_case(fixture, engine=Engine(), raw_reader=lambda r: "answer")
        first = report["event_traces"][1]
        trace = first["query_time_trace"]
        self.assertNotIn("FUTURE_SOURCE", json.dumps(trace))
        self.assertNotIn("FUTURE_QUESTION", json.dumps(trace))
        self.assertEqual(trace["completed_session_count"], 1)
        self.assertEqual(trace["completed_query_count"], 1)
        self.assertNotEqual(first["persistent_before_sha256"], first["native_query_state_sha256"])
        self.assertEqual(first["native_query_state_sha256"], persistent_state_hash(trace))
        self.assertEqual({c["phase"] for c in trace["memory_immutability_checks"]}, {"query_start", "query_complete"})
        body = {"messages": [{"role": "user", "content": json.dumps({
            "query": "FIRST_QUESTION", "canonical_answer_grounding": {}, "constraint_set": None})}]}
        request = dict(event="request", request_id=1, body=body, body_sha256=digest(body),
                       context=dict(arm="cupmem", uid=fixture["case_id"], query_label="e1"))
        bound = resolve_composer_request(request, trace, query_label="e1", query_text="FIRST_QUESTION",
                                         expected_state_sha256=first["native_query_state_sha256"])
        self.assertTrue(bound["binding"]["verified"])
        # The final state contains future data and must not bind an earlier query.
        later = resolve_composer_request(request, report["native_result"], query_label="e1", query_text="FIRST_QUESTION",
                                         expected_state_sha256=first["native_query_state_sha256"])
        self.assertFalse(later["binding"]["verified"])
        self.assertIn("persistent_state_hash_mismatch", {e["reason"] for e in later["binding"]["errors"]})

    def test_engine_error_preserves_partial_writer_state_and_does_not_resume(self):
        engine, progress = Engine(fail_session=1), []
        run = IncrementalTransferRun(case(), engine=engine, raw_reader=lambda r: "answer", progress_callback=progress.append)
        with self.assertRaises(TransferInterrupted) as raised:
            run.run()
        report = raised.exception.report
        self.assertEqual(report["completed_events"], 2)
        self.assertEqual(report["completed_native_sessions"], 1)
        self.assertEqual(len(report["source_arrivals"]), 1)
        self.assertEqual(len(report["final_persistent_state"]["chunk_bank"]), 2)
        self.assertEqual(report["event_traces"][-1]["status"], "interrupted")
        self.assertEqual(progress[-1]["status"], "interrupted")
        self.assertNotIn("ERROR_MESSAGE_MUST_NOT_BE_LOGGED", json.dumps(report))
        with self.assertRaises(RuntimeError):
            run.advance()
        self.assertEqual(len(engine.writes), 2)

    def test_replayed_or_changed_event_is_rejected_before_any_extra_work(self):
        fixture, engine = case(), Engine()
        run = IncrementalTransferRun(fixture, engine=engine, raw_reader=lambda r: "answer")
        run.advance(fixture["events"][0])
        with self.assertRaises(ValueError):
            run.advance(fixture["events"][0])
        run.advance(fixture["events"][1])
        changed = deepcopy(fixture["events"][2])
        changed["source"]["source"]["text"] = "CHANGED_PREFIX"
        with self.assertRaises(ValueError):
            run.advance(changed)
        self.assertEqual(len(engine.writes), 1)
        result = run.run()
        self.assertEqual(len(engine.writes), 2)
        self.assertEqual(result["status"], "completed")

    def test_silent_approval_and_duplicate_event_ids_are_rejected(self):
        for extra in (dict(op="review", event_id="review", choice="approve"), case()["events"][0]):
            fixture = case()
            fixture["events"].append(extra)
            engine = Engine()
            with self.assertRaises(ValueError):
                IncrementalTransferRun(fixture, engine=engine, raw_reader=lambda r: None)
            self.assertEqual(engine.resets, 0)
            self.assertEqual(engine.writes, [])

    def test_distinct_repeated_arrivals_are_not_deduplicated_or_cached(self):
        fixture = case()
        fixture["events"][2]["source"] = deepcopy(fixture["events"][0]["source"])
        engine = Engine()
        report = run_case(fixture, engine=engine, raw_reader=lambda r: "answer")
        self.assertEqual(len(engine.writes), 2)
        first, second = report["source_arrivals"]
        self.assertEqual(first["source_id"], second["source_id"])
        self.assertNotEqual(first["event_id"], second["event_id"])
        self.assertNotEqual(first["session_index"], second["session_index"])
        other = case()
        other["events"][0]["source"]["source"]["text"] = "DIFFERENT_HISTORY"
        newer = run_case(other, engine=engine, raw_reader=lambda r: "answer")
        self.assertEqual(engine.resets, 2)
        self.assertEqual(len(engine.writes), 4)
        self.assertNotEqual(report["case_sha256"], newer["case_sha256"])
        self.assertEqual(len(newer["final_persistent_state"]["chunk_bank"]), 2)

    def test_unexpected_external_state_change_is_caught_before_next_event(self):
        engine = Engine()
        run = IncrementalTransferRun(case(), engine=engine, raw_reader=lambda r: None)
        run.advance()
        engine.store.values.append({"foreign_history": "must not be used"})
        with self.assertRaises(TransferInterrupted) as raised:
            run.advance()
        self.assertEqual(raised.exception.report["interruption"]["phase"], "prefix_integrity")
        self.assertEqual(engine.reads, [])

    def test_raw_failure_and_serializer_failure_are_not_completion(self):
        def broken_raw(record):
            raise RuntimeError("raw failed")
        with self.assertRaises(TransferInterrupted) as raised:
            run_case(case(), engine=Engine(), raw_reader=broken_raw)
        self.assertEqual(raised.exception.report["completed_native_queries"], 1)
        self.assertEqual(raised.exception.report["completed_paired_queries"], 0)
        self.assertIn("raw_reader_input", raised.exception.report["event_traces"][-1])
        with self.assertRaises(TransferInterrupted) as raised:
            run_case(case(), engine=Engine(fail_serialize=True), raw_reader=lambda r: "answer")
        report = raised.exception.report
        self.assertEqual(report["status"], "interrupted")
        self.assertEqual(report["native_serialization_error"], "ValueError")
        self.assertEqual(report["interruption"]["event_id"], "e0")
        self.assertEqual(report["interruption"]["event_index"], 0)
        self.assertEqual(report["completed_events"], 0)
        self.assertEqual(report["completed_native_sessions"], 1)
        self.assertEqual(report["event_traces"][-1]["status"], "interrupted")

    def test_final_callback_failure_names_executed_event_and_preserves_uncommitted_native_work(self):
        def fail_final(report):
            if (report["status"] == "running" and report["phase"] == "event_executed"
                    and report["event_traces"][-1]["event_id"] == "e3"):
                raise OSError("output publication failed")
        with self.assertRaises(TransferInterrupted) as raised:
            run_case(case(), engine=Engine(), raw_reader=lambda r: "answer", progress_callback=fail_final)
        report = raised.exception.report
        self.assertEqual(report["status"], "interrupted")
        self.assertEqual(report["interruption"]["event_id"], "e3")
        self.assertEqual(report["interruption"]["event_index"], 3)
        self.assertEqual(report["completed_events"], 3)
        self.assertEqual(report["completed_native_queries"], 2)
        self.assertEqual(report["completed_paired_queries"], 1)
        self.assertEqual(report["event_traces"][-1]["status"], "interrupted")
        self.assertIn("raw_reader_result", report["event_traces"][-1])

    def test_all_exported_fixtures_match_original_checkpoint_prefixes(self):
        exported = json.loads((ROOT / "evaluation/cupmem/transfer-inputs.json").read_text())
        total_sources = total_queries = no_query_cases = 0
        for fixture in exported["git"] + exported["timeline"]:
            calls, engine = [], Engine()
            result = run_case(fixture, engine=engine, raw_reader=lambda record: calls.append(record))
            expected = [native_record_at(fixture, i) for i, e in enumerate(fixture["events"]) if e["op"] == "ask"]
            self.assertEqual(calls, expected)
            self.assertEqual(result["status"], "completed")
            self.assertEqual(result["owner_review"], "unsupported_native_owner_review; no approval applied")
            total_sources += len(engine.writes)
            total_queries += len(calls)
            no_query_cases += not bool(calls)
            if not calls:
                self.assertEqual(len(result["native_result"]["session_logs"]), 3)
                self.assertEqual(result["native_result"]["query_logs"], {})
        self.assertEqual((total_sources, total_queries, no_query_cases), (280, 146, 54))


if __name__ == "__main__":
    unittest.main()
