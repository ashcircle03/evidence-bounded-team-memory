"""One claim / span view over every stored annotation form: records.view/v1.

Readers otherwise handle records.graph v1-v4, the optional records.arguments/v1
layer and sources without any extraction separately. claims_view(source) reads
all of them into the same shape (spec 7, Records representation):

  {version, source_id, extraction_status, claims: [
     {id, origin, stance, qualification,
      claim / condition / basis / time / subject: [{start, end, quote}],
      assertions: [{stance, kind, spans}], arguments: [{predicate, role_question, argument}]}]}

Every span is [start, end) in Python code points with quote == text[start:end].
A source without record_graph gives extraction_status 'not_run' and its argument
predicates only. Stored records are validated first and never modified. This is
a read view, not a stored or exchanged contract type.
"""
from copy import deepcopy

from .graph import ROLES, validate_graph
from team_memory.storage.objects import digest

VERSION = 'records.view/v1'


def _span(text, start, end):
    return dict(start=start, end=end, quote=text[start:end])


def _graph_claims(source, graph):
    text = source['text']
    units = {u['id']: u for u in graph['units']}

    def spans(ids):
        return [_span(text, units[i]['start'], units[i]['end']) for i in ids]

    claims = []
    for c in graph['claims']:
        entry = dict(id=c['id'], origin=graph['version'], stance=c['stance'], qualification=c['qualification'],
                     **{role: spans(c[role]) for role in ROLES}, arguments=[])
        kinds = {a['unit_id']: a['kind'] for a in c.get('basis_annotations', [])}
        for span, uid in zip(entry['basis'], c['basis']):
            span['kind'] = kinds.get(uid, 'unspecified')
        if 'assertions' in c:
            entry['assertions'] = [dict(stance=a['stance'], kind=a['kind'], spans=spans(a['unit_ids']))
                                   for a in c['assertions']]
        else:
            entry['assertions'] = [dict(stance=c['stance'], kind='assertion', spans=spans(c['claim']))]
        claims.append(entry)
    # records.graph/v4: context bound directly to one assertion of a claim.
    for binding in graph.get('context_bindings', []):
        anchor = (binding['target_start'], binding['target_end'])
        for entry in claims:
            if any((a['spans'][0]['start'], a['spans'][-1]['end']) == anchor for a in entry['assertions']):
                span = _span(text, binding['context_start'], binding['context_end'])
                if binding['role'] == 'basis':
                    span['kind'] = binding['basis_kind']
                if all((s['start'], s['end']) != (span['start'], span['end']) for s in entry[binding['role']]):
                    entry[binding['role']].append(span)
    return claims


def _attach_arguments(source, claims, layer):
    """Predicate inside a claim span -> that claim; otherwise a predicate-only entry."""
    text = source['text']
    orphans = {}
    for link in layer['links']:
        p = link['predicate']
        owners = [c for c in claims if any(s['start'] <= p['start'] and p['end'] <= s['end'] for s in c['claim'])]
        for owner in owners:
            owner['arguments'].append(deepcopy(link))
        if not owners:
            orphans.setdefault((p['start'], p['end']), []).append(deepcopy(link))
    for (start, end), links in sorted(orphans.items()):
        predicate = _span(text, start, end)
        claims.append(dict(id='a:' + digest([source['id'], [start, end]]), origin=layer['version'],
                           stance='unknown', qualification=layer['qualification'],
                           claim=[predicate], **{role: [] for role in ROLES if role != 'claim'},
                           assertions=[dict(stance='unknown', kind='assertion', spans=[predicate])],
                           arguments=links))


def claims_view(source):
    graph = source.get('record_graph')
    layer = source.get('record_arguments')
    if graph is not None:
        validate_graph(source, graph)
    if layer is not None:
        from .arguments import validate_arguments
        validate_arguments(source)
    claims = _graph_claims(source, graph) if graph is not None else []
    if layer is not None:
        _attach_arguments(source, claims, layer)
    return dict(version=VERSION, source_id=source['id'],
                extraction_status=graph['status'] if graph is not None else 'not_run', claims=claims)
