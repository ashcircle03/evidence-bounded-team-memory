"""Run in each member's checkout. Standard Git pull/push exchanges the store."""
import argparse
import json
import sys
from pathlib import Path

from .merge import replay, review, submit, source_disputes
from .qa import answer
from .reconsider import proposal_inbox, reconsider, review_proposal
from .store import Store, capture


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--store", default="team-records", help="Git-tracked directory (default: team-records)")
    cmd = p.add_subparsers(dest="command", required=True)
    add = cmd.add_parser("submit", help="add an agent's structured record; read JSON from file or stdin (-)")
    add.add_argument("json_file")
    for name in ("capture", "prepare", "draft", "ingest"):
        writer = cmd.add_parser(name, help="prepare input for a member AI or draft with a local HF model")
        writer.add_argument("json_file")
        if name in ("draft", "ingest"):
            writer.add_argument("--model", required=True, help="path to local model weights")
        if name == "ingest":
            writer.add_argument("--reconsider-goal", help="also assess old decisions in a separate review inbox")
    scope = cmd.add_parser("reconsider", help="read an incoming source and propose a review of an earlier decision")
    scope.add_argument("json_file")
    scope.add_argument("--goal", required=True, help="project goal known before reading the new report")
    scope.add_argument("--model", required=True)
    scope.add_argument("--limit", type=int, default=3)
    cmd.add_parser("inbox", help="recompute merge proposals after pulling records")
    vote = cmd.add_parser("review", help="record a local review on the exact proposal you inspected")
    for key in ("id", "proposal", "actor"):
        vote.add_argument(key)
    vote.add_argument("decision", choices=("approve", "reject"))
    query = cmd.add_parser("ask", help="read accepted and provisional evidence for a question")
    query.add_argument("question")
    query.add_argument("--issue")
    query.add_argument("--model", help="optional local HF reader for a short answer with a checked citation")
    cmd.add_parser("demo", help="replay the example in an isolated, temporary Git remote and two clones")
    args = p.parse_args()
    store = Store(args.store)
    if args.command in ("capture", "prepare", "draft", "submit", "ingest", "reconsider"):
        data = sys.stdin.read() if args.json_file == "-" else Path(args.json_file).read_text(encoding="utf8")
        envelope = json.loads(data)
        if args.command == "reconsider":
            from .choice import LocalChoice
            result = reconsider(store, envelope, args.goal, LocalChoice(args.model), args.limit)
        elif args.command == "submit":
            result = submit(store, envelope)
        elif args.command == "capture":
            result = {"source_id": capture(store, envelope)}
        elif args.command == "ingest":
            from .writer import ingest, local_generator
            capture(store, envelope)
            result = ingest(store, envelope, local_generator(args.model), reconsider_goal=args.reconsider_goal)
        else:
            from .writer import draft, local_generator, prepare
            result = prepare(store, envelope) if args.command == "prepare" else draft(store, envelope, local_generator(args.model))
    elif args.command == "review":
        handler = review_proposal if args.id in store.load("decision_assessments") else review
        result = handler(store, args.id, args.proposal, args.actor, args.decision)
    elif args.command == "inbox":
        result = list(replay(store).values()) + source_disputes(store.load("sources")) + proposal_inbox(store)
    elif args.command == "demo":
        from .demo import run
        result = run()
    else:
        result = answer(store, args.question, args.issue)
        if args.model and result["status"] in ("grounded_records", "source_only"):
            from .qa import read_answer
            from .writer import local_generator
            result = read_answer(result, args.question, local_generator(args.model))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError) as error:
        sys.exit(f"team_memory: {error}")
