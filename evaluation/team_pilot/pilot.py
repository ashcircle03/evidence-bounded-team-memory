"""Build frozen prompts or replay the recorded generations through the production APIs."""

import argparse
from datetime import datetime, timezone
import hashlib
import html
import json
from pathlib import Path
import subprocess

from team_memory.evidence import ask, assess
from team_memory.store import Store, digest, source_envelope
from team_memory.sync import DEFAULT_GOAL

HERE = Path(__file__).resolve().parent
UPSTREAM = "16991a9ce7b223b38f0b473f51a8a7d94c8b9249"
EVER = "a6b210a32248e841967b7b64a64281d2ff3f669d"
DEVELOPMENT = [
    (
        "F_SH_Top01_013",
        "After conducting a technical assessment of the data quality of the production line energy management system, what is the preliminary estimated number of workdays required for data cleansing and initial verification in the report?",
        "2025-01-14/Group 1/5",
        ["at least 10 working days"],
    ),
    (
        "F_SH_Top01_033",
        "When reviewing the first draft of the user interview outline for the carbon emissions management platform, who suggested adding questions about customizable reporting dimensions to address the needs of managers and auditors?",
        "2025-01-24/Group 1/5",
        ["Lizhen Zhou"],
    ),
]
TOPICS = [
    498,
    515,
    519,
    518,
    552,
    553,
    572,
    597,
    615,
    618,
    654,
    668,
    669,
    680,
    691,
    701,
]
AUTHORS = "Ari Bea Cal Dee Emi Fay Gus Hal Iya Jo Kai Liv Moe Noa Ola Paz Qin Ren Sol Tai".split()


def envelope(text, location, speaker, at="2026-11-03T12:00:00Z"):
    return source_envelope(
        dict(
            owner=speaker,
            observed_at=at,
            source=dict(text=text, location=location, speaker=speaker),
        )
    )


def bundle(envs):
    return {digest(env): (env, "source_only") for env in envs}


def pep_sources(repo):
    history = {}
    for n in TOPICS:
        path = f"peps/pep-{n:04}.rst"
        raw = subprocess.check_output(
            ["git", "--git-dir", str(repo), "show", UPSTREAM + ":" + path]
        ).decode()
        env = envelope(
            "\n".join(raw.splitlines()[:140]),
            f"https://github.com/python/peps/blob/{UPSTREAM}/{path}",
            f"PEP {n} contributors",
        )
        history[n] = env
    return history


def dev_sources(path):
    if path.is_dir():
        return {
            sid: (env, "source_only")
            for sid, env in Store(path).load("sources").items()
        }
    envs = []
    for day in json.loads(path.read_text()):
        if day["date"] > "2025-01-31":
            continue
        for group, messages in day["dialogues"].items():
            for m in messages:
                stamp = m["time"].strip()
                if ":" in stamp and len(stamp) <= 15 and "-" not in stamp:
                    stamp = day["date"] + "T" + stamp
                dt = datetime.fromisoformat(stamp)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                loc = f"EverMemBench-Dynamic@{EVER}/01/{day['date']}/{group}/{m['message_index']}"
                envs.append(
                    envelope(
                        html.unescape(m["dialogue"]), loc, m["speaker"], dt.isoformat()
                    )
                )
    return bundle(envs)


def call_hash(system, content):
    return hashlib.sha256((system + "\n" + content).encode()).hexdigest()


def construct(repo, dev, saved=None):
    cases = json.loads((HERE / "cases.json").read_text())
    docs = pep_sources(repo)
    earlier = [
        envelope(
            c["previous"], f"casebook://decisions/{digest(c['previous'])}", AUTHORS[i]
        )
        for i, c in enumerate(cases["review"])
    ]
    packets = []
    outcomes = []

    def run(case, phase, arm, function, args, key):
        name = f"{case}/{phase}/{arm}"
        called = []

        def invoke(system, content):
            h = call_hash(system, content)
            packets.append(dict(id=name, system=system, content=content, sha256=h))
            called.append(h)
            if saved is None:
                return "NONE"
            row = saved[name]
            if row["sha256"] != h:
                raise ValueError(f"Changed input for {name}")
            return row["raw"]

        result = function(*args, invoke, arm)
        if len(called) != 1:
            raise ValueError(f"expected one call: {name}")
        outcomes.append(
            dict(id=name, case=case, phase=phase, arm=arm, key=key, result=result)
        )

    for index, c in enumerate(cases["qa"]):
        n = c["pep"]
        target = docs[n]["source"]["location"]
        expected = docs[n]["source"]["text"].splitlines()[c["line"] - 1]
        if not any(a.casefold() in expected.casefold() for a in c["answers"]):
            raise ValueError(f"gold line lacks answer in {n}")
        counter = envelope(
            c["counter"], f"casebook://messages/{digest(c['counter'])}", AUTHORS[index]
        )
        noise = [
            envelope(
                f"The calendar reserves {day} as the only meeting day for the PEP {n} integration review.",
                f"casebook://calendar/{n}/{j}",
                AUTHORS[index + j],
            )
            for j, day in enumerate(("Monday", "Thursday"))
        ]
        for phase, extra in (
            ("clean", []),
            ("unrelated", noise),
            ("conflict", [counter]),
        ):
            sources = bundle([*docs.values(), *extra])
            key = [dict(location=target, answers=c["answers"], line=c["line"])]
            if phase == "conflict":
                key.append(
                    dict(location=counter["source"]["location"], answers=c["other"])
                )
            for arm in ("simple", "candidate"):
                run(f"pep-{n}", phase, arm, ask, (sources, c["question"]), key)
    for i, c in enumerate(cases["review"]):
        incoming = envelope(
            c["incoming"],
            f"casebook://observations/{digest(c['incoming'])}",
            AUTHORS[(i + 7) % len(AUTHORS)],
            "2026-11-04T12:00:00Z",
        )
        key = dict(
            location=earlier[i]["source"]["location"],
            actions=c["actions"],
            old_cue=c["old_cue"],
            new_cue=c["new_cue"],
            new_location=incoming["source"]["location"],
        )
        for arm in ("simple", "candidate"):
            run(
                f"review-{i + 1:02}",
                "review",
                arm,
                assess,
                (bundle(earlier), digest(incoming), incoming, DEFAULT_GOAL),
                key,
            )
    sources = dev_sources(dev)
    if len(sources) != 528:
        raise ValueError("expected 528 original January topic-01 records")
    for case, q, loc, aliases in DEVELOPMENT:
        key = [dict(location=f"EverMemBench-Dynamic@{EVER}/01/{loc}", answers=aliases)]
        for arm in ("simple", "candidate"):
            run(case, "development", arm, ask, (sources, q), key)
    if len(packets) != 104 or len({r["id"] for r in packets}) != 104:
        raise ValueError("expected 104 distinct calls")
    if saved is not None and set(saved) != {r["id"] for r in packets}:
        raise ValueError("recorded run and rebuilt inputs differ")
    return packets, outcomes


def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("command", choices=("prepare", "replay"))
    cli.add_argument("peps", type=Path)
    cli.add_argument("ever_topic_or_store", type=Path)
    cli.add_argument("output", type=Path)
    cli.add_argument("--recording", type=Path)
    a = cli.parse_args()
    if (a.command == "replay") != bool(a.recording):
        cli.error("replay requires --recording")
    saved = None
    if a.recording:
        logged = json.loads(a.recording.read_text())["calls"]
        saved = {r["id"]: r for r in logged}
        if len(saved) != len(logged):
            raise ValueError("duplicate call")
    packets, outcomes = construct(a.peps, a.ever_topic_or_store, saved)
    write(a.output, packets if saved is None else outcomes)
