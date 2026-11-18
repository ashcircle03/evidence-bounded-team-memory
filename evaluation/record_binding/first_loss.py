"""Offline records audit. Run from repository root with the project's Python."""
from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from evaluation.record_causal.storage import correct_stance_nodes
from evaluation.record_bound.rows import compiled_rows
from evaluation.record_full.evaluate import matches, raw_rows, score
from team_memory.records import preserving
from team_memory.records.graph import linked_span
from team_memory.adapters.base import request
from team_memory.adapters.records import RecordsAdapter
from team_memory.adapters.reader_bridge import evidence_from, witnesses_from
from team_memory.contracts.ports import CallContext

OLD = Path('results/record-binding/v4')
OUT = Path('results/record-binding/first-loss')
ROLES = {'condition', 'basis'}


def read(path):
    return json.loads(Path(path).read_text())


def hit(span, node):
    """Require both the frozen text match and overlap with a gold occurrence."""
    return matches(span['quote'], node) and any(
        max(span['start'], loc['start']) < min(span['end'], loc['end']) for loc in node['spans'])


def raw_inventory(source, raw):
    rows = raw_rows(raw)
    for row, item in zip(rows, json.loads(raw)['extractions']):
        try:
            row.update(preserving._aligned_span(source, item))
            row['quote'] = source['text'][row['start']:row['end']]
        except ValueError as error:
            row['alignment_error'] = str(error)
    return rows


def reader_packets(source, root):
    graph = source['record_graph']
    ctx = CallContext('audit', 'importer', frozenset(['records:read','records:write','records:import']))
    payload = dict(source=source, expected_revision=0, idempotency_key=source['id'])
    result = RecordsAdapter(root, 'audit').handle(request('record.append', payload, workspace_id='audit',
        request_id=source['id']), context=ctx)
    assert result['status'] == 'ok'
    snap = RecordsAdapter(root, 'audit').snapshot()
    assert snap['sources'] == [source]
    units = {unit['id']: unit for unit in graph['units']}
    packets = {}
    for group in graph['claims']:
        unit = units[group['claim'][0]]
        start,end = linked_span(source,unit['start'],unit['end'])
        evidence = evidence_from(dict(source_id=source['id'],start=start,end=end,
            quote=source['text'][start:end]), snap, 1)
        bundle = dict(snapshot=snap,query=dict(text='transport',time_scope='current',as_of=None,
            conditions=[]),evidence=[evidence],coverage='hits',unresolved_proposal_ids=[])
        witness = witnesses_from(bundle)[0]
        received = next(c for c in witness['record_context']['claims'] if c['id']==group['id'])
        for role in ('claim','basis','condition','time','subject'):
            assert [s['id'] for s in received[role]] == group[role]
        assert all(witness[k]==source[k] for k in ('speaker','observed_at','location'))
        packets[group['id']] = dict(start=start,end=end,quote=witness['quote'],received=received)
    return packets


def owner_groups(rows, node, *, only_claim=False):
    return {r['group'] for r in rows if 'quote' in r and hit(r,node) and
            (not only_claim or r['role']=='claim')}


def classify(edge, nodes, raw, graph, raw_score, stored_score):
    target, role, context = edge
    a, b = nodes[target+':claim'], nodes[context]
    if tuple(edge) not in stored_score['missing_edges']:
        return 'retained'
    raw_correct = tuple(edge) not in raw_score['missing_edges']
    if graph['status']=='failed' and raw_correct:
        return 'whole_record_rejected'
    if raw_correct:
        return 'raw_to_graph'
    aligned = [r for r in raw if 'quote' in r]
    targets = owner_groups(aligned,a,only_claim=True)
    contexts = [r for r in aligned if hit(r,b)]
    if not targets:
        return 'target_missing_or_split'
    if not contexts:
        return 'context_missing_or_split'
    separate = [r for r in contexts if not hit(r,a)]
    if not separate:
        return 'context_inside_target'
    if any(r['role']==role for r in separate) and not any(r['group'] in targets and r['role']==role for r in separate):
        return 'target_assignment'
    if any(r['group'] in targets for r in separate):
        return 'role_assignment'
    return 'target_and_role_or_unresolved'


def audit_pairs(item, output, gold, missing):
    catalog=item['catalog']
    labels={(q['context']['id'], t['id']):json.loads(output[q['context']['id']])[t['id']]
            for q in catalog['queries'] for t in q['targets']}
    spans={s['id']:s for s in catalog['contexts']}
    nodes={n['id']:n for n in gold['nodes']}
    support=defaultdict(set)
    for target,role,context in gold['edges']+gold['optional_edges']:
        if role in ROLES:
            for key in labels:
                if hit(spans[key[0]],nodes[context]) and hit(spans[key[1]],nodes[target+':claim']):
                    support[key].add(role)
    oracles=[]
    for target,role,context in gold['edges']:
        if role not in ROLES:continue
        a,b=nodes[target+':claim'],nodes[context]
        targets=[s for s in catalog['targets'] if hit(s,a)]
        contexts=[s for s in catalog['contexts'] if hit(s,b)]
        pairs=[(c['id'],t['id']) for c in contexts for t in targets if (c['id'],t['id']) in labels]
        correct=any(labels[k]==role for k in pairs)
        wrong_target=[k for k,v in labels.items() if v==role and v not in support[k]
                      and any(k[0]==c for c,_ in pairs) and not hit(spans[k[1]],a)]
        # Only relabel a positive prediction. Turning NONE into a relation also changes existence.
        wrong_role=[k for k in pairs if labels[k] in ROLES-{role} and labels[k] not in support[k]]
        qualifies=catalog['status']=='ready'
        can_supply_context=any(not(loc['start']<=t['start'] and t['end']<=loc['end'])
                               for t in targets for loc in b['spans'])
        can_supply_target=any(not(c['start']<=loc['start'] and loc['end']<=c['end'])
                              for c in contexts for loc in a['spans'])
        oracles.append(dict(edge=[target,role,context],baseline_missing=(target,role,context) in missing,
            eligible_pairs=[[*k,labels[k]] for k in pairs],correct_label=correct,
            gold_context_only=qualifies and not pairs and can_supply_context,
            gold_target_span_only=qualifies and not pairs and can_supply_target,
            target_only=list(wrong_target) if not correct else [],
            role_only=list(wrong_role) if not correct else []))
    decisions=[]
    for (c,t),role in labels.items():
        valid=support[c,t]
        other=any(k[0]==c and role in v for k,v in support.items())
        category=('supported' if role in valid else 'missed_or_wrong_type' if valid else
                  'wrong_target' if role in ROLES and other else
                  'unadjudicated_positive' if role in ROLES else 'no_gold_positive')
        decisions.append(dict(context=c,target=t,label=role,gold_roles=sorted(valid),category=category))
    return oracles,decisions


def main():
    for table in ('frozen_evaluation_files','code_sha256'):
        for name, digest in read(OLD/'pair-freeze.json')[table].items():
            assert sha256(Path(name).read_bytes()).hexdigest()==digest,name
    gold=read('evaluation/record_full/gold.json')['documents']
    packet_path=Path(read(OLD/'pair-freeze.json')['packet_inputs'])
    assert sha256(packet_path.read_bytes()).hexdigest()==read(OLD/'pair-freeze.json')['data_sha256']['inputs.json']
    inputs={i['id']:i for i in read(packet_path)}
    original={r['id']:r['raw'] for r in read('results/record-strata/v1/record-strata-122970.json')['rows'] if r['arm']=='ours'}
    sources={r['id']:r['source'] for r in read(OLD/'pair-stored.json') if r['arm']=='baseline'}
    outputs={r['id']:r['outputs'] for r in read(OLD/'record-pair-123016.json')['rows']}
    scores={r['id']:r['score'] for r in read(OLD/'pair-evaluation.json')['cases'] if r['arm']=='baseline'}
    documents=[]
    with TemporaryDirectory() as root:
        for d in gold:
            iid=d['id']; source=sources[iid]; graph=source['record_graph']; item=inputs[iid]
            assert item['original_raw']==original[iid]
            assert item['source']=={k:v for k,v in source.items() if k!='record_graph'}
            rows=compiled_rows(source); s=score(rows,d,source)
            assert json.loads(json.dumps(s))==scores[iid]
            raw=raw_inventory(source,original[iid]); initial=score(raw,d,source)
            packets=reader_packets(source,Path(root)/iid)
            nodes={n['id']:n for n in d['nodes']}
            groups={g:[r for r in rows if r['group']==g] for g in packets}
            by_group={g:score(rr,d,source) for g,rr in groups.items()}
            raw_claim_groups={g:{r['group'] for r in raw if r['role']=='claim' and 'quote' in r
                and any((r['start'],r['end'])==(a['spans'][0]['start'],a['spans'][-1]['end'])
                        for a in packets[g]['received']['assertions'])} for g in groups}
            edges=[]
            for e in d['edges']:
                a,b=nodes[e[0]+':claim'],nodes[e[2]]
                owners=sorted(g for g,ss in by_group.items() if tuple(e) not in ss['missing_edges'])
                edges.append(dict(edge=e,target_positions=a['spans'],context_positions=b['spans'],
                    raw_target_rows=[r['id'] for r in raw if matches(r['text'],a)],
                    raw_context_rows=[r['id'] for r in raw if matches(r['text'],b)],
                    raw_correct=tuple(e) not in initial['missing_edges'],stored_owner_groups=owners,
                    reader_packets=owners,first_loss=classify(e,nodes,raw,graph,initial,s)))
            # Relabel one existing compiled row, holding text, group and every other row fixed.
            # Report group-level success separately from defensible atomic ownership.
            baseline_repairs=[]
            for e in d['edges']:
                target,role,context=e
                if role not in ROLES or tuple(e) not in s['missing_edges']:continue
                for row in rows:
                    if row['role']==role or not matches(row['text'],nodes[context]):continue
                    if not any(matches(r['text'],nodes[target+':claim']) for r in groups[row['group']] if r['role']=='claim' and r['id']!=row['id']):continue
                    trial=[dict(r,role=role) if r['id']==row['id'] else r for r in rows]
                    changed=score(trial,d,source)
                    if tuple(e) in changed['missing_edges']:continue
                    lost=set(changed['missing_edges'])-set(s['missing_edges'])
                    added=set(changed['incorrect_edges'])-set(s['incorrect_edges'])
                    baseline_repairs.append(dict(edge=e,row=row,group_ambiguous=len(packets[row['group']]['received']['assertions'])!=1,
                        lost_edges=sorted(lost),added_fp=sorted(added),
                        lost_content=sorted(set(changed['missing_nodes'])-set(s['missing_nodes'])),
                        lost_stances=sorted(correct_stance_nodes(rows,d)-correct_stance_nodes(trial,d)),
                        stance_delta=changed['stance_correct']-s['stance_correct']))
            target_trials=[]
            for edge in d['edges']:
                owner,role,context=edge
                if role not in ROLES or tuple(edge) not in s['missing_edges']:continue
                destinations={r['group'] for r in rows if r['role']=='claim' and matches(r['text'],nodes[owner+':claim'])}
                for row in rows:
                    if row['role']!=role or not matches(row['text'],nodes[context]):continue
                    for group in sorted(destinations-{row['group']}):
                        moved=[dict(r,group=group) if r['id']==row['id'] else r for r in rows]
                        trial=score(moved,d,source)
                        if tuple(edge) not in trial['missing_edges']:
                            target_trials.append(dict(edge=edge,row=row,to=group,
                                group_ambiguous=len(packets[group]['received']['assertions'])!=1,
                                lost_edges=sorted(set(trial['missing_edges'])-set(s['missing_edges'])),
                                added_fp=sorted(set(trial['incorrect_edges'])-set(s['incorrect_edges'])),
                                lost_content=sorted(set(trial['missing_nodes'])-set(s['missing_nodes'])),
                                lost_stances=sorted(correct_stance_nodes(rows,d)-correct_stance_nodes(moved,d)),
                                stance_delta=trial['stance_correct']-s['stance_correct']))
            fps=[]
            for e in s['incorrect_edges']:
                owners=[g for g,ss in by_group.items() if tuple(e) in ss['incorrect_edges']]
                assert owners,(iid,e)
                for_group=[]
                for g in owners:
                    matched=[r for r in groups[g] if r['role']!='claim' and
                        (r['id']==int(e[2].split(':')[1]) if e[2].startswith('unmatched:') else
                         matches(r['text'],nodes[e[2]]))]
                    candidates=[r for r in raw if 'quote' in r and r['group'] in raw_claim_groups[g] and any(
                        r['role']==m['role'] and u['start']<r['end'] and r['start']<u['end'] for m in matched
                        for u in packets[g]['received'][m['role']])]
                    upstream=[]
                    for rg in raw_claim_groups[g]:
                        rs=score([r for r in raw if r['group']==rg],d,source)
                        for owner,role,node in rs['incorrect_edges']:
                            same_owner=owner==e[0] or (owner=='unbound:'+rg and e[0]=='unbound:'+g)
                            same_node=node==e[2] if not node.startswith('unmatched:') else (
                                e[2].startswith('unmatched:') and int(node.split(':')[1]) in {r['id'] for r in candidates})
                            if same_owner and same_node and role==e[1]:upstream.append([owner,role,node])
                    for_group.append(dict(group=g,raw_scored_equivalents=upstream,target_status='ambiguous_group' if
                        len(packets[g]['received']['assertions'])!=1 else 'single_assertion',
                        compiled_rows=matched,raw_row_ids=[r['id'] for r in candidates],packet=g))
                reason=('unmatched_context' if e[2].startswith('unmatched:') else
                        'unbound_target' if e[0].startswith('unbound:') else
                        'wrong_role' if nodes[e[2]]['role']!=e[1] else 'wrong_target')
                fps.append(dict(scored_edge=e,reason=reason,origins=for_group))
            oracle,pairs=audit_pairs(item,outputs[iid],d,s['missing_edges'])
            documents.append(dict(id=iid,panel=d['panel'],difficulty=d['difficulty'],availability=d['availability'],
                baseline_target_trials=target_trials,baseline_role_trials=baseline_repairs,source_text=source['text'],source_id=source['id'],raw=raw,storage_status=graph['status'],
                storage_diagnostics=graph['diagnostics'],reader_packets=packets,edges=edges,
                incorrect=fps,oracles=oracle,pair_decisions=pairs))
    assert len(documents)==68 and sum(len(x['incorrect']) for x in documents)==26
    assert sum(len(x['pair_decisions']) for x in documents)==1192
    assert sum(len(x['edges']) for x in documents)==129
    assert sum(e['first_loss']=='retained' for x in documents for e in x['edges'])==44
    assert all(o['origins'] and all(g['raw_row_ids'] for g in o['origins']) for x in documents for o in x['incorrect'])
    OUT.mkdir(exist_ok=True)
    (OUT/'audit.json').write_text(json.dumps(documents,ensure_ascii=False,indent=2)+'\n')
    for panel in ('natural_audit','balanced_synthetic'):
        subset=[x for x in documents if x['panel']==panel]
        for key in ('gold_context_only','gold_target_span_only','target_only','role_only'):
            wins=[(x['id'],o['edge']) for x in subset for o in x['oracles'] if o[key] and o['baseline_missing']]
            print(panel,key,len(wins),sorted({i for i,e in wins}))
        print(panel,Counter(e['first_loss'] for x in subset for e in x['edges']))

if __name__=='__main__':
    main()
