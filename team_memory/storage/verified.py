"""Disposable process-local cache of verified immutable JSON objects.

The files remain authoritative. Every read enumerates names and stats each file,
so additions, deletion, replacement and edits invalidate cached entries. Disable
caching for a full byte audit; this is not authentication of a Git author.
"""
from copy import deepcopy
import json

from team_memory.storage.objects import digest


class VerifiedObjects:
    def __init__(self, root, *, cache=True):
        self.root = root
        self.enabled = cache
        self.entries = {}

    def load(self, kind):
        prior = self.entries.get(kind, {}) if self.enabled else {}
        current = {}
        objects = {}
        for path in sorted((self.root / kind).glob('*.json')):
            st = path.stat()
            fingerprint = (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns)
            cached = prior.get(path.name)
            if cached is not None and cached[0] == fingerprint:
                obj = cached[1]
            else:
                obj = json.loads(path.read_text(encoding='utf8'))
                if path.stem != digest(obj):
                    raise ValueError('Immutable object digest mismatch')
                if not isinstance(obj, dict):
                    raise ValueError('Immutable object must be a JSON object')
            current[path.name] = (fingerprint, obj)
            objects[path.stem] = obj
        if self.enabled:
            self.entries[kind] = current
        return deepcopy(objects)
