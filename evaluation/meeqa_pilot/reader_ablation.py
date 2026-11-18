"""Single-meeting reader ablation using frozen records and verified baseline prompts."""
import hashlib
import json
import os
from pathlib import Path

import httpx

from evaluation.meeqa_pilot.run import REV, SYSTEM, TEAM_QA_TEMPLATE, post, turns


INSTRUCTION = """Read this single meeting excerpt and answer the participant's question.
A single speaker can supply the answer. An indirect reply or a conditional reply can answer
the question if it supplies the information requested. Check that the selected words support
the requested detail about the right person or action. Abstain if the excerpt leaves it open.
Use the transcript as the source for verbatim answers and quotations.

{context}

Question: {question}"""


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()


def contexts(item, records):
    notes = []
    for offset, source in turns(item):
        graph = records[source['id']]['graph']
        units = {u['id']: u for u in graph['units']}
        for claim in graph['claims']:
            note = {}
            for role in ('claim', 'condition', 'basis', 'time', 'subject'):
                note[role] = [dict(start=offset + units[u]['start'], end=offset + units[u]['end'],
                                   text=units[u]['quote']) for u in claim[role]]
            note.update(speaker=source['speaker'], assertion_stances=[a['stance'] for a in claim['assertions']])
            notes.append(note)
    return {arm: 'Source 1:\n' + item['context'] + '\nRecords annotations:\n' + json.dumps(data, ensure_ascii=False)
            for arm, data in [('raw', []), ('records', notes)]}


def reconstruct(panel, previous):
    assert previous['status'] == 'complete' and previous['revision'] == REV
    data = {i['id']: (i, contexts(i, previous['records'])) for i in panel}
    jobs = {}
    for row in previous['answers']:
        key = row['id'], row['arm']
        item, by_arm = data[key[0]]
        context = by_arm[key[1]]
        old = TEAM_QA_TEMPLATE.format(context_str=context, query_str=item['question'])
        assert digest(old) == row['prompt_sha256'] and key not in jobs
        jobs[key] = INSTRUCTION.format(context=context, question=item['question'])
    assert len(jobs) == 2*len(panel) == 16
    return jobs


def main():
    folder = Path(os.environ['READER_PACKET'])
    cfg = json.loads((folder/'config.json').read_text())
    path = Path(os.environ['RECORD_INPUTS'])
    assert hashlib.sha256(path.read_bytes()).hexdigest() == cfg['input_sha256']
    root = Path(cfg['project'])/'results'
    previous = json.loads((root/'meeqa-124297.json').read_text())
    assert previous['input_sha256'] == cfg['input_sha256']
    jobs = reconstruct(json.loads(path.read_text()), previous)
    job = os.environ['SLURM_JOB_ID']
    target = root/f'meeqa-{job}.json'
    assert not target.exists()
    report = dict(job=job, revision=REV, input_sha256=cfg['input_sha256'], status='started', answers=[], oracle=[])
    def save():
        tmp = target.with_suffix('.tmp')
        tmp.write_text(json.dumps(report, ensure_ascii=False))
        tmp.replace(target)
    with httpx.Client(trust_env=False,timeout=300) as client:
        for (qid, arm), prompt in jobs.items():
            response = post(client, SYSTEM, prompt)
            report['answers'].append(dict(id=qid, arm=arm, response=response, prompt_sha256=digest(prompt)))
            save()
        # Gold locations are accessed only after the 16 blind predictions have been persisted.
        hints = json.loads((folder/'hints.json').read_text())
        for row in report['answers']:
            hint = hints.get(row['id'])
            prediction = json.loads(row['response']['choices'][0]['message']['content'])
            if hint and prediction['outcome'] == 'abstain':
                prompt = jobs[row['id'],row['arm']] + f"\nInspect transcript character range [{hint[0]}, {hint[1]}) in particular: {hint[2]}"
                report['oracle'].append(dict(id=row['id'],arm=row['arm'],response=post(client,SYSTEM,prompt)))
        report['status'] = 'complete'
        save()


if __name__ == '__main__':
    main()
