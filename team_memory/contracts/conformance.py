"""Run a replaceable port against a shared scenario, without model dependencies.

An adapter factory returns Subject(port, observe_state). The observer reads the
authoritative state (excluding logs/caches), so read-only tests detect writes.
"""

import argparse
from copy import deepcopy
from dataclasses import dataclass
import importlib
import json
from pathlib import Path
from typing import Callable, Any

from .ports import CallContext, Port
from .validation import ContractError, require, validate_exchange


@dataclass
class Subject:
    port: Port
    observe_state: Callable[[], Any]


def pointer(value, path):
    """RFC 6901 JSON pointer, including escaped slash/tilde keys."""
    if path == "":
        return value
    require(path.startswith("/"), "assertion path must be a JSON pointer")
    for part in path[1:].split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def run_case(case, subject):
    before_state = deepcopy(subject.observe_state())
    context = CallContext(**{**case["context"],
                             "capabilities": frozenset(case["context"]["capabilities"])})
    request = deepcopy(case["request"])
    response = subject.port.handle(request, context=context)
    require(request == case["request"], "port mutated its caller's input")
    validate_exchange(request, response)
    for assertion in case["expect"]:
        actual = pointer(response, assertion["path"])
        if "equals" in assertion:
            require(actual == assertion["equals"], f"unexpected {assertion['path']}")
        elif "contains" in assertion:
            require(assertion["contains"] in actual, f"missing value at {assertion['path']}")
        else:
            raise ContractError("unknown fixture assertion")
    if case["state_unchanged"]:
        require(subject.observe_state() == before_state, "port changed authoritative state")
    elif response['module'] == 'records' and response['status'] == 'ok' and 'snapshot' in response['data']:
        require(subject.observe_state() == response['data']['snapshot'], "receipt was not committed")
    elif request['operation'] == 'gateway.ingest' and response['status'] in ('ok','partial'):
        current = subject.observe_state()
        require(current['revision'] >= response['data']['receipt']['snapshot']['revision'],
                "ingest receipt is newer than committed state")
        source = request['payload']['source']
        require(source in current['sources'], "ingest partial lost committed source")
    if case.get("retry_identically"):
        committed = deepcopy(subject.observe_state())
        retry_request = deepcopy(case['request'])
        retried = subject.port.handle(retry_request, context=context)
        require(retry_request == case['request'], "retry mutated input")
        validate_exchange(case["request"], retried)
        require(retried['status'] == response['status'], "retry changed status")
        first = deepcopy(response['data'])
        first['replayed'] = True
        require(retried['data'] == first, "retry did not return the original receipt")
        require(subject.observe_state() == committed, "retry applied a second mutation")
    return response


class FixturePort:
    """Canned dependency double. It is NOT a records implementation or a model."""

    def __init__(self, case):
        self.case = deepcopy(case)
        self.calls = 0
        self.state = deepcopy(case['setup']['snapshot'])

    def handle(self, request, *, context):
        require(request == self.case['request'], "unexpected request to fixture double")
        result = deepcopy(self.case['response'])
        if self.calls and self.case.get('retry_identically'):
            result['data']['replayed'] = True
        self.calls += 1
        if result['status'] == 'ok' and result['module'] == 'records' and 'snapshot' in result['data']:
            self.state = deepcopy(result['data']['snapshot'])
        if request['operation'] == 'gateway.ingest' and result['status'] in ('ok','partial'):
            self.state = deepcopy(result['data']['receipt']['snapshot'])
        return result


def fixture_factory(case):
    """Validate fixture consistency only. Never report this as an adapter pass."""
    port = FixturePort(case)
    return Subject(port, lambda: deepcopy(port.state))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixtures", type=Path)
    parser.add_argument("--module", choices=("records", "relations", "retrieval", "answering", "gateway"))
    parser.add_argument("--factory", help="module:function; receives one complete scenario")
    args = parser.parse_args()
    cases = json.loads(args.fixtures.read_text(encoding="utf-8"))
    cases = [c for c in cases if args.module is None or c['response']['module'] == args.module]
    if not cases:
        parser.error("no scenarios selected")
    factory = fixture_factory
    if args.factory:
        module, name = args.factory.rsplit(":", 1)
        factory = getattr(importlib.import_module(module), name)
    failures = []
    for case in cases:
        try:
            run_case(case, factory(deepcopy(case)))
        except Exception as exc:
            # Do not print source text, credentials, or arbitrary adapter outputs.
            failures.append({"case": case['name'], "error_type": type(exc).__name__})
    print(json.dumps({"mode": "adapter" if args.factory else "fixture-only",
                      "cases": len(cases), "passed": len(cases) - len(failures),
                      "failures": failures}, ensure_ascii=False))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
