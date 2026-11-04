"""Git tracks each incoming record and review as a separate immutable JSON file."""
import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def digest(value):
    return hashlib.sha256(encoded(value)).hexdigest()[:24]


def nonempty(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be nonempty text")
    return value.strip()


def timestamp(value):
    date = datetime.fromisoformat(nonempty(value, "observed_at").replace("Z", "+00:00"))
    if date.tzinfo is None:
        raise ValueError("observed_at needs an explicit UTC offset")
    return date.astimezone(timezone.utc).isoformat(timespec="microseconds")


def record(data):
    """Validate the contract used by a member's agent. Keep its interpretation separate from the quote."""
    item = {key: nonempty(data.get(key), key) for key in ("owner", "issue", "value", "quote")}
    source = data["source"]
    item["source"] = {key: nonempty(source.get(key), key) for key in ("location", "speaker", "text")}
    if item["quote"] not in item["source"]["text"]:
        raise ValueError("quote must occur verbatim in source.text")
    scope = data["scope"]
    if not isinstance(scope, dict):
        raise ValueError("scope must be an object; use {} for unknown scope")
    item["scope"] = {nonempty(k, "condition"): nonempty(v, "condition value") for k, v in scope.items()}
    item["observed_at"] = timestamp(data["observed_at"])
    if data.get("reason_quote"):
        reason = nonempty(data["reason_quote"], "reason_quote")
        if reason not in item["source"]["text"]:
            raise ValueError("reason_quote must occur verbatim in source.text")
        item["reason_quote"] = reason
    if data.get("corrects"):
        item["corrects"] = nonempty(data["corrects"], "corrects")
    return item


class Store:
    def __init__(self, root):
        self.root = Path(root)

    def load(self, kind):
        items = {}
        for path in sorted((self.root / kind).glob("*.json")):
            obj = json.loads(path.read_text(encoding="utf8"))
            if path.stem != digest(obj):
                raise ValueError(f"changed immutable object: {path}")
            items[path.stem] = obj
        return items

    def put(self, kind, obj):
        directory = self.root / kind
        directory.mkdir(parents=True, exist_ok=True)
        key = digest(obj)
        path = directory / (key + ".json")
        with tempfile.NamedTemporaryFile(dir=directory, delete=False) as tmp:
            try:
                tmp.write(encoded(obj))
                tmp.flush()
                os.fsync(tmp.fileno())
                try:
                    os.link(tmp.name, path)
                except FileExistsError:
                    if path.read_bytes() != encoded(obj):
                        raise ValueError(f"changed immutable object: {path}")
            finally:
                os.unlink(tmp.name)
        return key


def source_envelope(data):
    src = data["source"]
    return {"owner": nonempty(data["owner"], "owner"), "observed_at": timestamp(data["observed_at"]),
            "source": {k: nonempty(src.get(k), k) for k in ("speaker", "location", "text")}}


def capture(store, envelope):
    return store.put("sources", source_envelope(envelope))
