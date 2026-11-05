"""Recover the 20 legacy QA corpora without running a model or selecting gold text.

This is an input/reconstruction artifact, not a new CUPMem result. Historical
reader outputs are scoring-only. ``model_payload`` is the only model boundary;
it returns full original sources and the question, never the scoring section.

The old readers treated history as a source collection. Both its original
iteration order and a chronological adapter order are recorded. A future paired
runner must explicitly select one order for BOTH arms. Nothing is shortened to
fit an inference budget.
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

from evaluation.decision_records.build import ROOT, WORK, GIT, read
from evaluation.pair_selection.qa import EVER, FINAL, packets
from evaluation.pair_selection.qa_replay import historical
from evaluation.revision.build_final import build as git_cases
from evaluation.revision.regression import build as regression
from evaluation.team_pilot.pilot import (
    DEVELOPMENT, EVER as EVER_REV, UPSTREAM as PEP_REV,
    dev_sources, pep_sources,
)
from team_memory.store import digest as source_id

HERE = Path(__file__).resolve().parent
LEGACY = ROOT / "results/timeline/legacy-qa.json"
PEPS = WORK / ".work/peps-external.git"
STORE = WORK / ".work/speaker-run/paired-snapshot"


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def fingerprint(value):
    return sha256(canonical(value)).hexdigest()


def model_payload(data, case_id, *, order):
    """Return source-only input; callers must explicitly choose a declared order."""
    if order not in ("historical", "chronological"):
        raise ValueError("order must be historical or chronological")
    case = next(c for c in data["cases"] if c["id"] == case_id)
    history = data["histories"][case["history_id"]][order + "_source_ids"]
    records = []
    for sid in history:
        env = data["documents"][sid]
        # Rebuild the boundary from an allowlist, including unmodified attribution.
        records.append(dict(source_id=sid, owner=env["owner"], observed_at=env["observed_at"],
                            source={k: env["source"][k] for k in ("text", "location", "speaker")}))
    return dict(history=records, question=case["question"], as_of=case["as_of"])


def _history_metrics(ids, documents):
    return dict(document_count=len(ids),
                source_text_utf8_bytes=sum(len(documents[s]["source"]["text"].encode()) for s in ids),
                attributed_history_utf8_bytes=len(canonical([
                    dict(source_id=s, **documents[s]) for s in ids])))


def _prefix_nodes(histories, order):
    # Count source-prefix states; only byte-identical prefixes may be reused.
    prefixes = set()
    for history in histories.values():
        prefix = []
        for sid in history[order + "_source_ids"]:
            prefix.append(sid)
            prefixes.add(tuple(prefix))
    return len(prefixes)


def _source_files():
    paths = [LEGACY, ROOT / "evaluation/revision/final-key.json",
             ROOT / "evaluation/revision/development/ever-questions.json",
             ROOT / "evaluation/team_pilot/cases.json",
             ROOT / "results/revision/evermem-external.json"]
    paths += [ROOT / x for x in [
        "evaluation/revision/build_final.py", "evaluation/revision/final_cases.py",
        "evaluation/revision/regression.py", "evaluation/revision/run.py",
        "evaluation/team_pilot/pilot.py", "evaluation/pair_selection/qa.py",
        "evaluation/pair_selection/qa_replay.py", "team_memory/store.py",
    ]]
    for version, job in [("revision-final-v1", "119273"), ("revision-dev-v3", "119272"),
                         ("pull-pilot-v1", "119269")]:
        paths.extend([WORK / "campaigns/speakermem-dev/source" / version / "packets.json",
                      WORK / "campaigns/speakermem-dev/results" / ("sm-" + job + ".json")])
    return {str(p.relative_to(WORK)): sha256(p.read_bytes()).hexdigest() for p in paths}


def reconstruct(*, verify_archived=True):
    """Recover full source corpora and frozen keys; never invoke a generator."""
    saved = read(LEGACY)
    finals, rebuilt_key = git_cases(GIT)
    frozen_key = read(ROOT / "evaluation/revision/final-key.json")
    old = regression(PEPS, STORE)
    ever_docs = {sid: env for sid, (env, _) in dev_sources(STORE).items()}
    ever_questions = {q["id"]: q["question"] for q in read(
        ROOT / "evaluation/revision/development/ever-questions.json")["answers"]}
    pep_docs = {source_id(env): env for env in pep_sources(PEPS).values()}
    book = {q["pep"]: q for q in read(ROOT / "evaluation/team_pilot/cases.json")["qa"]}
    external = {q["id"]: q for q in read(ROOT / "results/revision/evermem-external.json")["items"]}
    expected_names = FINAL + EVER + ["pep-680/clean/candidate"]
    if set(saved["rows"]) != set(expected_names) or len(expected_names) != 20:
        raise ValueError("legacy selection changed")

    data = dict(schema_version=1,
                label="legacy QA source reconstruction; no new model inference",
                documents={}, histories={}, cases=[], evaluation_only={})
    history_lookup = {}

    def add_case(name, question, ids, docs, as_of, sides, corpus, source_key):
        previous = saved["rows"][name]
        if question != previous["question"] or not previous["identical"]:
            raise ValueError("legacy question/output mismatch: " + name)
        for sid in ids:
            env = docs[sid]
            if source_id(env) != sid:
                raise ValueError("source ID mismatch")
            if sid in data["documents"] and data["documents"][sid] != env:
                raise ValueError("source collision")
            data["documents"][sid] = deepcopy(env)
        key = tuple(ids)
        if key not in history_lookup:
            hid = fingerprint([dict(source_id=s, **docs[s]) for s in ids])
            history_lookup[key] = hid
            chronological = sorted(range(len(ids)), key=lambda i: (docs[ids[i]]["observed_at"], i))
            ordered = [ids[i] for i in chronological]
            data["histories"][hid] = dict(
                historical_source_ids=list(ids), chronological_source_ids=ordered,
                order_changed=ordered != list(ids),
                historical_sha256=hid,
                chronological_sha256=fingerprint([dict(source_id=s, **docs[s]) for s in ordered]),
                **_history_metrics(ids, docs))
        hid = history_lookup[key]
        data["cases"].append(dict(id=name, question=question, as_of=as_of, history_id=hid))
        # Historical accepted outputs are witnesses, not source text or fresh gold.
        accepted = previous["before"].get("answers", [previous["before"]])
        witnesses = []
        for item in accepted:
            sid = item.get("source_id", item.get("id"))
            env = docs[sid]
            if sid not in ids or env["source"]["location"] != item["location"]:
                raise ValueError("legacy citation is outside the original corpus")
            quote = item["quote"]
            start = item.get("start", env["source"]["text"].find(quote))
            end = item.get("end", start + len(quote))
            if start < 0 or env["source"]["text"][start:end] != quote:
                raise ValueError("legacy citation is not an exact original span")
            witnesses.append(dict(source_id=sid, location=item["location"], start=start, end=end,
                                  quote=quote, historical_answer=item["answer"]))
        for side in sides:
            locations = side["locations"] if "locations" in side else [side["location"]]
            matching = [s for s in ids if docs[s]["source"]["location"] in locations]
            if not matching:
                raise ValueError("frozen gold source missing")
            if not any(alias.casefold() in (docs[s]["source"]["text"] + "\n" + docs[s]["source"]["speaker"]).casefold()
                       for s in matching for alias in side["aliases"]):
                raise ValueError("frozen alias not grounded")
        data["evaluation_only"][name] = dict(
            corpus=corpus, key_source=source_key, expected_sides=sides,
            historical_state=previous["before"]["status"],
            historical_output_sha256=fingerprint(previous["before"]),
            historical_citations=witnesses)

    for name in FINAL:
        cid, _ = name.split("/")
        dataset = old if cid.startswith("old-") else finals
        case = next(c for c in dataset["cases"] if c["id"] == cid)
        if cid.startswith("old-"):
            number = int(cid.split("-")[2])
            q = book[number]
            location = f"https://github.com/python/peps/blob/{PEP_REV}/peps/pep-{number:04}.rst"
            sides = [dict(location=location, aliases=q["answers"], condition=None)]
            if cid.endswith("conflict"):
                sides.append(dict(location="casebook://messages/" + source_id(q["counter"]),
                                  aliases=q["other"], condition=None))
            corpus = "PEP public source with controlled counterstatement" if len(sides) > 1 else "PEP public source"
            key_source = "evaluation/team_pilot/cases.json"
        else:
            if rebuilt_key[cid] != frozen_key[cid]:
                raise ValueError("Git key reconstruction changed")
            sides = frozen_key[cid]["sides"]
            corpus = frozen_key[cid]["origin"]
            key_source = "evaluation/revision/final-key.json"
        add_case(name, case["question"], case["history"], dataset["documents"], case["as_of"],
                 sides, corpus, key_source)

    for name in EVER:
        cid = name.split("/")[0]
        original = external[cid]
        aliases = next((a for n, _, _, a in DEVELOPMENT if n == cid), [original["reference"]])
        # Keep the original external reference too (business/working-day wording).
        aliases = list(dict.fromkeys([*aliases, original["reference"]]))
        locations = [f"EverMemBench-Dynamic@{EVER_REV}/01/" + x.replace("|", "/")
                     for x in original["retrieval_reference_hits"]]
        # Native retrieval references include background context. They are an
        # evidence group for ONE answer, not separate required answers/citations.
        sides = [dict(locations=locations, aliases=aliases, condition=None,
                      evidence_group_semantics="candidate native references; membership alone does not prove quote entailment")]
        add_case(name, ever_questions[cid], list(ever_docs), ever_docs, "2025-02-01T00:00:00Z",
                 sides, "natural EverMemBench-Dynamic QA",
                 "results/revision/evermem-external.json:reference/retrieval_reference_hits")

    q = book[680]
    add_case("pep-680/clean/candidate", q["question"], list(pep_docs), pep_docs, "2026-11-03T12:00:00Z",
             [dict(location=f"https://github.com/python/peps/blob/{PEP_REV}/peps/pep-0680.rst",
                   aliases=q["answers"], condition=None)], "PEP public source", "evaluation/team_pilot/cases.json")

    _, refs = packets()
    selected_refs = {k: v for k, v in refs.items() if v["group"] in expected_names}
    validation = dict(status="not_run", inference_calls=0)
    if verify_archived:
        rows = historical(refs, {k: v["original"] for k, v in refs.items()})
        if rows != saved["rows"]:
            raise ValueError("archived packet/reader replay differs from saved 20-case result")
        validation = dict(status="verified", historical_rows_identical=20,
                          actual_reader_call_hashes_checked=len(selected_refs), inference_calls=0,
                          meaning="source/replay compatibility only; not new-actor QA preservation")
    data["provenance"] = dict(
        selection="exact 20 rows of results/timeline/legacy-qa.json, no new selection",
        historical_job_id=str(saved["job_id"]), archived_replay=validation,
        source_file_sha256=_source_files(),
        archived_reader_inputs={k: v["original"]["sha256"] for k, v in selected_refs.items()},
        source_scope={"Git": "all source envelopes in the original case history at pinned Git revision",
                      "PEP": "all original 16 PEPs; first 140 lines each at pinned revision with the original source_envelope outer-whitespace normalization",
                      "EverMemBench": "all original 528 January topic-01 records; no gold filtering"},
        canonical_order="historical",
        order_policy="canonical paired regression retains original source collection order; chronological order is a separate noncanonical adapter variant, never implicitly selected",
        timestamp_semantics={
            "Git_manual": "observed_at is the pinned Git snapshot commit time for every extracted section, not each section's authorship time",
            "PEP": "observed_at is the original 2026-11-03 corpus fixture time, not the PEP's historical publication date",
            "EverMemBench": "observed_at is the source event timestamp; original Store iteration was source-ID order, not event chronology",
            "as_of": "original query cutoff/context timestamp, not a new observed event",
            "limitation": "legacy corpora are source collections; do not claim native STALE chronological-session semantics"},
        model_boundary="use model_payload(..., order=...) only; evaluation_only/provenance/case IDs are not model input")
    for case in data["cases"]:
        case["model_payload_sha256"] = {
            order: fingerprint(model_payload(data, case["id"], order=order))
            for order in ("historical", "chronological")}
        case["model_payload_utf8_bytes"] = {
            order: len(canonical(model_payload(data, case["id"], order=order)))
            for order in ("historical", "chronological")}
    counts = Counter(c["history_id"] for c in data["cases"])
    data["sizing"] = dict(
        cases=len(data["cases"]), unique_documents=len(data["documents"]), unique_histories=len(counts),
        summed_case_documents=sum(data["histories"][c["history_id"]]["document_count"] for c in data["cases"]),
        unique_history_documents=sum(h["document_count"] for h in data["histories"].values()),
        unique_source_prefix_states={o: _prefix_nodes(data["histories"], o) for o in ("historical", "chronological")},
        history_case_counts=dict(counts),
        unique_source_text_utf8_bytes=sum(len(e["source"]["text"].encode()) for e in data["documents"].values()),
        calls_estimate=None,
        caveat="document/prefix counts are not API request counts; CUPMem makes multiple requests per session; reuse requires exact input/config hashes and query-memory immutability")
    return data


def write_artifacts(output=HERE / "legacy-inputs.json", manifest=HERE / "legacy-inputs-manifest.json"):
    data = reconstruct()
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    report = dict(schema_version=1, status="inputs_reconstructed_no_new_inference",
                  artifact=output.name, sha256=sha256(output.read_bytes()).hexdigest(),
                  builder_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                  sizing=data["sizing"], archived_replay=data["provenance"]["archived_replay"],
                  source_file_sha256=data["provenance"]["source_file_sha256"])
    manifest.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=HERE / "legacy-inputs.json")
    parser.add_argument("--manifest", type=Path, default=HERE / "legacy-inputs-manifest.json")
    args = parser.parse_args()
    print(json.dumps(write_artifacts(args.output, args.manifest), indent=2))
