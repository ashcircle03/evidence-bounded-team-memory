"""Exact-text source contract for new inputs; historical hashes stay readable.

The old source_envelope is frozen by historical reconstruction manifests.
Reuse its validation, restoring the input text before hashing new v2 sources.
"""
from team_memory.storage.objects import Store, source_envelope as legacy_envelope


def source_envelope(data):
    env = legacy_envelope(data)
    env['source']['text'] = data['source']['text']
    return env


class SourceStore(Store):
    source_envelope = staticmethod(source_envelope)

    def capture_source(self, envelope):
        return self.put('sources', source_envelope(envelope))
