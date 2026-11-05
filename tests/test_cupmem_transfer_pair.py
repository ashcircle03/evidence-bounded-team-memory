"""Offline orchestration with fake generation and actual pinned serialization."""
from copy import deepcopy
import json
from pathlib import Path
import unittest

from evaluation.cupmem.provenance import digest
from evaluation.cupmem.transfer_inputs import native_record_at
from evaluation.cupmem.transfer_pair import (
    PairedTransferInterrupted, PairedTransferRun, build_native_raw_packet,
)
from team_memory.store import digest as source_id
from tests.test_cupmem_transfer_runtime import Item, PINNED, UPSTREAM


class FakeAudit:
    def __init__(self):
        self.context, self.events, self.rid = {}, [], 0

    def set_context(self, **context):
        self.context = deepcopy(context)

    def post(self, messages, raw, *, finish="stop", wrong_uid=False):
        self.rid += 1
        body = dict(model="fake-no-provider", messages=deepcopy(messages))
        context = deepcopy(self.context)
        if wrong_uid:
            context["uid"] = "another-case"
        self.events.append(dict(event="request", request_id=self.rid, body=body,
                                body_sha256=digest(body), context=context))
        self.events.append(dict(event="response", request_id=self.rid, status=200,
                                body={"choices": [dict(message=dict(role="assistant", content=raw), finish_reason=finish)]}))


class FakeStore:
    def __init__(self):
        self.items = []

    def to_snapshot(self):
        return dict(active_profile={"b/t": deepcopy(self.items)}, stale_archive=[], unknown_current=[])


class FakeEngine(PINNED.SampleRunnerMixin):
    def __init__(self, audit, *, retry=False, selected=True, malformed=False, wrong_uid=False):
        self.audit = audit
        self.retry, self.selected = retry, selected
        self.malformed, self.wrong_uid = malformed, wrong_uid
        self.reset()

    def reset(self):
        self.store, self.chunk_bank, self.delta_store = FakeStore(), [], []

    def _chunk_trace_dict(self, chunk):
        return deepcopy(chunk.to_dict())

    def _delta_trace_dict(self, delta):
        return deepcopy(delta.to_dict())

    def process_session(self, *, session, session_index, session_time):
        i = session_index
        self.chunk_bank.append(Item(dict(chunk_id=f"c{i}", session_id=f"s_{i:03d}", source_turn_ids=["t_0"], text="Generated summary")))
        self.delta_store.append(Item(dict(delta_id=f"d{i}", evidence_chunk_ids=[f"c{i}"])))
        self.store.items.append(dict(item_id=f"p{i}", bucket="b", local_track="t", value="Generated value",
                                    status="ACTIVE", active_strength="STRONG", evidence_chunk_ids=[f"c{i}"],
                                    source_delta_ids=[f"d{i}"], revision_history=[]))
        return dict(session_id=f"s_{i:03d}", session_index=i, session_time=session_time,
                    user_turns=[dict(turn_id="t_0", content=session[0]["content"])],
                    invalidation_logs=[], native_update_trace={"operation": "ADD", "item_id": f"p{i}"})

    def answer_query(self, *, query_label, query_text):
        i = len(self.store.items) - 1
        selected = [dict(hit_ref=dict(source="active", source_detail="strong_active", id=f"p{i}", bucket="b", local_track="t"),
                         status_label="ACTIVE_STRONG", text="Generated value")] if self.selected else []
        grounding = dict(decisive_basis=selected, supporting_basis=[], blocker_basis=[], old_premise_safe=True)
        payload = dict(query=query_text, canonical_answer_grounding=grounding, constraint_set=None)
        messages = [dict(role="system", content="fake native composer"), dict(role="user", content=json.dumps(payload))]
        result = dict(answer="native answer", brief_rationale="native rationale")
        if self.retry:
            self.audit.post(messages, '{"answer":')
        raw = json.dumps(result)
        if self.malformed:
            raw = "```json\n" + raw + "\n```"  # Simulated upstream parse/repair; adapter must not repair.
        self.audit.post(messages, raw, wrong_uid=self.wrong_uid)
        return dict(query_label=query_label, query_text=query_text, answer=result,
                    debug_trace={"query": {"answer_composer_raw_payload": result}})


def env(text, date):
    return dict(owner="Author", observed_at=date, source=dict(speaker="Author", location="source://" + date, text=text))


def case():
    return dict(case_id="paired-fixture", events=[
        dict(op="ingest", event_id="s0", source=env("Rate 10 under condition A.", "2025-01-01")),
        dict(op="ask", event_id="q0", question="What is the rate?"),
        dict(op="ingest", event_id="s1", source=env("Future rate 20 under condition B.", "2025-01-02")),
        dict(op="ask", event_id="q1", question="What is the new rate?"),
    ])


class PairedTransferTests(unittest.TestCase):
    def setup_run(self, *, fixture=None, engine_kwargs=None, bad_raw_input=False,
                  invalid_cited=False, fail_cup=False, mutate_cited=False):
        fixture = fixture or case()
        audit = FakeAudit()
        engine = FakeEngine(audit, **(engine_kwargs or {}))
        raw_calls, cited_calls, progress = [], [], []
        def native_raw_reader(record):
            raw_calls.append(deepcopy(record))
            packet = build_native_raw_packet(record, upstream_root=UPSTREAM)
            messages = [dict(role="system", content=packet["system"]), dict(role="user", content=packet["user"])]
            if bad_raw_input:
                messages[-1]["content"] = "silently shortened"
            audit.post(messages, "raw native answer")
            return dict(raw="raw native answer", packet=packet)
        def cited_generate(packet):
            cited_calls.append(deepcopy(packet))
            if fail_cup and packet["arm"] == "cupmem":
                raise OSError("provider unavailable")
            data = json.loads(packet["user"])
            if invalid_cited:
                raw = '{"kind":'
            elif not data["sources"]:
                raw = '{"kind":"insufficient","answers":[]}'
            else:
                source = data["sources"][0]
                value = "20" if "20" in source["source"]["text"] else "10"
                raw = json.dumps(dict(kind="single", answers=[dict(source=source["id"], quote=source["source"]["text"],
                                       answer=value, condition="")]))
            audit.post([dict(role="system", content=packet["system"]), dict(role="user", content=packet["user"])], raw)
            if mutate_cited:
                engine.store.items[0]["value"] = "illicit reader mutation"
            return raw
        run = PairedTransferRun(fixture, engine=engine, native_raw_reader=native_raw_reader,
                                cited_generate=cited_generate, request_events=lambda: deepcopy(audit.events),
                                set_context=audit.set_context, upstream_root=UPSTREAM, progress_callback=progress.append)
        return run, audit, engine, raw_calls, cited_calls, progress

    def test_two_prefixes_native_and_cited_are_separate_full_and_selected(self):
        run, audit, engine, raw_calls, cited_calls, progress = self.setup_run()
        run.advance()
        first = run.advance()
        self.assertNotIn("Future rate", json.dumps(first))
        self.assertNotIn("new rate", json.dumps(first))
        result = run.run()
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["completed_events"], 4)
        self.assertEqual(result["completed_cited_pairs"], 2)
        self.assertEqual(raw_calls, [native_record_at(case(), i) for i in (1, 3)])
        first_pair, last_pair = result["paired_queries"]
        self.assertEqual(first_pair["native_answer"]["answer"], "native answer")
        self.assertEqual(first_pair["raw_native"]["raw"], "raw native answer")
        raw, cup = last_pair["prepared_packets"]["raw"], last_pair["prepared_packets"]["cupmem"]
        self.assertEqual(raw["system"], cup["system"])
        self.assertEqual(len(json.loads(raw["user"])["sources"]), 2)
        self.assertEqual(len(json.loads(cup["user"])["sources"]), 1)
        self.assertEqual(cup["source_ids"], [source_id(case()["events"][2]["source"])])
        for packet in cited_calls:
            self.assertEqual(json.loads(packet["user"])["relations"], [])
        self.assertIn("unsupported", result["review_detection"])
        self.assertIn("no approval", result["owner_review"])
        self.assertEqual(result["native_runtime"]["native_result"]["session_logs"][0]["native_update_trace"]["operation"], "ADD")
        self.assertTrue(progress)
        with self.assertRaises(RuntimeError):
            run.advance()

    def test_composer_retry_selects_successful_response_not_first_request(self):
        run, audit, *_ = self.setup_run(engine_kwargs={"retry": True})
        result = run.run()
        pair = result["paired_queries"][0]
        binding = pair["composer_binding"]
        self.assertEqual(binding["request_event"]["request_id"], 2)
        self.assertEqual(binding["nonmatching_attempts"][0]["request_id"], 1)
        self.assertEqual(binding["parsed_response"], pair["native_answer"])

    def test_no_selection_keeps_empty_cup_sources_and_native_answer(self):
        run, *_ = self.setup_run(engine_kwargs={"selected": False})
        result = run.run()
        for pair in result["paired_queries"]:
            self.assertEqual(pair["prepared_packets"]["cupmem"]["source_ids"], [])
            self.assertEqual(pair["cupmem_cited"]["parsed"]["kind"], "insufficient")
            self.assertEqual(pair["native_answer"]["answer"], "native answer")

    def test_malformed_cited_output_is_retained_unrepaired_not_execution_success_claim(self):
        run, *_ = self.setup_run(invalid_cited=True)
        result = run.run()
        self.assertEqual(result["status"], "completed")
        for pair in result["paired_queries"]:
            for arm in ("raw_cited", "cupmem_cited"):
                self.assertEqual(pair[arm]["parsed"]["kind"], "invalid")
                self.assertEqual(pair[arm]["raw"], '{"kind":')
        self.assertIn("not performed", result["semantic_scoring"])

    def test_actual_raw_prompt_must_match_not_merely_callback_echo(self):
        run, audit, engine, raw_calls, cited_calls, _ = self.setup_run(bad_raw_input=True)
        with self.assertRaises(PairedTransferInterrupted) as raised:
            run.run()
        result = raised.exception.report
        self.assertEqual(result["completed_events"], 1)
        self.assertEqual(result["native_runtime"]["completed_native_queries"], 1)
        self.assertEqual(result["paired_queries"][0]["native_answer"]["answer"], "native answer")
        error = result["paired_queries"][0]["raw_native"]["error"]
        self.assertEqual(error["diagnostics"][0]["reason"], "actual_reader_messages_differ_from_fixed_packet")
        self.assertEqual(cited_calls, [])
        self.assertFalse(result["paired_queries"][0]["raw_native"]["packet"]["truncated"])

    def test_wrong_case_or_repaired_native_output_is_adapter_failure_with_native_preserved(self):
        for kwargs in ({"wrong_uid": True}, {"malformed": True}):
            run, audit, engine, raw_calls, cited_calls, _ = self.setup_run(engine_kwargs=kwargs)
            with self.assertRaises(PairedTransferInterrupted) as raised:
                run.run()
            result = raised.exception.report
            self.assertEqual(result["interruption"]["reason"], "composer_response_binding_not_unique")
            self.assertEqual(result["paired_queries"][0]["native_answer"]["answer"], "native answer")
            self.assertEqual(result["paired_queries"][0]["raw_native"]["status"], "completed")
            self.assertEqual(cited_calls, [])
            self.assertEqual(result["native_runtime"]["completed_events"], 2)
            self.assertEqual(result["completed_events"], 1)

    def test_second_cited_failure_retains_first_result_and_stops_future_ingest(self):
        run, audit, engine, raw_calls, cited_calls, _ = self.setup_run(fail_cup=True)
        with self.assertRaises(PairedTransferInterrupted) as raised:
            run.run()
        result = raised.exception.report
        pair = result["paired_queries"][0]
        self.assertEqual(pair["raw_cited"]["status"], "completed")
        self.assertEqual(pair["cupmem_cited"]["status"], "interrupted")
        self.assertEqual(result["interruption"]["phase"], "cupmem_cited")
        self.assertEqual(result["interruption"]["error_type"], "OSError")
        self.assertEqual(len(engine.chunk_bank), 1)
        self.assertEqual(result["completed_cited_pairs"], 0)

    def test_cited_mutation_is_checked_even_at_final_checkpoint(self):
        fixture = case(); fixture["events"] = fixture["events"][:2]
        run, *_ = self.setup_run(fixture=fixture, mutate_cited=True)
        with self.assertRaises(PairedTransferInterrupted) as raised:
            run.run()
        result = raised.exception.report
        self.assertEqual(result["interruption"]["reason"], "cited_callback_mutated_native_persistent_memory")
        self.assertEqual(result["post_reader_persistent_state"]["final_profile_snapshot"]["active_profile"]["b/t"][0]["value"], "illicit reader mutation")

    def test_builder_rejects_extra_gold_or_multiple_questions(self):
        record = native_record_at(case(), 1)
        record["M_new"] = "gold must never be sent"
        with self.assertRaises(ValueError):
            build_native_raw_packet(record, upstream_root=UPSTREAM)
        record = native_record_at(case(), 1)
        record["probing_queries"]["future"] = "Future question"
        with self.assertRaises(ValueError):
            build_native_raw_packet(record, upstream_root=UPSTREAM)

    def test_one_actual_frozen_stream_runs_all_original_checkpoints_without_reviews(self):
        root = Path(__file__).resolve().parents[1]
        from evaluation.cupmem.transfer_inputs import verify_freeze
        verify_freeze(root)
        fixture = json.loads((root / "evaluation/cupmem/transfer-inputs.json").read_text())["timeline"][0]
        run, audit, engine, raw_calls, cited_calls, _ = self.setup_run(fixture=fixture)
        result = run.run()
        indices = [i for i, event in enumerate(fixture["events"]) if event["op"] == "ask"]
        self.assertEqual(result["completed_cited_pairs"], len(indices))
        self.assertEqual(raw_calls, [native_record_at(fixture, i) for i in indices])
        for pair, index in zip(result["paired_queries"], indices):
            expected = [event["source"] for event in fixture["events"][:index + 1] if event["op"] == "ingest"]
            supplied = json.loads(pair["prepared_packets"]["raw"]["user"])["sources"]
            self.assertEqual([{k: row[k] for k in ("owner", "observed_at", "source")} for row in supplied], expected)
            self.assertEqual(pair["prepared_packets"]["cupmem"]["source_ids"], [source_id(expected[-1])])
        self.assertEqual(result["owner_review"], "unsupported_native_owner_review; no approval applied")


if __name__ == "__main__":
    unittest.main()
