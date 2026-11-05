"""Audited, provider-injected native and cited QA over one fixed source stream.

No provider, scoring, retrieval repair, truncation, prompted review, or owner
approval is implemented here. The caller passes one verified frozen actor case.
Native operations remain native traces, never classified as review proposals.

Required callbacks:
* native_raw_reader(record) -> {"raw": str, "packet": build_native_raw_packet(...)}
* cited_generate(packet) -> raw str
* request_events() -> flushed append-only request AND response audit events
* set_context(**context) -> set the transport's context for subsequent requests

The engine must retain debug_trace.query.answer_composer_raw_payload. Binding
uses the successful physical response matching that exact native payload. JSON
repair is never performed here. A native retry that cannot be bound is an
explicit adapter failure, not evidence that native QA was incorrect.
"""
from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path

from . import upstream
from .provenance import digest
from .readers import build_cup_qa_packet, build_raw_qa_packet, parse_qa_output, sources_from_native_record
from .transfer_runtime import IncrementalTransferRun, TransferInterrupted, persistent_snapshot


def _copy(value):
    return json.loads(json.dumps(value, ensure_ascii=False, allow_nan=False))


class PairBindingError(ValueError):
    def __init__(self, reason, **details):
        self.reason, self.details = reason, _copy(details)
        super().__init__(reason)


class PairedTransferInterrupted(RuntimeError):
    def __init__(self, report):
        self.report = _copy(report)
        super().__init__("Paired transfer interrupted; see preserved report.interruption")


class OfficialRawPromptBuilder:
    """Verify upstream once and load only its two pure prompt functions."""
    def __init__(self, upstream_root):
        self.root = Path(upstream_root).resolve()
        self.verified_files = upstream.verify_source(self.root)
        path = self.root / "STALE/Evaluation/run_target_model.py"
        self.source_sha256 = sha256(path.read_bytes()).hexdigest()
        self.functions = upstream.definitions(path, ["format_haystack", "build_prompts"], {})

    def packet(self, record):
        if not isinstance(record, dict) or len(record.get("probing_queries", {})) != 1:
            raise PairBindingError("raw_record_requires_one_current_question")
        label = next(iter(record["probing_queries"]))
        sources, question = sources_from_native_record(record, query_label=label)
        history = self.functions["format_haystack"](record["haystack_session"], record["timestamps"])
        system, user = self.functions["build_prompts"](history, question, label)
        return dict(schema="cupmem-official-raw-native-packet-v1", system=system, user=user,
                    input_sha256=digest(dict(system=system, user=user)), record_sha256=digest(record),
                    query_label=label, visible_source_arrivals=len(sources), truncated=False,
                    prompt_source_sha256=self.source_sha256, upstream_revision=upstream.REVISION,
                    label="official prompt functions, full current attributed history; separate native raw baseline")


@lru_cache(maxsize=4)
def _prompt_builder(upstream_root):
    return OfficialRawPromptBuilder(upstream_root)


def build_native_raw_packet(record, *, upstream_root):
    """Original official formatting, no source shortening or context fallback.

    An immutable version directory is required. Verification/function loading is
    cached per resolved directory; create a new version directory for a change.
    The transport must fail explicitly if the full packet exceeds its context.
    """
    return _prompt_builder(str(Path(upstream_root).resolve())).packet(record)


def _completion(response):
    if not isinstance(response, dict) or response.get("event") != "response":
        raise PairBindingError("missing_response_event")
    if type(response.get("status")) is not int or not 200 <= response["status"] < 300:
        raise PairBindingError("http_response_not_successful", status=response.get("status"))
    choices = response.get("body", {}).get("choices")
    if not isinstance(choices, list) or len(choices) != 1:
        raise PairBindingError("response_requires_one_choice")
    choice = choices[0]
    if choice.get("finish_reason") != "stop":
        raise PairBindingError("response_not_uncensored_stop", finish_reason=choice.get("finish_reason"))
    message = choice.get("message", {})
    if message.get("role", "assistant") != "assistant" or not isinstance(message.get("content"), str):
        raise PairBindingError("response_requires_assistant_text")
    return message["content"]


def _pairs(events):
    requests, responses = {}, {}
    for event in events:
        kind, rid = event.get("event"), event.get("request_id")
        if kind not in {"request", "response"}:
            continue
        if type(rid) is not int:
            raise PairBindingError("audit_request_id_must_be_integer")
        target = requests if kind == "request" else responses
        if rid in target:
            raise PairBindingError("duplicate_audit_event", event=kind, request_id=rid)
        target[rid] = event
    return [(request, responses.get(rid)) for rid, request in requests.items()]


def _context_matches(request, uid, label, arm):
    context = request.get("context", {})
    return (isinstance(context, dict) and context.get("uid") == uid
            and context.get("query_label") == label and context.get("arm") == arm)


def bind_composer(events, query_trace, *, uid, query_label, question):
    """Select a successful actual composer attempt, never the first candidate."""
    payload = query_trace.get("debug_trace", {}).get("query", {}).get("answer_composer_raw_payload")
    if not isinstance(payload, dict):
        raise PairBindingError("missing_native_composer_raw_payload_enable_debug_trace")
    matches, diagnostics = [], []
    for request, response in _pairs(events):
        if not _context_matches(request, uid, query_label, "cupmem"):
            continue
        rid = request["request_id"]
        try:
            raw = _completion(response)
            try:
                actual = json.loads(raw)
            except (TypeError, ValueError):
                raise PairBindingError("native_response_not_strict_json_no_adapter_repair") from None
            if actual != payload:
                continue
            body = request.get("body", {})
            if request.get("body_sha256") != digest(body):
                raise PairBindingError("request_body_hash_mismatch")
            messages = body.get("messages", [])
            try:
                sent = json.loads(messages[-1]["content"])
                if messages[-1].get("role") != "user" or not isinstance(sent, dict):
                    raise ValueError()
            except (ValueError, TypeError, KeyError, IndexError):
                raise PairBindingError("matching_response_has_no_bindable_final_composer_payload") from None
            if (sent.get("query") != question or not isinstance(sent.get("canonical_answer_grounding"), dict)
                    or "constraint_set" not in sent):
                raise PairBindingError("matching_response_has_no_bindable_final_composer_payload")
            matches.append(dict(request_event=request, response_event=response, raw=raw,
                                parsed_response=actual, response_sha256=digest(response),
                                binding="exact successful response JSON equals native composer raw payload"))
        except PairBindingError as exc:
            diagnostics.append(dict(request_id=rid, reason=exc.reason, **exc.details))
    if len(matches) != 1:
        raise PairBindingError("composer_response_binding_not_unique", matches=len(matches), diagnostics=diagnostics)
    return _copy(dict(**matches[0], nonmatching_attempts=diagnostics))


def bind_reader(events, packet, raw, *, uid, query_label, arm):
    """Require actual sent full messages and returned raw text, not an echo claim."""
    expected = [dict(role="system", content=packet["system"]), dict(role="user", content=packet["user"])]
    matches, diagnostics = [], []
    for request, response in _pairs(events):
        if not _context_matches(request, uid, query_label, arm):
            continue
        rid, body = request["request_id"], request.get("body", {})
        try:
            if request.get("body_sha256") != digest(body):
                raise PairBindingError("request_body_hash_mismatch")
            if body.get("messages") != expected:
                raise PairBindingError("actual_reader_messages_differ_from_fixed_packet")
            returned = _completion(response)
            if returned != raw:
                raise PairBindingError("actual_reader_output_differs_from_callback")
            matches.append(dict(request_event=request, response_event=response,
                                response_sha256=digest(response), input_sha256=packet["input_sha256"]))
        except PairBindingError as exc:
            diagnostics.append(dict(request_id=rid, reason=exc.reason, **exc.details))
    if len(matches) != 1:
        raise PairBindingError("reader_audit_binding_not_unique", matches=len(matches), diagnostics=diagnostics)
    return _copy(dict(**matches[0], nonmatching_attempts=diagnostics))


class PairedTransferRun:
    def __init__(self, case, *, engine, native_raw_reader, cited_generate,
                 request_events, set_context, upstream_root, sample_index=0, progress_callback=None):
        for name, value in dict(native_raw_reader=native_raw_reader, cited_generate=cited_generate,
                                request_events=request_events, set_context=set_context).items():
            if not callable(value):
                raise TypeError(name + " must be injected")
        self.case, self.engine = _copy(case), engine
        self.raw_reader, self.cited_generate = native_raw_reader, cited_generate
        self.request_events, self.set_context = request_events, set_context
        self.progress_callback = progress_callback
        self.builder = _prompt_builder(str(Path(upstream_root).resolve()))
        self.native = IncrementalTransferRun(case, engine=engine, raw_reader=self._raw,
                                             sample_index=sample_index, progress_callback=self._capture)
        self.status, self.phase = "not_started", "not_started"
        self.index = 0
        self.pairs = []
        self.current = None
        self.native_report = self.native.report()
        self.interruption = None
        self.audit_seen = []
        self.native_audit_start = self.raw_audit_start = 0
        self.post_reader_state = None

    def _audit(self):
        events = _copy(self.request_events())
        if not isinstance(events, list) or any(not isinstance(event, dict) for event in events):
            raise PairBindingError("audit_callback_requires_event_list")
        if events[:len(self.audit_seen)] != self.audit_seen:
            raise PairBindingError("audit_events_changed_or_disappeared")
        self.audit_seen = events
        return events

    def _context(self, arm, *, phase, query_label=None, event_id=None):
        context = dict(arm=arm, uid=self.case["case_id"], phase=phase)
        if query_label is not None:
            context["query_label"] = query_label
        if event_id is not None:
            context["event_id"] = event_id
        self.set_context(**context)

    def _capture(self, report):
        self.native_report = _copy(report)
        phase = report["phase"]
        event = self.case["events"][self.index]
        if phase == "before_ingest":
            self._context("cupmem", phase="write", event_id=event["event_id"])
        elif phase == "before_native_query":
            self.native_audit_start = len(self._audit())
            self._context("cupmem", phase="query", query_label=event["event_id"], event_id=event["event_id"])
        elif phase == "before_raw_query":
            native_row = report["event_traces"][-1]
            self.current["native_answer"] = _copy(native_row["native_query_trace"]["answer"])
            self.current["query_time_trace_sha256"] = native_row["query_time_trace_sha256"]
            self.raw_audit_start = len(self._audit())
            self._context("raw_native", phase="query", query_label=event["event_id"], event_id=event["event_id"])
        self._emit()

    def _raw(self, record):
        packet = self.builder.packet(record)
        self.current["raw_native"] = dict(status="running", packet=packet)
        try:
            output = _copy(self.raw_reader(_copy(record)))
            self.current["raw_native"]["callback_output"] = output
            if not isinstance(output, dict) or not isinstance(output.get("raw"), str) or output.get("packet") != packet:
                raise PairBindingError("native_raw_callback_must_return_exact_official_packet_and_raw_text")
            binding = bind_reader(self._audit()[self.raw_audit_start:], packet, output["raw"],
                                  uid=record["uid"], query_label=packet["query_label"], arm="raw_native")
            self.current["raw_native"].update(status="completed", raw=output["raw"], audit_binding=binding)
            return output
        except PairBindingError as exc:
            # IncrementalTransferRun intentionally stores only exception types;
            # retain our non-secret structural diagnostics before it wraps us.
            self.current["raw_native"].update(status="adapter_error", error=dict(reason=exc.reason, **exc.details))
            raise

    def report(self):
        return _copy(dict(schema="cupmem-transfer-pair-v1", status=self.status, phase=self.phase,
                          case_id=self.case["case_id"], case_sha256=digest(self.case),
                          completed_events=self.index, expected_events=len(self.case["events"]),
                          completed_cited_pairs=sum(row["status"] == "completed" for row in self.pairs),
                          paired_queries=self.pairs, native_runtime=self.native_report,
                          post_reader_persistent_state=self.post_reader_state,
                          owner_review="unsupported_native_owner_review; no approval applied",
                          review_detection="unsupported; native updates are unmapped, not zero classified proposals",
                          semantic_scoring="not performed; parsed citations establish format/source scope only",
                          interruption=self.interruption))

    def _emit(self):
        if self.progress_callback:
            before = digest(persistent_snapshot(self.engine))
            self.progress_callback(self.report())
            if digest(persistent_snapshot(self.engine)) != before:
                raise PairBindingError("progress_callback_mutated_native_persistent_memory")

    def _cited(self, arm, packet, label):
        field = "raw_cited" if arm == "raw_cited" else "cupmem_cited"
        row = self.current[field] = dict(status="running", packet=_copy(packet))
        self.phase = field
        self._context(arm, phase="cited_query", query_label=label, event_id=label)
        before = len(self._audit())
        self._emit()
        raw = self.cited_generate(_copy(packet))
        row["raw"] = _copy(raw)
        row["parsed"] = parse_qa_output(raw, packet)
        row["audit_binding"] = bind_reader(self._audit()[before:], packet, raw,
                                            uid=self.case["case_id"], query_label=label, arm=arm)
        # Invalid model JSON is a preserved model-format outcome, not repaired.
        row["status"] = "completed"

    def _finish_query(self, native_row):
        self.phase = "composer_binding"
        label, question = native_row["event_id"], native_row["question"]
        self.current["native_answer"] = _copy(native_row["native_query_trace"]["answer"])
        self.current["query_time_trace_sha256"] = native_row["query_time_trace_sha256"]
        composer = bind_composer(self._audit()[self.native_audit_start:self.raw_audit_start],
                                 native_row["native_query_trace"], uid=self.case["case_id"],
                                 query_label=label, question=question)
        self.current["composer_binding"] = composer
        sources, original_question = sources_from_native_record(native_row["raw_reader_input"], query_label=label)
        if original_question != question:
            raise PairBindingError("native_question_prefix_mismatch")
        raw = build_raw_qa_packet(sources, question)
        cup = build_cup_qa_packet(sources, question, request_event=composer["request_event"],
                                  trace=native_row["query_time_trace"], query_label=label,
                                  expected_state_sha256=native_row["native_query_state_sha256"])
        self.current["prepared_packets"] = dict(raw=_copy(raw), cupmem=_copy(cup))
        if not cup["ready"]:
            raise PairBindingError("cupmem_cited_packet_not_ready", adapter_stage=cup["stage"], errors=cup["errors"])
        if raw["system"] != cup["system"]:
            raise PairBindingError("paired_cited_system_prompts_differ")
        before = digest(persistent_snapshot(self.engine))
        for arm, packet in (("raw_cited", raw), ("cupmem_cited", cup)):
            self._cited(arm, packet, label)
            self.post_reader_state = persistent_snapshot(self.engine)
            if digest(self.post_reader_state) != before:
                raise PairBindingError("cited_callback_mutated_native_persistent_memory", arm=arm)
        self.current["status"] = "completed"

    def advance(self):
        if self.status in {"completed", "interrupted"}:
            raise RuntimeError("Paired run is terminal; no implicit replay or resume")
        event = self.case["events"][self.index]
        self.status, self.phase = "running", "native_event"
        if event["op"] == "ask":
            self.current = dict(event_id=event["event_id"], event_index=self.index, status="running")
            self.pairs.append(self.current)
        else:
            self.current = None
        try:
            self.native_report = self.native.advance(event)
            if event["op"] == "ask":
                self._finish_query(self.native_report["event_traces"][-1])
            self.phase = "paired_event_executed"
            self._emit()
            self.index += 1
            self.status = "completed" if self.index == len(self.case["events"]) else "running"
            self.phase = "completed" if self.status == "completed" else "event_completed"
            return self.report()
        except BaseException as exc:
            if isinstance(exc, TransferInterrupted):
                self.native_report = exc.report
            else:
                self.native_report = self.native.report()
            self.interruption = dict(event_id=event["event_id"], event_index=self.index,
                                     phase=self.phase, error_type=type(exc).__name__,
                                     interpretation="execution/adapter interruption, not a native QA score")
            if isinstance(exc, PairBindingError):
                self.interruption.update(reason=exc.reason, details=exc.details)
            if isinstance(exc, TransferInterrupted):
                self.interruption["native_interruption"] = exc.report["interruption"]
            if self.current:
                self.current["status"] = "interrupted"
                for arm in ("raw_native", "raw_cited", "cupmem_cited"):
                    if self.current.get(arm, {}).get("status") == "running":
                        self.current[arm]["status"] = "interrupted"
            self.status = "interrupted"
            try:
                self.post_reader_state = persistent_snapshot(self.engine)
            except BaseException as snapshot_error:
                self.interruption["snapshot_error_type"] = type(snapshot_error).__name__
            try:
                self._emit()
            except BaseException as callback_error:
                self.interruption["progress_callback_error_type"] = type(callback_error).__name__
            raise PairedTransferInterrupted(self.report()) from None

    def run(self):
        while self.status not in {"completed", "interrupted"}:
            self.advance()
        if self.status != "completed":
            raise PairedTransferInterrupted(self.report())
        return self.report()


def run_paired_case(case, **kwargs):
    return PairedTransferRun(case, **kwargs).run()
