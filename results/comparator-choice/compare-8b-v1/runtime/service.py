import json, os
from pathlib import Path
p=Path(__file__).resolve().parent
c=json.loads((p/'config.json').read_text())
os.environ['PYTHONPATH']=str(p/'code')+':'+c['reference_extras']
os.execv(c['python_client'], [c['python_client'], '-u', str(p/'code/evaluation/comparator_choice/run.py'), str(p)])
