"""Verify the upstream pilot and score execution fidelity separately from transfer."""
from hashlib import sha256
import json
from pathlib import Path
import shutil


def main():
    repo=Path(__file__).resolve().parents[2]
    report=repo/'results/rationale-reuse/comrat-v1'
    ledger=json.loads((repo.parent/'campaigns/speakermem-dev/campaign-dispatch.json').read_text())
    job=ledger['jobs']['cup-comrat-original-v1']
    assert job['state']=='COMPLETED' and job['exit_code']=='0:0'
    result=json.loads((repo.parent/f"campaigns/speakermem-dev/results/sm-{job['job_id']}.json").read_text())
    assert result['status']=='complete' and str(result['job_id'])==job['job_id']
    freeze=json.loads((report/'freeze.json').read_text())
    for name,digest in freeze['files'].items():
        assert sha256((report/'runtime'/name).read_bytes()).hexdigest()==digest,name
    assert result['input_sha256']==freeze['files']['inputs.json']
    assert result['config_sha256']==freeze['files']['config.json']
    assert sha256((report/'keys.json').read_bytes()).hexdigest()==freeze['keys_sha256']
    source_manifest=json.loads((report.parent/'upstream-audit/comrat-manifest.json').read_text())
    source_digests={x['name'].split('Rationale-Analyses-Tool/',1)[1]:x['sha256']
                    for x in source_manifest['members'] if 'Rationale-Analyses-Tool/' in x['name']}
    for name,digest in result['upstream_sha256'].items():assert source_digests[name]==digest,name
    for name,digest in freeze['service_sha256'].items():
        assert sha256((repo/name).read_bytes()).hexdigest()==digest, name
    inputs=json.loads((report/'runtime/inputs.json').read_text())
    rows=result['documents'];assert len(rows)==len(inputs)==34
    for expected,actual in zip(inputs,rows):
        assert expected['id']==actual['id'] and expected['text']==actual['input_text']
        for raw in actual['raw_predictions']:
            assert len(raw['probabilities'])==len(actual['rows'])==len(raw['token_ids'])
            for probability,row in zip(raw['probabilities'],actual['rows']):
                assert int(probability>0.5)==row[raw['label']]
    by_id={r['id']:r for r in rows};assert len(by_id)==34
    keys=json.loads((report/'keys.json').read_text())
    fidelity=[];transfer=[]
    for key in keys:
        item=by_id[key['id']]
        if 'published_decision' in key:
            predicted=item['rows'][0]
            assert predicted['message_preprocessed']==item['input_text']
            fidelity.append(dict(id=key['id'],predicted=[predicted['Decision'],predicted['Rationale']],
                                 published=[key['published_decision'],key['published_rationale']],
                                 human_majority=[int(sum(key['human_decisions'])>=3),int(sum(key['human_rationales'])>=3)]))
        else:
            nonempty=[r for r in item['rows'] if r['message_preprocessed'].strip()]
            detected=bool(nonempty) and any(r['Decision'] for r in nonempty) and any(r['Rationale'] for r in nonempty)
            transfer.append(dict(id=key['id'],expected=key['reasoned_decision'],predicted=detected,
                                 source=item['input_text'],rows=nonempty))
    published_matches=sum(a==b for r in fidelity for a,b in zip(r['predicted'],r['published']))
    human_matches=sum(a==b for r in fidelity for a,b in zip(r['predicted'],r['human_majority']))
    tp=sum(x['predicted'] and x['expected'] for x in transfer)
    fp=sum(x['predicted'] and not x['expected'] for x in transfer)
    gate=published_matches==24 and tp==4 and fp==0
    summary=dict(status='complete',job_id=job['job_id'],slurm_state=job['state'],exit_code=job['exit_code'],
                 published_prediction_labels=dict(correct=published_matches,total=24,meaning='fidelity, not accuracy'),
                 human_majority_labels=dict(correct=human_matches,total=24,meaning='tiny public user-study subset'),
                 known_old_documents=dict(positive_detected=tp,positive_total=4,false_positives=fp,negative_total=7,
                                          unique_positive_sources=2,unique_negative_sources=7),
                 empty_rows=sum(not r['message_preprocessed'].strip() for item in rows for r in item['rows']),
                 routing_gate_passed=gate,adopted=False,default_service_unchanged=True,
                 qa_rerun=False,inference_seconds=result['inference_seconds'],gpu_allocation_seconds=job['elapsed_seconds'],
                 tensorflow=result['tensorflow'],devices=result['devices'],
                 limitations=['No pair-level reasoning, reconsideration, or QA measured.',
                              'Known authored transfer controls are not a natural benchmark.',
                              'Published predictions are not ground-truth labels.'])
    (report/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    (report/'cases.json').write_text(json.dumps(dict(fidelity=fidelity,transfer=transfer),indent=2)+'\n')
    shutil.copyfile(repo.parent/f"campaigns/speakermem-dev/results/sm-{job['job_id']}.json",report/'result.json')
    (report/'dispatch.json').write_text(json.dumps(job,indent=2)+'\n')
    (report.parent/'progress.json').write_text(json.dumps(dict(status='original_pilot_complete',job_id=job['job_id'],
        routing_gate_passed=gate,adopted=False,default_service_unchanged=True,running_jobs=[]),indent=2)+'\n')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
