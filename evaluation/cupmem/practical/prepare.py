"""Local-only deterministic packaging; never submits or changes an existing version."""
from hashlib import sha256
import json
from pathlib import Path
import shutil
import tarfile

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
CAMPAIGN = ROOT.parent/'campaigns/speakermem-dev'


def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')


def development():
    prior = json.loads((HERE.parent/'service-inputs.json').read_text())
    sources, questions = prior['sources'], prior['questions']
    events = [dict(label='initial_report', operation='ingest', source=sources[0]),
              dict(label='changed_condition', operation='ingest', source=sources[1]),
              dict(label='duplicate_report', operation='ingest', source=sources[1])]
    events += [dict(label='before_review/'+q['id'], operation='ask', question=q['question'],
                    temporal_scope=q['scope']) for q in questions]
    events += [dict(label='owner_review', operation='review_reconsider'),
               dict(label='unrelated_report', operation='ingest', source=sources[2])]
    events += [dict(label='after_review/'+q['id'], operation='ask', question=q['question'],
                    temporal_scope=q['scope']) for q in questions[:2]]
    data = dict(scope='Development only: existing Cedar stream plus explicit bulk import, not final evaluation',
                cases=[dict(id='cedar', events=events), dict(id='bulk', events=[
                    dict(label='bulk_import', operation='import_history', records=sources),
                    dict(label='bulk_folder', operation='ask', question=questions[1]['question'], temporal_scope='current'),
                    dict(label='bulk_runtimes', operation='ask', question=questions[0]['question'], temporal_scope='historical')])])
    write(HERE/'development.json', data)
    write(HERE/'development-key.json', dict(scope='Existing development cases only, evaluator not model input',
        source_expectations='../service-expected.json', bulk_expectations=dict(folder='Cedar-audit',
        runtimes='one process40 seconds and four processes12 seconds, with original citations'),
        required_operations_no_error=True, calls_per_qa=1, source_preservation=True, duplicate_calls=0,
        owner_review='only explicit simulated owner event may approve a reconsideration'))
    return HERE/'development.json'


def package(version, inputs, *, minutes=30, max_calls=400):
    if not version.startswith('cup-practical-') or not 15 <= minutes <= 90:
        raise ValueError('explicit practical version and bounded wall time required')
    dest = CAMPAIGN/'source'/version
    dest.mkdir(exist_ok=False)
    cfg = json.loads((CAMPAIGN/'source/cup-service-v1/config.json').read_text())
    code = list(cfg['code_sha256']) + ['team_memory/cupmem_candidates.py', 'team_memory/cupmem_practical.py']
    cfg['code_sha256'] = {name:sha256((ROOT/name).read_bytes()).hexdigest() for name in code}
    cfg.update(source_version=version, scope='Paired simple source retrieval/readout and practical CUPMem service',
        input_sha256=sha256(inputs.read_bytes()).hexdigest(), max_calls=max_calls,
        client_seconds=(minutes-10)*60, serve_seconds=(minutes-9)*60,
        resources=dict(gpus=1, cpus=8, ram_gb=48, wall_minutes=minutes))
    cfg['execution_changes'].update(native_pipeline_modified='Native writer unmodified; query generation replaced with candidate retrieval and one cited readout',
        embedding='Pinned encoder, batched32 and process-local text-vector cache; same in both arms',
        bulk_import='Full sources in original order; max16 records/12000characters per native session; original timestamps retained in source envelopes')
    write(dest/'config.json', cfg)
    shutil.copyfile(inputs, dest/'inputs.json')
    shutil.copyfile(HERE/'run.py', dest/'service.py')
    shutil.copyfile(HERE/'server.py', dest/'serve.py')
    with tarfile.open(dest/'code.tar.gz', 'w:gz') as archive:
        for name in code: archive.add(ROOT/name, arcname=name)
    template = (CAMPAIGN/'source/cup-service-v1/run.sbatch').read_text()
    template = template.replace('cup-service-v1', version).replace('--time=00:25:00', f'--time={minutes//60:02d}:{minutes%60:02d}:00')
    (dest/'run.sbatch').write_text(template)
    names = ['run.sbatch','config.json','serve.py','service.py','inputs.json','code.tar.gz']
    freeze = dict(source_version=version, input_sha256=cfg['input_sha256'], code_sha256=cfg['code_sha256'],
                  resources=cfg['resources'], files_sha256={n:sha256((dest/n).read_bytes()).hexdigest() for n in names})
    write(HERE/(version+'-freeze.json'), freeze)
    return freeze


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(); p.add_argument('version'); p.add_argument('--inputs', type=Path)
    p.add_argument('--minutes', type=int, default=30); p.add_argument('--max-calls', type=int, default=400)
    a = p.parse_args()
    print(json.dumps(package(a.version, a.inputs or development(), minutes=a.minutes, max_calls=a.max_calls), indent=2))
