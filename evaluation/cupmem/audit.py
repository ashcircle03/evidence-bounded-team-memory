"""Count every HTTP attempt, preserve raw bodies, and bound concurrent requests.

No credential, header, or environment is persisted. Uncertain requests retain
their token reservation. BudgetStop escapes upstream's ordinary retry loops.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import threading
import time


class BudgetStop(BaseException):
    pass


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


class Audit:
    def __init__(self, path, *, limits, secrets=()):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        # Never silently reuse an old run's accounting.
        self.file = self.path.open("x", encoding="utf-8")
        self.limits = limits
        self.secrets = tuple(s for s in secrets if s)
        self.lock = threading.RLock()
        self.context = {}
        self.attempts = 0
        self.used_input = self.used_output = 0
        self.reserved_input = self.reserved_output = 0
        self.pending = {}
        self.unknown = []
        self.censored = []

    def _write(self, row):
        text = canonical(row)
        for secret in self.secrets:
            text = text.replace(secret, "[REDACTED_CREDENTIAL]")
        self.file.write(text + "\n")
        self.file.flush()

    def set_context(self, **context):
        with self.lock:
            self.context = context

    def start(self, body, *, endpoint, output_reservation):
        if not isinstance(body.get("messages"), list):
            raise BudgetStop("Only audited chat requests are allowed")
        # Conservative UTF-8 byte reservation; provider usage replaces it on return.
        # Restrict the pilot to plain text messages, with no tools/images.
        if any(not isinstance(m.get("content"), str) for m in body["messages"]):
            raise BudgetStop("Unsupported non-text input")
        estimate = len(canonical(body["messages"]).encode()) + 64 * len(body["messages"]) + 256
        with self.lock:
            if self.attempts + 1 > self.limits["requests"]:
                raise BudgetStop("Request budget exhausted")
            if self.used_input + self.reserved_input + estimate > self.limits["input_tokens"]:
                raise BudgetStop("Input budget reservation exhausted")
            if self.used_output + self.reserved_output + output_reservation > self.limits["output_tokens"]:
                raise BudgetStop("Output budget reservation exhausted")
            self.attempts += 1
            rid = self.attempts
            self.pending[rid] = (estimate, output_reservation)
            self.reserved_input += estimate
            self.reserved_output += output_reservation
            self._write(dict(event="request", request_id=rid, time=time.time(),
                             endpoint=endpoint, context=deepcopy(self.context),
                             body=body, body_sha256=digest(body),
                             input_reservation=estimate, output_reservation=output_reservation))
            return rid

    def finish(self, rid, *, status, body, elapsed):
        with self.lock:
            usage = body.get("usage", {}) if isinstance(body, dict) else {}
            inp, out = usage.get("prompt_tokens"), usage.get("completion_tokens")
            known = all(type(n) is int and n >= 0 for n in (inp, out))
            self._write(dict(event="response", request_id=rid, time=time.time(),
                             status=status, elapsed_seconds=elapsed, body=body,
                             usage_known=known))
            if known:
                ri, ro = self.pending.pop(rid)
                self.reserved_input -= ri
                self.reserved_output -= ro
                self.used_input += inp
                self.used_output += out
                if inp > ri or out > ro:
                    raise BudgetStop("Provider usage exceeded conservative reservation")
            else:
                self.unknown.append(rid)
            if isinstance(body, dict) and any(c.get("finish_reason") == "length" for c in body.get("choices", [])):
                self.censored.append(rid)
                raise BudgetStop("Output reached pilot cap; not a valid uncensored reproduction")

    def failed(self, rid, exc):
        with self.lock:
            self.unknown.append(rid)
            self._write(dict(event="transport_error", request_id=rid,
                             error_type=type(exc).__name__, time=time.time()))

    def summary(self):
        with self.lock:
            return dict(requests=self.attempts, observed_input_tokens=self.used_input,
                        observed_output_tokens=self.used_output,
                        reserved_or_uncertain_input_tokens=self.reserved_input,
                        reserved_or_uncertain_output_tokens=self.reserved_output,
                        uncertain_request_ids=self.unknown, censored_request_ids=self.censored,
                        limits=self.limits)


def sdk_factory(audit, *, policy, transport=None):
    """Inject only the HTTP transport through the upstream-supported client factory.

    Keep OpenAI SDK retries AND CUPMem retries; all physical attempts are counted.
    Pilot output caps are explicit runtime deviations, never silent prompt edits.
    """
    import httpx
    from openai import OpenAI

    class AuditedTransport(httpx.BaseTransport):
        def __init__(self):
            self.inner = transport or httpx.HTTPTransport()

        def handle_request(self, request):
            endpoint = str(request.url)
            if request.method != "POST" or endpoint != policy["base_url"].rstrip("/") + "/chat/completions":
                raise BudgetStop("Request destination is outside authorized route")
            body = json.loads(request.read())
            model = body.get("model")
            if model not in policy["models"]:
                raise BudgetStop("Model outside approved configuration")
            model_policy = policy["models"][model]
            field = model_policy["output_limit_field"]
            bound = model_policy["output_limit"]
            existing = body.get(field, bound)
            body[field] = min(existing, bound)
            for other in ("max_tokens", "max_completion_tokens"):
                if other != field and other in body:
                    raise BudgetStop("Ambiguous output limit configuration")
            raw = json.dumps(body, ensure_ascii=False).encode()
            headers = dict(request.headers)
            headers["content-length"] = str(len(raw))
            forwarded = httpx.Request(request.method, request.url, headers=headers,
                                      content=raw, extensions=request.extensions)
            rid = audit.start(body, endpoint=endpoint, output_reservation=body[field])
            started = time.perf_counter()
            try:
                response = self.inner.handle_request(forwarded)
                raw_response = response.read()
            except Exception as exc:
                audit.failed(rid, exc)
                raise
            try:
                payload = json.loads(raw_response)
            except (ValueError, UnicodeDecodeError):
                payload = {"unparsed_body": raw_response.decode(errors="replace")}
            audit.finish(rid, status=response.status_code, body=payload,
                         elapsed=time.perf_counter() - started)
            return response

        def close(self):
            self.inner.close()

    def create(**kwargs):
        if kwargs.get("base_url", "").rstrip("/") != policy["base_url"].rstrip("/"):
            raise BudgetStop("Credential destination mismatch")
        return OpenAI(**kwargs, http_client=httpx.Client(transport=AuditedTransport(),
                      timeout=120.0), default_headers={"User-Agent": "curl/8.7.1"})

    return create
