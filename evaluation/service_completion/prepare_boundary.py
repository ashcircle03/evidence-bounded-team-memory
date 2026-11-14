"""Freeze the I/O-only candidate against the unchanged v3b evaluation inputs."""
from datetime import datetime,timezone
from hashlib import sha256
import json
from pathlib import Path
import shutil
import tarfile


def main():
    repo=Path(__file__).resolve().parents[2]
    previous=repo/'results/service-completion/v3b/runtime'
    version='cup-boundary-v1'
    folder=repo.parent/'campaigns/speakermem-dev/source'/version
    report=repo/'results/module-boundary/v1'
    folder.mkdir(exist_ok=False);report.mkdir(parents=True,exist_ok=False)
    cfg=json.loads((previous/'config.json').read_text())
    cfg.update(source_version=version,scope='I/O contracts only; unchanged same37 development regression',
        store_root='/local_datasets/pjw031003/capstone-shared-knowledge/service-stores')
    for name in ('serve.py','prepare_nltk.py','nltk-data.tar.gz','service.py','inputs.json'):
        shutil.copyfile(previous/name,folder/name)
    (folder/'run.sbatch').write_text((previous/'run.sbatch').read_text().replace('cup-completion-v3b',version))
    with tarfile.open(folder/'code.tar.gz','w:gz') as archive:
        for name in sorted(cfg['code_sha256']):archive.add(repo/name,arcname=name)
    cfg['code_sha256']={n:sha256((repo/n).read_bytes()).hexdigest() for n in cfg['code_sha256']}
    protocol='''# Module boundary v1 — fixed before inference

Same Qwen3-8B revision, nonthinking/temp0, same37 inputs and original keys as
cup-completion-v3b. No classifier prompt, QA prompt, model, retrieval configuration
or training change. No new LLM stage. Compare requests and outputs as well as scores.

Changes: sentence selector retains exact original offsets; malformed candidates
are rejected independently (all duplicate kind/targets rejected); comparator call
failure is a recorded failed receipt and cannot block reading captured sources.
Reconsideration effects are explicit derived state, never factual corrections.
New reconsideration snapshots are versioned; existing v1 renderings stay stable.
Only contexts containing reconsideration receive the new effect field/text.

Acceptance: preserve all previously correct legacy20 answers and required source
citations, all eight prior state/value plus review-citation successes, exact scope
of factual corrections, immutable original sources, original-owner review.
Inspect writer/cache positives and near-miss negatives separately. Plumbing tests
with supplied correct labels do NOT establish improved model classification.
Failure/empty extraction is not a correct negative. No semantic tuning after run.
Report strict full source coverage separately from the historical core-value gate.

Use existing QA keys; do not put keys in actor inputs. Raw calls, output, sources,
proposals, votes and snapshots retained. This is repeated authored development
data, not held-out or a full EverMemBench/STALE benchmark. Only three legacy QA
questions are natural EverMem-derived questions.

GPU1, CPU8, RAM48G, Slurm12h, conda, no node pin, --no-requeue, max800 calls.
No paid API. Node-local stores; export results to Ceph. No automatic retry.
'''
    (folder/'PROTOCOL.md').write_text(protocol)
    cfg['data_sha256']={n:sha256((folder/n).read_bytes()).hexdigest() for n in ('inputs.json','PROTOCOL.md')}
    (folder/'config.json').write_text(json.dumps(cfg,indent=2)+'\n')
    shutil.copytree(folder,report/'runtime')
    shutil.copyfile(repo/'evaluation/service_completion/keys.json',report/'keys.json')
    freeze=dict(created_at=datetime.now(timezone.utc).isoformat(),config=cfg,
        files={p.name:sha256(p.read_bytes()).hexdigest() for p in sorted(folder.iterdir())},
        prior='cup-completion-v3b',keys_sha256=sha256((report/'keys.json').read_bytes()).hexdigest())
    (report/'freeze.json').write_text(json.dumps(freeze,indent=2)+'\n')
    (report.parent/'progress.json').write_text(json.dumps(dict(status='frozen_not_submitted',version=version),indent=2)+'\n')
    print(folder);print(' '.join(freeze['files']))


if __name__=='__main__':main()
