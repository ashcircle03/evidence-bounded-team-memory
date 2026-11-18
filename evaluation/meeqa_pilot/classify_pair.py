import hashlib
import json
import os
from pathlib import Path
from urllib.request import Request, build_opener, ProxyHandler

folder = Path(__file__).resolve().parent
cfg = json.loads((folder / 'config.json').read_text())
path = Path(os.environ['RECORD_INPUTS'])
assert hashlib.sha256(path.read_bytes()).hexdigest() == cfg['input_sha256']
items = {item['id']: item for item in json.loads(path.read_text())}
hints = json.loads((folder / 'hints.json').read_text())
assert len(hints) == 2
instruction = ("Classify how the given utterance responds to the question. "
               "Choose direct if it explicitly supplies the requested answer without a condition, "
               "indirect_or_conditional if it answers by implication or makes the answer depend on a condition, "
               "or no_answer if it does not supply an answer. Use only the question and utterance.")
labels = ['direct', 'indirect_or_conditional', 'no_answer']
rows = []
for qid, (start, end, utterance) in hints.items():
    item = items[qid]
    assert item['context'][start:end] == utterance
    messages = [dict(role='system', content=instruction),
                dict(role='user', content=f"Question: {item['question']}\nUtterance: {utterance}")]
    body = dict(model='Qwen3-8B', messages=messages, temperature=0, seed=42, max_tokens=512,
                chat_template_kwargs={'enable_thinking': False}, guided_choice=labels)
    request = Request(os.environ['PRACTICAL_MODEL_URL']+'/chat/completions',
                      data=json.dumps(body).encode(),headers={'Content-Type':'application/json'})
    with build_opener(ProxyHandler({})).open(request,timeout=300) as response:
        raw = json.load(response)
    choice = raw['choices'][0]
    label = choice['message']['content'].strip()
    assert label in labels and choice['finish_reason'] == 'stop'
    rows.append(dict(id=qid, request=body, response=raw, label=label))
job = os.environ['SLURM_JOB_ID']
dst = Path(cfg['project'])/'results'/f'meeqa-{job}.json'
with dst.open('x') as stream:
    json.dump(dict(status='complete',job=job,revision=cfg['model_revision'],rows=rows),stream,indent=2)
