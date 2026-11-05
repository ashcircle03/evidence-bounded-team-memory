"""Dependency-injected incremental native-QA execution; no provider or prompts.

The caller supplies an unmodified CUPMem engine and a raw-reader callback. Both
arms see the same current source prefix. The callback receives a source-only
native record, not a prompt invented here. Model/provider setup, prompted review,
cited reading, approval, scoring, and Slurm execution are deliberately absent.

Every run begins with the engine's public reset(). There is no resume or cache
API. Serialized snapshots are evidence, not instructions for restoring private
engine internals. Exact duplicate source arrivals with distinct event IDs are
processed again; duplicate/replayed event IDs or changed expected events are
rejected. That preserves the repeated-arrival diagnostic without silently
deduplicating it.
"""
from __future__ import annotations

from hashlib import sha256
import json
import time

from team_memory.store import digest as source_id
from .transfer_inputs import attributed_session, envelope_only, native_record_at


def _copy(value):
    """Detach JSON evidence from mutable engine/callback objects."""
    return json.loads(json.dumps(value, ensure_ascii=False, allow_nan=False))


def _hash(value):
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    return sha256(raw).hexdigest()


def persistent_snapshot(engine):
    """Read only official store/model serialization, never restore private state."""
    return _copy({
        "final_profile_snapshot": engine.store.to_snapshot(),
        "chunk_bank": [chunk.to_dict() for chunk in engine.chunk_bank],
        "delta_store": [delta.to_dict() for delta in engine.delta_store],
    })


def native_trace_state_hash(trace):
    """Provenance-compatible hash of official trace serialization, not raw state.

    Official trace helpers can move/drop change_signal_summary and op_hint.
    Therefore this binding hash must not be taken from persistent_snapshot().
    Both representations are independently checked around a native query.
    """
    return _hash({key: trace[key] for key in ("final_profile_snapshot", "chunk_bank", "delta_store")})


class TransferInterrupted(RuntimeError):
    """A failed execution with preserved evidence; never a completion result."""
    def __init__(self, report):
        self.report = _copy(report)
        error = self.report.get("interruption", {})
        super().__init__("Transfer interrupted at " + str(error.get("phase")) +
                         " (" + str(error.get("error_type")) + ")")


class StateMutationError(RuntimeError):
    pass


def _validate_case(case):
    if set(case) != {"case_id", "events"} or not isinstance(case["case_id"], str) or not case["case_id"]:
        raise ValueError("Expected one actor case without evaluator metadata")
    if not isinstance(case["events"], list) or not case["events"]:
        raise ValueError("Expected nonempty actor events")
    seen = set()
    for event in case["events"]:
        op = event.get("op")
        expected = {"op", "event_id", "source" if op == "ingest" else "question"}
        if op not in {"ingest", "ask"} or set(event) != expected:
            raise ValueError("Only source ingestion and existing QA checkpoints are supported; reviews are not executable")
        eid = event["event_id"]
        if not isinstance(eid, str) or not eid or eid in seen:
            raise ValueError("Missing or duplicate event ID")
        seen.add(eid)
        if op == "ingest":
            envelope_only(event["source"])
        elif not isinstance(event["question"], str) or not event["question"]:
            raise ValueError("Expected the original nonempty question")


class IncrementalTransferRun:
    """Run a single fixed actor event stream with no semantic policy changes.

    ``raw_reader(record)`` receives exactly ``native_record_at(case, index)`` at
    each ask. The engine receives attributed sources and unchanged questions.
    ``progress_callback(report)`` is optional; it is called before work, when an
    event has executed but before committing its completion, and on interruption.
    The caller should save the final returned completed report separately.
    Exceptions from a callback also interrupt the run. Reports contain only
    already-visible source text, although the full actor-case hash binds the run.
    """
    def __init__(self, case, *, engine, raw_reader, sample_index=0, progress_callback=None,
                 clock=time.perf_counter):
        _validate_case(case)
        if not callable(raw_reader):
            raise TypeError("raw_reader must be explicitly injected")
        self._case = _copy(case)
        self._engine = engine
        self._raw_reader = raw_reader
        self._sample_index = sample_index
        self._callback = progress_callback
        self._clock = clock
        self._started = None
        self._status = "not_started"
        self._phase = "not_started"
        self._index = 0
        self._session_logs = []
        self._query_logs = {}
        self._events = []
        self._arrivals = []
        self._state = None
        self._state_sha256 = None
        self._initial_state_sha256 = None
        self._interruption = None
        self._executing_event_index = None

    def _take_state(self):
        state = persistent_snapshot(self._engine)
        return state, _hash(state)

    def _prefix(self):
        return [row["source"] for row in self._arrivals]

    def _emit(self):
        if self._callback is not None:
            self._callback(self.report())

    def _native_result(self):
        if self._started is None:
            return None
        # The official serializer is passed only already-observed metadata/logs.
        return _copy(self._engine._build_sample_result(
            item={"uid": self._case["case_id"]}, sample_index=self._sample_index,
            session_mode="full", selected_session_indices=list(range(len(self._session_logs))),
            session_logs=_copy(self._session_logs), query_logs=_copy(self._query_logs),
            run_status=self._status, current_phase=self._phase,
            sample_elapsed_seconds=self._clock() - self._started))

    def report(self):
        """Snapshot evidence; it never contains future source text or questions."""
        try:
            native = self._native_result()
            serialization_error = None
        except BaseException as exc:
            native = None
            serialization_error = type(exc).__name__
        return _copy(dict(
            schema="cupmem-transfer-native-runtime-v1", status=self._status, phase=self._phase,
            case_id=self._case["case_id"], case_sha256=_hash(self._case),
            scope="native write traces and paired QA only; not complete team-system evaluation",
            adapter="one exact attributed source per session, original arrival order; not native STALE data",
            owner_review="unsupported_native_owner_review; no approval applied",
            unimplemented=["prompted_review", "cited_reader", "evaluator", "provider_setup", "slurm", "resume", "cross_case_cache"],
            expected_events=len(self._case["events"]), completed_events=self._index,
            completed_native_sessions=len(self._session_logs), completed_native_queries=len(self._query_logs),
            completed_paired_queries=sum(e["op"] == "ask" and e["status"] == "completed" for e in self._events),
            source_arrivals=self._arrivals, event_traces=self._events,
            initial_persistent_state_sha256=self._initial_state_sha256,
            final_persistent_state=self._state, final_persistent_state_sha256=self._state_sha256,
            state_hash_scope=["store.to_snapshot()", "chunk_bank[*].to_dict()", "delta_store[*].to_dict()"],
            native_result=native, native_serialization_error=serialization_error,
            interruption=self._interruption))

    def _interrupt(self, exc):
        failed_phase = self._phase
        failed_index = self._executing_event_index if self._executing_event_index is not None else self._index
        # Native work may have completed even if serialization/publication did
        # not. Completion accounting must still refer to the failing event,
        # never the next event which has not executed.
        self._index = min(self._index, failed_index)
        self._status = "interrupted"
        self._interruption = dict(error_type=type(exc).__name__, phase=failed_phase,
                                  event_index=failed_index,
                                  event_id=self._case["events"][failed_index]["event_id"]
                                  if failed_index < len(self._case["events"]) else None)
        # Errors may happen after a partial writer mutation. Preserve the actual
        # current snapshot where available; never roll it back or call it success.
        try:
            self._state, self._state_sha256 = self._take_state()
        except BaseException as snapshot_error:
            self._interruption["snapshot_error_type"] = type(snapshot_error).__name__
        if self._events and self._events[-1]["event_index"] == failed_index:
            self._events[-1]["status"] = "interrupted"
            self._events[-1]["persistent_after_sha256"] = self._state_sha256
        try:
            self._emit()
        except BaseException as callback_error:
            self._interruption["progress_callback_error_type"] = type(callback_error).__name__
        raise TransferInterrupted(self.report()) from None

    def _start(self):
        self._phase = "reset"
        self._started = self._clock()
        self._engine.reset()
        self._state, self._state_sha256 = self._take_state()
        self._initial_state_sha256 = self._state_sha256
        self._status = "running"
        self._phase = "started"
        self._emit()

    def advance(self, event=None):
        """Execute exactly the next frozen event, optionally checking its bytes.

        Passing an old or modified event is rejected before any model work. This
        method cannot resume a serialized state or switch to a different case.
        """
        if self._status in {"completed", "interrupted"}:
            raise RuntimeError("Run is terminal; no implicit resume or replay")
        expected = self._case["events"][self._index]
        if event is not None and event != expected:
            raise ValueError("Duplicate/replayed event or changed source prefix")
        self._executing_event_index = self._index
        try:
            if self._started is None:
                self._start()
            self._phase = "prefix_integrity"
            _, observed = self._take_state()
            if observed != self._state_sha256:
                raise StateMutationError("Engine state changed outside this exact event prefix")
            row = dict(event_index=self._index, event_id=expected["event_id"], op=expected["op"],
                       event_sha256=_hash(expected), status="running",
                       persistent_before_sha256=observed, prefix_before_sha256=_hash(self._prefix()))
            self._events.append(row)
            if expected["op"] == "ingest":
                self._ingest(expected, row)
            else:
                self._ask(expected, row)
            self._state, self._state_sha256 = self._take_state()
            row["persistent_after_sha256"] = self._state_sha256
            row["prefix_after_sha256"] = _hash(self._prefix())
            row["status"] = "executed"
            self._phase = "event_executed"
            # A serialization failure is an execution failure, not a successful
            # event with a missing native trace. report() remains best-effort
            # only so that the interruption itself can still be preserved.
            self._native_result()
            self._emit()
            row["status"] = "completed"
            self._index += 1
            self._status = "completed" if self._index == len(self._case["events"]) else "running"
            self._phase = "completed" if self._status == "completed" else "event_completed"
            result = self.report()
            if result["native_serialization_error"]:
                raise RuntimeError("Completed event lacks native serialization")
            self._executing_event_index = None
            return result
        except BaseException as exc:
            self._interrupt(exc)

    def _ingest(self, event, row):
        env = envelope_only(event["source"])
        index = len(self._session_logs)
        session = attributed_session(env)
        row.update(source_id=source_id(env), source_sha256=_hash(env), session_index=index,
                   session_id=f"s_{index:03d}", session_time=env["observed_at"],
                   model_session=_copy(session), model_session_sha256=_hash(session))
        self._phase = "before_ingest"
        self._emit()
        started = self._clock()
        log = self._engine.process_session(session=_copy(session), session_index=index,
                                           session_time=env["observed_at"])
        log = _copy(log)
        log["elapsed_seconds"] = round(self._clock() - started, 3)
        self._session_logs.append(log)
        row["native_session_trace"] = log
        self._arrivals.append(dict(event_id=event["event_id"], session_index=index,
                                   session_id=f"s_{index:03d}", source_id=source_id(env), source=env,
                                   source_sha256=_hash(env)))

    def _ask(self, event, row):
        record = native_record_at(self._case, self._index)
        if record["haystack_session"] != [attributed_session(env) for env in self._prefix()]:
            raise StateMutationError("Visible source prefix differs from frozen event history")
        if set(record["probing_queries"]) != {event["event_id"]}:
            raise ValueError("Only the current checkpoint question may be visible")
        row.update(question=event["question"], raw_reader_input=_copy(record),
                   raw_reader_input_sha256=_hash(record),
                   visible_source_arrival_count=len(self._arrivals))
        before = row["persistent_before_sha256"]
        self._phase = "before_native_query"
        self._emit()
        _, immediately_before = self._take_state()
        if immediately_before != before:
            raise StateMutationError("Progress callback changed native persistent memory")
        native_before = self._native_result()
        native_before_hash = native_trace_state_hash(native_before)
        row["native_query_state_sha256"] = native_before_hash
        row["native_state_hash_scope"] = "official _build_sample_result profile/chunk/delta trace fields; may differ from raw to_dict state hash"
        row["memory_immutability_checks"] = [dict(phase="query_start", query=event["event_id"],
                                                   state_sha256=native_before_hash)]
        started = self._clock()
        log = self._engine.answer_query(query_label=event["event_id"], query_text=event["question"])
        log = _copy(log)
        log["elapsed_seconds"] = round(self._clock() - started, 3)
        self._query_logs[event["event_id"]] = log
        row["native_query_trace"] = log
        self._phase = "after_native_query"
        native_after = self._native_result()
        native_after_hash = native_trace_state_hash(native_after)
        row["memory_immutability_checks"].append(dict(phase="query_complete", query=event["event_id"],
                                                      state_sha256=native_after_hash))
        native_after["memory_immutability_checks"] = _copy(row["memory_immutability_checks"])
        row["query_time_trace"] = _copy(native_after)
        row["query_time_trace_sha256"] = _hash(native_after)
        _, after_native = self._take_state()
        row["persistent_after_native_query_sha256"] = after_native
        if before != after_native or native_before_hash != native_after_hash:
            raise StateMutationError("Native query mutated persistent memory")
        self._phase = "before_raw_query"
        self._emit()
        started = self._clock()
        row["raw_reader_result"] = _copy(self._raw_reader(_copy(record)))
        row["raw_reader_elapsed_seconds"] = round(self._clock() - started, 3)
        _, after_raw = self._take_state()
        row["persistent_after_raw_query_sha256"] = after_raw
        if before != after_raw:
            raise StateMutationError("Raw reader changed native persistent memory")

    def run(self):
        while self._status not in {"completed", "interrupted"}:
            self.advance()
        if self._status != "completed":
            raise TransferInterrupted(self.report())
        return self.report()


def run_case(case, *, engine, raw_reader, sample_index=0, progress_callback=None):
    return IncrementalTransferRun(case, engine=engine, raw_reader=raw_reader,
                                  sample_index=sample_index, progress_callback=progress_callback).run()
