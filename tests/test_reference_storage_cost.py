"""Check timing instrumentation and independent interventions without a GPU."""
from pathlib import Path
import pytest
from tests.test_reference_index_lifecycle import env,documents
from team_memory.readers.retrieval import ReferenceQA
from evaluation.storage_cost.instrumentation import Timings,instrument,intervention


@pytest.mark.parametrize('arm',['previous','batch_only','cache_only','combined'])
def test_cold_ablation_counts_and_timer_accounting(env,arm):
    t=env;reader=ReferenceQA(Path(t.temp.name)/arm,profile='team',**t.options)
    reader.import_history(documents(t),prepare=False);sources=reader.store.load('sources');meter=Timings()
    with intervention(arm,reader,sources) as module,instrument(module,meter),meter.measure('total'):
        result=module.prepare(reader,sources)
    assert result['prepared_documents']==2 and len(t.embed._texts)==2
    assert meter.rows['split']['calls']==2
    assert meter.rows['cache_transaction']['calls']==(2 if arm in ['previous','batch_only'] else 1)
    assert meter.rows['embedding_pipeline']['calls']==(2 if arm in ['previous','cache_only'] else 1)
    assert abs(sum(v['exclusive_seconds'] for v in meter.rows.values())-meter.rows['total']['seconds'])<0.001
    before=len(t.embed._texts);assert reader.ask('What value?')['status']=='ok'
    assert len(t.embed._texts)==before
