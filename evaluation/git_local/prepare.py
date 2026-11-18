"""Measure explicit write-side preparation without an answer request."""
import json
from pathlib import Path
import sys
import os
from unittest.mock import patch


def main(packet, checkout, output):
    from team_memory.readers.retrieval import local_components
    from team_memory.readers.attribution import AttributedQA
    from team_memory.service import TeamMemoryService
    from team_memory.readers import indexing
    cfg=json.loads((packet/'config.json').read_text())
    assert os.environ.get('SLURM_JOB_ID')
    inputs=json.loads((packet/'inputs.json').read_text())
    parts=local_components(cfg['model_path'],cfg['embedding'],os.environ['PRACTICAL_MODEL_URL'])
    report=dict(pid=os.getpid(),document_embeddings=0,parsed_ids=[],rows=[])
    cls=type(parts['embed_model']);original=cls._get_text_embeddings;parse=indexing.document_nodes
    def embed(self,texts):
        report['document_embeddings']+=len(texts);return original(self,texts)
    def tracked(*args,**kwargs):
        nodes=parse(*args,**kwargs);report['parsed_ids'].extend(sorted({n.ref_doc_id for n in nodes}));return nodes
    with patch.object(cls,'_get_text_embeddings',embed),patch.object(indexing,'document_nodes',tracked):
        for case in inputs['cases']:
            path=checkout/'records'/case['id'];reader=AttributedQA(path,**parts)
            TeamMemoryService(path,reader=reader,generate=None)
            report['rows'].append(dict(case_id=case['id'],result=reader.prepare_index()))
    output.write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':main(*map(Path,sys.argv[1:]))
