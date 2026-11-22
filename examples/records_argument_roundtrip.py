"""Run from the checkout with python -m examples.records_argument_roundtrip."""
from tempfile import TemporaryDirectory

from team_memory.adapters.base import request
from team_memory.adapters.records import RecordsAdapter
from team_memory.contracts.ports import CallContext
from team_memory.records.arguments import with_arguments


def demo(root):
    source = dict(id="minutes-1", owner="team", speaker="secretary",
                  observed_at="2026-11-19T00:00:00Z", location="minutes.md#L4",
                  text="Petr will send questions.")
    # Example extractor output; appending the unannotated source works too.
    source = with_arguments(source, [
        dict(predicate=[10, 14], qas=[
            dict(question="who will send something ?", answers=["Petr"]),
            dict(question="what will someone send ?", answers=["questions"]),
        ])
    ], producer="example")
    ctx = CallContext("demo", "team", frozenset({"records:write", "records:read"}))
    def call(operation, payload):
        port = RecordsAdapter(root, "demo")
        reply = port.handle(request(operation, payload, workspace_id="demo", request_id=operation),
                            context=ctx)
        if reply["status"] != "ok":
            raise RuntimeError(reply["errors"])
        return reply["data"]
    call("record.append", dict(source=source, expected_revision=0, idempotency_key="minutes-1"))
    stored = call("snapshot.get", dict(snapshot_id=None))["sources"][0]
    return [(x["predicate"]["quote"], x["role_question"], x["argument"]["quote"], stored["location"])
            for x in stored["record_arguments"]["links"]]


if __name__ == "__main__":
    with TemporaryDirectory() as root:
        for row in demo(root):
            print(*row, sep=" | ")
