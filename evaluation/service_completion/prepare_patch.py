"""Freeze a new source-patch execution packet; never submit or overwrite a run."""
from datetime import datetime, timezone
from hashlib import sha256
import importlib.metadata
import json
from pathlib import Path
import shutil
import tarfile


def main(version='cup-source-patch-v1'):
    repo=Path(__file__).resolve().parents[2]
    previous=repo/'results/service-completion/v3b/runtime'
    assert version in ('cup-source-patch-v1','cup-source-patch-v2')
    folder=repo.parent/'campaigns/speakermem-dev/source'/version
    folder.mkdir(exist_ok=False)
    report=repo/'results/source-patch'/version.rsplit('-',1)[-1];report.mkdir(parents=True,exist_ok=False)
    config=json.loads((previous/'config.json').read_text())
    config.update(source_version=version,scope='Two-stage source patch; same37 regression, not held-out',
                  store_root='/local_datasets/pjw031003/capstone-shared-knowledge/service-stores')
    remote=config['project']+'/source/sm-'+version
    for name in ('serve.py','prepare_nltk.py','nltk-data.tar.gz'):
        shutil.copyfile(previous/name,folder/name)
    shutil.copyfile(repo/'evaluation/service_completion/inputs.json',folder/'inputs.json')
    # Unmodified upstream pure-Python packages, including full package licenses.
    with tarfile.open(folder/'patch-deps.tar.gz','w:gz') as archive:
        for name,expected in [('jsonpatch','1.33'),('jsonpointer','3.0.0')]:
            dist=importlib.metadata.distribution(name);assert dist.version==expected
            for file in dist.files:
                rel=Path(str(file))
                if '..' in rel.parts or rel.suffix=='.pyc' or '__pycache__' in rel.parts:continue
                archive.add(dist.locate_file(file),arcname=str(rel))
    names=sorted(config['code_sha256'].keys() | {'team_memory/source_patch.py'})
    if version.endswith('v2'):names=sorted(set(names)|{'team_memory/decision_patch.py'})
    with tarfile.open(folder/'code.tar.gz','w:gz') as archive:
        for name in names:archive.add(repo/name,arcname=name)
    config['code_sha256']={name:sha256((repo/name).read_bytes()).hexdigest() for name in names}
    protocol='''# Source patch v1 — fixed before inference

One run, same Qwen3-8B revision, nonthinking/temp0, same37 QA inputs and original
keys as completion v3b. Existing20 core answers+required evidence must remain20/20;
the eight previously passing state/value+review citation cases must remain8/8.
Rate strict direct-source coverage separately (the older release/pending output
already lacked its direct incoming citation). Judge the original writer/cache
positive relations for reconsideration+correct changed premise and the two
negative relations for no unnecessary proposal. Empty extraction, failed receipt,
missing update or parse failure cannot count as a correct negative. Inspect actual
source sentences and before/after delta, not keyword labels. Preserve any failure.

Implementation: old-only typed extraction, bounded RFC6902 update of value/scope,
deterministic kind gate, unchanged original sources and owner approval. Full raw
requests/outputs retained. No answer key in actor. No new answer prompts or QA
models. One extra comparison call per incoming source. jsonpatch1.33 and
jsonpointer3.0.0 are unmodified offline pure-Python dependencies with licenses.

GPU1, conda, Slurm12h, no node pin, max800 calls, no paid API. Temporary stores
on node-local /local_datasets; exported full source/proposal/vote/snapshot records
on Ceph. No semantic revision after outputs; do not add prompt variants this run.
This repeated authored development set is not a natural or independent benchmark.
'''
    if version.endswith('v2'):
        config['scope']='Existing factual comparator plus source-bound decision patch; same37 regression'
        protocol=protocol.replace('Source patch v1','Decision patch v2')
        start=protocol.index('Implementation:');end=protocol.index('GPU1,')
        protocol=protocol[:start]+'''Implementation: the v1 flat value schema let actions occupy premise fields
and caused format failures, losing earlier fact corrections. v1 is preserved and
not adopted. Keep the v3b factual comparison input/prompt/output unchanged. Extract
only reasoned decisions from old sources through vLLM guided_json; decision and
basis are different immutable source references. Existing factual proposals that
overlap those decision/basis spans are suppressed and retained in the audit. A
scoped RFC6902 patch can replace only the basis reference with incoming evidence;
it cannot change action or choose kind. A changed basis yields reconsideration;
unchanged/not-addressed gives no proposal. Unknown remains an explicit abstention,
not a correct negative. Explanations render original quotes, not invented values.
No extra QA stage or prompt. jsonpatch1.33/jsonpointer3.0.0 unmodified. Two comparison
calls for pure fact inputs, three when decisions need updates. Source/owner
approval and evidence contracts are unchanged. Guided schema reaches HTTP while
retaining nonthinking and the original QA model configuration.

''' +protocol[end:]
    (folder/'PROTOCOL.md').write_text(protocol)
    config['data_sha256']={n:sha256((folder/n).read_bytes()).hexdigest()
                            for n in ('inputs.json','PROTOCOL.md','patch-deps.tar.gz')}
    (folder/'config.json').write_text(json.dumps(config,indent=2)+'\n')
    service=(previous/'service.py').read_text().replace("str(p/'code')+':'+c['reference_extras']",
        "str(p/'code')+':'+os.environ['PATCH_DEPS']+':'+c['reference_extras']")
    (folder/'service.py').write_text(service)
    script=(previous/'run.sbatch').read_text().replace('cup-completion-v3b',version)
    marker='unset OPENAI_API_KEY BAZE_API_KEY HF_TOKEN HUGGING_FACE_HUB_TOKEN'
    setup=f'''export PATCH_DEPS=/local_datasets/pjw031003/capstone-shared-knowledge/patch-deps/$SLURM_JOB_ID
mkdir -p "$PATCH_DEPS"
tar -xzf {remote}/patch-deps.tar.gz -C "$PATCH_DEPS"
'''
    (folder/'run.sbatch').write_text(script.replace(marker,setup+marker))
    runtime=report/'runtime';shutil.copytree(folder,runtime)
    freeze=dict(created_at=datetime.now(timezone.utc).isoformat(),config=config,
                files={p.name:sha256(p.read_bytes()).hexdigest() for p in sorted(folder.iterdir())},
                prior='cup-completion-v3b',keys_sha256=sha256((repo/'evaluation/service_completion/keys.json').read_bytes()).hexdigest())
    (report/'freeze.json').write_text(json.dumps(freeze,indent=2)+'\n')
    shutil.copyfile(repo/'evaluation/service_completion/keys.json',report/'keys.json')
    (report.parent/'progress.json').write_text(json.dumps(dict(status='frozen_not_submitted',version=version),indent=2)+'\n')
    print(folder)
    print(' '.join(freeze['files']))


if __name__=='__main__':
    import sys
    main(sys.argv[1] if len(sys.argv)>1 else 'cup-source-patch-v1')
