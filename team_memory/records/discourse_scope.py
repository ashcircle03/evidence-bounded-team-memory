"""Match the relation classifier's sentence channel and observed endpoint geometry."""
from copy import deepcopy
from nltk.tokenize import PunktTokenizer
from team_memory.records import preserving


def sentence_pairs(source, pairs):
    """Keep exact endpoints, including any overlap. Replace only the surrounding windows."""
    bounds=list(PunktTokenizer('english').span_tokenize(source['text']))
    result=deepcopy(pairs)
    for pair in result:
        for endpoint in (pair['context'],pair['target']):
            a,b=endpoint['start'],endpoint['end']
            assert source['text'][a:b]==endpoint['text']
            covering=[(lo,hi) for lo,hi in bounds if lo<b and a<hi]
            if not covering:
                raise ValueError('Missing containing sentence')
            endpoint['sentence']=source['text'][covering[0][0]:covering[-1][1]]
    return result


def geometry(pair):
    c,t=pair['context'],pair['target']
    if c['end']<=t['start'] or t['end']<=c['start']:
        return 'disjoint'
    if t['start']<=c['start'] and c['end']<=t['end']:
        return 'embedded'
    return 'partial_overlap'


def supported_decisions(pairs, decisions, training_counts):
    if len(pairs)!=len(decisions):
        raise ValueError('Missing relation decisions')
    return [decision if training_counts.get(geometry(pair),0)>0 else 'keep'
            for pair,decision in zip(pairs,decisions)]


def scoped_predictor(source, predict, training_counts, parse=None):
    """Adapt the model decision to its observed geometry and optional policy syntax."""
    def adapted(pairs):
        local = sentence_pairs(source, pairs)
        roles = supported_decisions(local, predict(local), training_counts)
        if parse is not None:
            from . import policy_scope
            roles = policy_scope.merge(roles, [policy_scope.restriction(p, parse) for p in local])
        return roles
    return adapted


def construct(source, generate, predict, training_counts, *, model):
    return preserving.construct(source, generate, predict=predict, training_counts=training_counts, model=model)
