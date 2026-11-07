"""Supported JSONL boundary: attributed source QA + existing timeline review.

Share only immutable sources/proposals/votes. Processing receipts and indexes
belong to each client; a restart/pull does not replay a native memory writer.
Authentication and Git transport belong to the caller, not this module.
"""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
from threading import RLock

from .store import Store, digest
from .source_store import SourceStore, source_envelope
from . import timeline
from .timeline_cli import process_sources


VERSION = 'team-memory/v2'


class TeamMemoryService:
    def __init__(self, store, *, reader, generate, client_state=None):
        self.store = SourceStore(store.root if isinstance(store, Store) else store)
        if self.store.root.resolve() != reader.store.root.resolve():
            raise ValueError('Reader and review must use the same original source store')
        if client_state is None:
            root = self.store.root.resolve()
            while not root.exists():
                root = root.parent
            git = subprocess.run(['git', '-C', str(root), 'rev-parse', '--absolute-git-dir'],
                                 text=True, capture_output=True)
            client_state = (Path(git.stdout.strip())/'team-memory-clients'/digest(str(self.store.root.resolve()))
                            if git.returncode == 0 else self.store.root.parent/('.timeline-client-'+self.store.root.name))
        self.store.timeline_client_root = Path(client_state)
        reader.store = self.store
        # Derived indexes are private to each checkout, just like processing receipts.
        reader.index_dir = self.store.timeline_client_root / 'reference-index'
        self.reader, self.generate = reader, generate
        self.lock = RLock()

    def _response(self, operation, **fields):
        return dict(schema_version=VERSION, operation=operation,
                    implementation=dict(reader=type(self.reader).__name__, review='timeline-direct',
                                        sources='exact-input-text/v2'), **fields)

    def import_history(self, records):
        # Initial history is not a series of inferred approvals or retrospective
        # proposals. Subsequent reports/pulled records use ingest/sync instead.
        envs = [source_envelope(e) for e in records]
        with self.lock:
            if self.store.load('sources'):
                raise ValueError('import_history is only for an empty store; use ingest or sync')
            result = self.reader.import_history(envs)
            for sid in result['source_ids']:
                timeline.client_store(self.store).put('receipts', dict(source_id=sid, mode='direct',
                    history=[], proposals=[], errors=[], initial_history=True))
            return self._response('import_history', **result)

    def sync(self):
        with self.lock:
            rows = process_sources(self.store, self.generate, 'direct')
            errors = [dict(source_id=r['source_id'], **e) for r in timeline.receipts(self.store)
                      for e in r.get('errors', [])]
            return self._response('sync', status='partial' if errors else 'ok',
                processed=len(rows), review_errors=errors, proposals=timeline.proposals(self.store))

    def ingest(self, source):
        env = source_envelope(source)
        with self.lock:
            self.sync()
            row = timeline.ingest(self.store, env, self.generate, 'direct')
            return self._response('ingest', status='partial' if row['errors'] else 'ok',
                receipt=row, proposals=[p for p in timeline.proposals(self.store) if p['id'] in row['proposals']])

    def ask(self, question, temporal_scope='current'):
        if temporal_scope not in ('current', 'historical'):
            raise ValueError('temporal_scope must be current or historical')
        with self.lock:
            synced = self.sync()
            relations = timeline.proposals(self.store)
            with self.reader.lock:
                self.reader.review_relations = relations
                self.reader.temporal_scope = temporal_scope
                result = deepcopy(self.reader.ask(question))
            context = getattr(self.reader, 'active_review_context', None)
            result.update(temporal_scope=temporal_scope, review_context=context,
                          review_status=synced['status'], review_errors=synced['review_errors'])
            if context:
                from .review_context import assertion_reviews
                for answer in result.get('answers', []):
                    for evidence in answer.get('evidence', []):
                        evidence['assertion_reviews'] = assertion_reviews(evidence, context)
            # Never equate successful source accounting with semantic validation.
            if result.get('aqa_candidate_accepted'):
                result['answer_revision'] = dict(status='unverified_candidate',
                    original_raw=result['pre_aqa_raw'], original_answers=result['aqa_prior_answers'],
                    candidate_raw=result['aqa_candidate_raw'], acceptance_basis=result['aqa_acceptance_basis'])
                if result['status'] == 'ok':
                    result['status'] = 'partial'
                result.setdefault('warnings', []).append(
                    'Answer replacement has source coverage only; original answer retained, semantic preservation unverified')
            return self._response('ask', **result)

    def review(self, proposal_id, actor, choice):
        with self.lock:
            return self._response('review', status='ok',
                proposals=[timeline.review(self.store, proposal_id, actor, choice)])

    def handle(self, request):
        operation = request.get('operation', 'invalid') if isinstance(request, dict) else 'invalid'
        try:
            if operation == 'import_history': return self.import_history(request['records'])
            if operation == 'ingest': return self.ingest(request['source'])
            if operation in ('sync', 'rebuild'): return self.sync()
            if operation == 'ask': return self.ask(request['question'], request.get('temporal_scope', 'current'))
            if operation == 'review': return self.review(request['proposal_id'], request['actor'], request['choice'])
            if operation == 'view':
                return self._response('view', status='ok', **timeline.view(self.store))
            raise ValueError('Unknown operation')
        except (ValueError, TypeError, KeyError) as exc:
            return self._response(operation, status='invalid', error_type=type(exc).__name__, error=str(exc))
        except Exception as exc:
            return self._response(operation, status='error', error_type=type(exc).__name__, error=str(exc))


def main():
    import argparse
    from contextlib import redirect_stdout
    import sys
    from llama_index.core.llms import ChatMessage
    from .reference_attributed import AttributedQA, CitedSourceQA
    from .reference_qa import local_components
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reader', choices=['attributed', 'direct'], default='attributed')
    parser.add_argument('--store', required=True)
    parser.add_argument('--client-state')
    parser.add_argument('--model-path', required=True)
    parser.add_argument('--embedding-path', required=True)
    parser.add_argument('--api-base', required=True)
    args = parser.parse_args()
    output = sys.stdout
    with redirect_stdout(sys.stderr):
        parts = local_components(args.model_path, args.embedding_path, args.api_base)
        def generate(system, content):
            return parts['llm'].chat([ChatMessage(role='system', content=system),
                ChatMessage(role='user', content=content)]).message.content
        reader = (AttributedQA if args.reader == 'attributed' else CitedSourceQA)(args.store, **parts)
        service = TeamMemoryService(args.store, reader=reader, generate=generate, client_state=args.client_state)
        for line in sys.stdin:
            try:
                result = service.handle(json.loads(line))
            except (ValueError, TypeError) as exc:
                result = service._response('invalid', status='invalid', error=str(exc))
            print(json.dumps(result, ensure_ascii=False), file=output, flush=True)


if __name__ == '__main__':
    main()
