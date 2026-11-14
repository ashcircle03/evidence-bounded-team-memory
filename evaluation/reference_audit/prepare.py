"""Package a fixed audit; intentionally never submits or edits production code."""
from hashlib import sha256
import json
from pathlib import Path
import shutil
import signal
import tarfile

from evaluation.reference_audit.run import digest

ROOT = Path(__file__).resolve().parents[2]
VERSION = 'reference-audit-v1'


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')


def main():
    keys = [ROOT/'evaluation/qa20/evaluator/key.json', ROOT/'evaluation/service_v3/stream-keys.json',
            ROOT/'results/module-boundary/v1/keys.json', ROOT/'evaluation/comparator_choice/oracle-key.json']
    for path in keys:
        assert path.is_file(), path
    folder = ROOT.parent/'campaigns/speakermem-dev/source'/VERSION
    report = ROOT/'results/reference-audit/v1'
    folder.mkdir(exist_ok=False); report.mkdir(parents=True, exist_ok=False)
    packets = []; provenance = []; historical = []
    for prefix, name in [('observed','module-boundary/v1'), ('oracle','comparator-choice/oracle-v1')]:
        origin = ROOT/'results'/name
        result = json.loads((origin/'result.json').read_text())
        for row in result['rows']:
            if row.get('request',{}).get('operation') != 'ask':
                continue
            key = row['case_id']+'/'+row['label']; cid = prefix+'/'+key
            answer = row['result']; ws = answer['citation_sources']; context = answer.get('review_context')
            identity = digest(dict(witnesses=ws, review_context=context))
            packets.append(dict(id=cid, split='legacy20' if row['case_id'].startswith('legacy-') else prefix,
                                question=row['request']['question'], witnesses=ws, review_context=context,
                                evidence_sha256=identity))
            provenance.append(dict(id=cid, origin=str(origin.relative_to(ROOT)), source_job=result['job_id'],
                                   original_key=key, result_sha256=sha256((origin/'result.json').read_bytes()).hexdigest()))
            historical.append(dict(id=cid, result=answer))
        shutil.copyfile(origin/'ratings.json', report/(prefix+'-historical-ratings.json'))
    assert len(packets) == 45 and sum(p['split']=='legacy20' for p in packets)==20
    write(folder/'inputs.json',dict(packets=packets))
    write(report/'case-provenance.json',provenance)
    write(report/'historical-outputs.json', historical)
    for i, path in enumerate(keys):
        shutil.copyfile(path, report/(f'gold-{i}-'+path.name))
    baseline = ROOT/'results/module-boundary/v1/runtime'
    cfg = json.loads((baseline/'config.json').read_text())
    cfg.update(source_version=VERSION, model_path=cfg['model_shared'], max_calls=2000,
               startup_seconds=900, client_seconds=10800, serve_seconds=11700,
               scope='Frozen45 QA; four reference-composition arms; not a paper reproduction')
    # Preserve the known server startup/cleanup behavior but read shared weights
    # directly. No implicit cache copy to another compute node is permitted.
    serve = (baseline/'serve.py').read_text()
    begin = serve.index('        local,shared=')
    end = serve.index('        cmd=',begin)
    serve = serve[:begin]+'''        local=shared=Path(cfg['model_shared'])
        ready=json.loads((shared/'READY.json').read_text())
        assert ready['revision']==cfg['model_revision']
        assert ready['files_sha256']==cfg['model_files_sha256']
        for name,expected in cfg['model_files_sha256'].items():
            assert Path(name).name==name
            h=hashlib.sha256()
            with (shared/name).open('rb') as stream:
                while block:=stream.read(8*1024*1024):h.update(block)
            assert h.hexdigest()==expected,name
        record['cache_check']='All shared checkpoint SHA256 verified on compute node; no local copy'
'''+serve[end:]
    serve = serve.replace("'service-completion-'+record['job_id']", "'reference-audit-'+record['job_id']")
    (folder/'serve.py').write_text(serve)
    service = (baseline/'service.py').read_text().replace('evaluation/service_completion/run.py','evaluation/reference_audit/run.py')
    (folder/'service.py').write_text(service)
    script = (baseline/'run.sbatch').read_text().replace('cup-boundary-v1',VERSION)
    script = script.replace('#SBATCH --nodes=1', '#SBATCH --nodes=1\n#SBATCH --nodelist=aurora-g8')
    script = script.replace('reference-nltk/$SLURM_JOB_ID', 'reference-nltk/120445')
    line = next(x for x in script.splitlines() if x.endswith('/prepare_nltk.py'))
    script = script.replace(line, 'test -f "$NLTK_DATA/tokenizers/punkt_tab/english/ortho_context.tab"')
    (folder/'run.sbatch').write_text(script)
    shutil.copyfile(ROOT/'evaluation/reference_audit/PROTOCOL.md', folder/'PROTOCOL.md')
    # Narrow source-only recursion, explicit timeout. No data, venv or checkpoint.
    signal.alarm(10)
    code = [p for p in (ROOT/'team_memory').rglob('*') if p.is_file() and
            (p.suffix in ('.py','.md') or p.name.startswith(('LICENSE','NOTICE')))]
    code += list((ROOT/'evaluation/reference_audit').glob('*.py'))
    with tarfile.open(folder/'code.tar.gz','w:gz') as archive:
        for path in sorted(set(code)):
            archive.add(path, arcname=str(path.relative_to(ROOT)), recursive=False)
    cfg['code_sha256'] = {str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest() for p in sorted(set(code))}
    signal.alarm(0)
    cfg['data_sha256'] = {n:sha256((folder/n).read_bytes()).hexdigest() for n in ['inputs.json','PROTOCOL.md']}
    write(folder/'config.json',cfg)
    manifest = {p.name:sha256(p.read_bytes()).hexdigest() for p in folder.iterdir() if p.is_file()}
    write(report/'freeze.json',dict(source_version=VERSION,packet_files=manifest,
                                  local_gold_sha256={p.name:sha256(p.read_bytes()).hexdigest() for p in report.iterdir() if p.is_file()},
                                  production_code_sha256=cfg['code_sha256']))
    (report/'runtime').mkdir()
    for path in folder.iterdir():
        shutil.copyfile(path,report/'runtime'/path.name)
    print(folder)


if __name__=='__main__':
    main()
