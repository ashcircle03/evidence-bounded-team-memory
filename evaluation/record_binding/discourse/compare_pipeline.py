"""Produce a semantic fingerprint per document, using tagged or working builder code."""
import json
from hashlib import sha256
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from unittest.mock import patch

from langextract import resolver
from team_memory.records import graph, preserving, policy_scope
from evaluation.record_binding import first_loss
from evaluation.record_binding.discourse.evaluate import edge_identity
from evaluation.record_binding.discourse.evaluate_scope import OUT, SOURCE
from evaluation.record_binding.first_loss import read, reader_packets
from evaluation.record_bound.rows import compiled_rows
from evaluation.record_full.evaluate import score


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def main(mode, parser_python, destination):
    assert mode in {"tag", "current"}
    cases = read(OUT/'evaluation.json')['cases']
    docs = {d['id']: d for d in read('evaluation/record_full/gold.json')['documents']}
    items = {i['id']: i for i in read(SOURCE/'record-pair-v1/inputs.json')}
    syntax = subprocess.run([parser_python, '-m', 'evaluation.record_binding.discourse.policy_predictions'],
        input=json.dumps([c['localized'] for c in cases]), text=True, capture_output=True, check=True)
    traces = json.loads(syntax.stdout)['rows']
    assert len(cases) == len(traces) == len(docs) == len(items) == 68
    align = resolver.Resolver.align
    report = {}
    counts = read(OUT/'record-scope-124247.json')['train_stats']['geometries']
    witnesses_from = first_loss.witnesses_from
    with TemporaryDirectory() as tmp:
        for c, trace in zip(cases, traces):
            iid = c['id']
            key = docs[iid]
            src = items[iid]['source']
            calls = []
            prompts = []
            predicted = []
            def count(self, extractions, *args, **kwargs):
                calls.extend(e.extraction_text for e in extractions)
                return align(self, extractions, *args, **kwargs)
            def generate(system, prompt):
                prompts.append(digest([system, prompt]))
                return items[iid]['original_raw']
            localized = [{k:v for k,v in p.items() if k != 'geometry'} for p in c['localized']]
            def predict(pairs):
                assert pairs == localized
                predicted.extend(pairs)
                return [output['decision'] for output in c['outputs']['sentence']]
            def syntax_for(pair, _parse):
                # The isolated spaCy worker evaluated the exact same pair.
                return trace[localized.index(pair)]
            with patch.object(resolver.Resolver, 'align', count), patch.object(
                policy_scope, 'restriction', syntax_for), patch.object(
                graph, 'sentence_units', wraps=graph.sentence_units) as partition:
                if mode == 'tag':
                    record = policy_scope.construct(src, generate, predict, counts, model='paired', parse=True)
                else:
                    record = preserving.construct(src, generate, predict=predict, training_counts=counts,
                                                  model='paired', parse=True)
            assert len(prompts)==1 and predicted==localized
            witnesses = []
            def capture(bundle):
                result = witnesses_from(bundle)
                witnesses.extend(result)
                return result
            with patch.object(first_loss, 'witnesses_from', capture):
                packets = reader_packets(record, Path(tmp)/iid)
            rows = compiled_rows(record)
            s = score(rows, key, src)
            correct = sorted(set(map(tuple,key['edges'])) - set(s['missing_edges']))
            wrong = sorted(edge_identity(e,record,rows) for e in s['incorrect_edges'])
            report[iid] = dict(correct=correct, incorrect=wrong, complete=s['complete'],
                record=digest(record), reader=digest(witnesses), packet_index=digest(packets), packets=len(packets),
                prompt=prompts[0], role_input=digest(predicted), alignments=len(calls), partitions=partition.call_count)
    Path(destination).write_text(json.dumps(report, indent=2)+'\n')


def compare(tag_path, new_path, output):
    baseline, current = read(tag_path), read(new_path)
    assert baseline.keys() == current.keys() and len(current) == 68
    cases = []
    for iid, old in baseline.items():
        new = current[iid]
        for field in old.keys() - {'partitions', 'alignments'}:
            assert old[field] == new[field], (iid, field)
        assert new['partitions'] == 1 and new['alignments'] <= old['alignments'], iid
        cases.append(dict(id=iid, correct=new['correct'], incorrect=new['incorrect'],
                          record_sha256=new['record'], reader_sha256=new['reader'],
                          packets=new['packets'], old_alignments=old['alignments'],
                          alignments=new['alignments'], old_partitions=old['partitions'],
                          partitions=new['partitions']))
    assert sum(len(c['correct']) for c in cases) == 51
    assert sum(len(c['incorrect']) for c in cases) == 19
    Path(output).write_text(json.dumps(dict(baseline='v0.2.0', cases=cases), indent=2)+'\n')


if __name__ == '__main__':
    if sys.argv[1] == 'compare':
        compare(*sys.argv[2:])
    else:
        main(*sys.argv[1:])
