"""Select a complete observation from nearby source paragraphs before proposing review."""
from . import contrast_review as contrast
from . import referenced_review
from .pair_selection import paragraphs

OBSERVATION = (
    'Which excerpt gives the observed incorrect behavior together with the conditions in which it occurs? '
    'Choose the concrete error, unexpected return/output, or failed operation, with enough context to '
    'identify its trigger. A statement that a commit fixes a regression, an isolated repair instruction, '
    'or an unfinished introduction to an error message is insufficient. '
    'If none of the excerpts states the failure and its trigger, choose insufficient evidence. Return the letter.'
)
NONE = 'Insufficient evidence of the actual incorrect behavior and its triggering condition.'


def observation_units(witnesses, sources):
    """Each unit is a literal paragraph plus its next included paragraph in the same record."""
    units = []
    for sid in dict.fromkeys(w['source_id'] for w in witnesses):
        text = sources[sid]['source']['text']
        spans = sorted((w for w in witnesses if w['source_id'] == sid), key=lambda w: w['start'])
        for index, w in enumerate(spans):
            if text[w['start']:w['end']] != w['quote']:
                raise ValueError('window does not resolve to the source')
            end = w['end']
            if index+1 < len(spans):
                following = spans[index+1]
                gap = text[end:following['start']]
                if following['start'] >= end and not gap.strip():
                    end = following['end']
            units.append(dict(w, end=end, quote=text[w['start']:end]))
    return units


def select_observation(witnesses, sources, generate):
    units = observation_units(witnesses, sources)
    winners = []
    # LocalChoice supports five labels. Keep abstention in every comparison, and
    # compare winners again when a long window needs more than one group.
    for start in range(0, len(units), 4):
        group = units[start:start+4]
        chosen = contrast.choose(generate, OBSERVATION, {}, [p['quote'] for p in group] + [NONE])
        if chosen < len(group):
            winners.append(group[chosen])
    if not winners:
        return None
    if len(winners) == 1:
        return winners[0]
    if len(winners) > 4:
        raise ValueError('observation window exceeds the supported limit')
    chosen = contrast.choose(generate, OBSERVATION, {}, [p['quote'] for p in winners] + [NONE])
    return winners[chosen] if chosen < len(winners) else None


def neighborhood(witness, envelope, radius=2):
    blocks = paragraphs(witness['source_id'], (envelope, 'source_only'))
    at = next((i for i, p in enumerate(blocks) if p.start == witness['start'] and p.quote == witness['quote']), None)
    if at is None:
        raise ValueError('selected report paragraph is missing')
    first = 1 if at > 0 else 0
    return [p.cite() for p in blocks[max(first, at-radius):at+radius+1]]


def render(previous, observation):
    return ('Reconsider the earlier decision “' + previous['quote'] +
            '”. The new report gives the following behavior and its conditions. “' + observation['quote'] + '”')


def revise(base, witnesses, sources, generate):
    if base.get('action') not in ('reassess', 'retest'):
        return base
    observation = select_observation(witnesses, sources, generate)
    if observation is None or observation['source_id'] != base['incoming']['source_id']:
        return dict(action='keep', basis='no supported observation with its condition in the report window')
    answer = dict(base, incoming=observation, report_anchor=base['incoming'],
                  observation_evidence=observation, rationale=render(base['previous'], observation))
    if 'alternative' in answer:
        answer['distinction'] = ('The alternative addresses “' + answer['alternative']['quote'] +
                                 '”. The reported observation is “' + observation['quote'] + '”.')
    return answer


def assess(previous, sid, incoming, goal, generate):
    base = referenced_review.assess(previous, sid, incoming, goal, generate)
    if base.get('action') not in ('reassess', 'retest'):
        return base
    return revise(base, neighborhood(base['incoming'], incoming), {sid: incoming}, generate)


def valid_evidence(item):
    observation = item.get('observation_evidence')
    if not isinstance(observation, dict) or observation != item.get('incoming'):
        return False
    return item.get('rationale') == render(item['previous'], observation)
