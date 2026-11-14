"""Assembly entrypoint. Model components and authenticated identity are injected."""
from pathlib import Path
from .records import RecordsAdapter
from .relations import RelationsAdapter
from .retrieval import RetrievalAdapter
from .answering import AnsweringAdapter
from .gateway import GatewayAdapter


def connect_v2(root,*,workspace_id,reader_factory,generate,cache_root=None):
    root=Path(root)
    cache=Path(cache_root) if cache_root else root.parent/('.module-cache-'+root.name)
    records=RecordsAdapter(root,workspace_id)
    return GatewayAdapter(workspace_id,records,RelationsAdapter(workspace_id,generate,snapshot_loader=records.snapshot,cache_root=cache/'relations'),
        RetrievalAdapter(workspace_id,reader_factory,cache/'retrieval',snapshot_loader=records.snapshot),
        AnsweringAdapter(workspace_id,reader_factory,cache/'answering',snapshot_loader=records.snapshot),journal_root=cache/'gateway')
