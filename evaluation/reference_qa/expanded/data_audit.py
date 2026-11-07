"""Read only pinned development data on an allocated compute node."""
import csv,hashlib,json,os,socket
from pathlib import Path
assert os.environ['SLURMD_NODENAME'] and os.environ['CONDA_PREFIX']
root=Path('/local_datasets/pjw031003/capstone-shared-knowledge/datasets-v1')
result={'job_id':os.environ['SLURM_JOB_ID'],'status':'complete','node':socket.gethostname(),'root':str(root),'ever':{}}
for topic in ['01','02']:
 q=json.loads((root/'EverMemBench-Dynamic'/topic/f'qa_{topic}.json').read_text());d=json.loads((root/'EverMemBench-Dynamic'/topic/'dialogue.json').read_text())
 groups={}
 for row in q:
  typ='_'.join(row['id'].split('_')[:2]);groups.setdefault(typ,[]).append(row)
 samples={k:sorted(v,key=lambda x:hashlib.sha256(('claim-evidence-v1:'+x['id']).encode()).hexdigest())[:2] for k,v in groups.items() if k in ['F_SH','F_MH','F_TP','MA_U','MA_P']}
 result['ever'][topic]={'counts':{k:len(v) for k,v in groups.items()},'qa_fields':list(q[0]),'dialogue_type':type(d).__name__,'dialogue_example':next(iter(d.items())) if isinstance(d,dict) else d[0],'samples':samples}
with (root/'Wikipedia_contradict_benchmark/WikiContradict_dataset_v1_rag_qa.csv').open(encoding='utf-8-sig') as f:wiki=list(csv.DictReader(f))
result['wiki']={'rows':len(wiki),'unique_ids':len({r['question_ID'] for r in wiki}),'fields':list(wiki[0]),'examples':wiki[:2]}
out=Path('/ceph_data/pjw031003/capstone-shared-knowledge/results')/f'sm-{os.environ["SLURM_JOB_ID"]}.json'
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('COMPLETE',out,flush=True)
