"""Recover restrictive policy populations already anchored to a single assertion.

Pass a loaded en_core_web_sm parser. No dependency or model loading on the
default ingestion path. The original group, span and stance remain authoritative.
"""


def restriction(pair, parse):
    if pair['old_role'] != 'subject':
        return None
    context, target = pair['context'], pair['target']
    start = context['start'] - target['start']
    end = context['end'] - target['start']
    if start < 0 or end > len(target['text']):
        return None
    text = target['text']
    if text[start:end] != context['text']:
        raise ValueError('Policy subject is not aligned to its claim')
    doc = parse(text)
    span = doc.char_span(start, end)
    if span is None or any(t.text in {',', ';', '(', ')'} for t in span):
        return None
    subjects = [t for t in span if t.dep_ in {'nsubj', 'nsubjpass'} and
                not (span.start <= t.head.i < span.end)]
    if len(subjects) != 1:
        return None
    subject = subjects[0]
    predicate = subject.head
    if any(t.dep_ != 'punct' and not (span.start <= t.i < span.end) for t in subject.subtree):
        return None
    if not any(t.dep_ in {'det', 'predet'} and t.lower_ in {'all', 'each', 'every', 'any'}
               for t in subject.children):
        return None
    modals = [t for t in predicate.children if t.dep_ == 'aux' and t.lower_ in {'must', 'shall'}]
    modifiers = [t for t in subject.children if t.dep_ in {'acl', 'relcl'}]
    if len(modals) != 1 or len(modifiers) != 1:
        return None
    modifier = modifiers[0]
    # The stored population must contain the complete restriction, including
    # qualifiers and negation. Tokenizers can attach closing markup to the verb.
    if any(not (span.start <= t.i < span.end) for t in modifier.subtree):
        return None
    if any(t.dep_ != 'punct' and t != subject and subject not in t.ancestors for t in span):
        return None
    return dict(subject=subject.text, modifier=modifier.text, modal=modals[0].text,
                predicate=predicate.text, dependency=modifier.dep_)


def merge(decisions, restrictions):
    if len(restrictions) != len(decisions):
        raise ValueError('Missing role decisions')
    return ['condition' if d == 'keep' and trace else d
            for trace, d in zip(restrictions, decisions)]


def construct(source, generate, predict, training_counts, *, model, parse):
    from . import discourse_roles, discourse_scope

    def adapted(pairs):
        local = discourse_scope.sentence_pairs(source, pairs)
        decisions = discourse_scope.supported_decisions(local, predict(local), training_counts)
        return merge(decisions, [restriction(p, parse) for p in local])

    return discourse_roles.construct(source, generate, adapted, model=model)
