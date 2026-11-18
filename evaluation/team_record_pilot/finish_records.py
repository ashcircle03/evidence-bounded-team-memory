"""Materialize v0.2.1 after the GPU extraction and checkpoint classifier finish."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from unittest.mock import patch

from team_memory.records import preserving, policy_scope, grouped
from evaluation.team_record_pilot.pilot import BY_ALIAS

def main(result_path, submitted_inputs, parser_python, output):
    result=json.loads(Path(result_path).read_text())
    inputs=Path(submitted_inputs).read_bytes()
    assert result['status']=='complete' and hashlib.sha256(inputs).hexdigest()==result['input_sha256']
    items={i['alias']:i for i in json.loads(inputs)}
    rows=result['rows']
    assert len(rows)==len(items)==len(BY_ALIAS) and {r['alias'] for r in rows}==set(items)==set(BY_ALIAS)
    proc=subprocess.run([parser_python,'-m','evaluation.record_binding.discourse.policy_predictions'],
        input=json.dumps([r['pairs'] for r in rows]),text=True,capture_output=True,check=True)
    traces=json.loads(proc.stdout)['rows']
    assert len(traces)==len(rows)
    records={}
    for row,trace in zip(rows,traces):
        alias=row['alias'];source=items[alias]['source'];assert source==BY_ALIAS[alias]['source']
        def generate(system,prompt):
            assert prompt==items[alias]['prompt'] and system=='Extract grounded records using the supplied format and examples.'
            return row['response']['choices'][0]['message']['content']
        def predict(local):
            assert local==row['pairs'] and len(local)==len(row['decisions'])==len(trace)
            return row['decisions']
        def syntax(pair,_):
            return trace[row['pairs'].index(pair)]
        with patch.object(policy_scope,'restriction',syntax):
            records[alias]=preserving.construct(source,generate,model='Qwen3-8B@b968826d9c46dd6066d109eabc6255188de91218',
                    predict=predict,training_counts={'disjoint':11974},parse=True)
    with Path(output).open('x') as stream:json.dump(records,stream,ensure_ascii=False)

if __name__=='__main__':
    main(*sys.argv[1:])
