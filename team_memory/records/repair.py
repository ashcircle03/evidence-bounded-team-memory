"""Opt-in deterministic repair of condition spans the model mislabels.

Public development analysis (2026-11-22, job 125239): of the 20 missed conditions,
11 had the antecedent ("If ...") stored as a claim span and 7 had the consequent
claim start with "then" or end with a citation, so it reached outside the
consequent. Rules read only the original text. Every span stays an exact source
substring, keeps its group, and no new group or claim is invented.

  1. split   a claim "If A, (then) B"  ->  condition "If A" + claim "B"
  2. relabel a claim that is only an antecedent ("If A"), when its group has
             another claim  ->  condition
  3. split   a claim "B if A" (antecedent at the end)  ->  claim "B" + condition "if A"
  4. trim    claims: leading "then"/"so"/"thus", trailing citation "[ 9 ]" and
             punctuation; conditions: trailing comma or "then"
"""
import re

_COND = r'(?:if|unless|when|whenever|once|provided that|in case|as long as)'
_LEADING_COND = re.compile(rf'\s*{_COND}\b', re.I)
_TRAILING_COND = re.compile(rf'\s{_COND}\b', re.I)
_LEADING_CONNECTIVE = re.compile(r'\s*(?:and then|then|so|thus|hence)\b[\s,]*', re.I)
_TRAILING_NOISE = re.compile(r'(?:\s*\[\s*[\w.,\s-]{1,12}\]|\s*[.;:,])+\s*$')
_CONDITION_TAIL = re.compile(r'(?:\s*,|\s+then)+\s*$', re.I)
_THEN = re.compile(r'then\b\s*', re.I)


def _strip(text, start, end):
    while start < end and text[start].isspace():
        start += 1
    while end > start and text[end - 1].isspace():
        end -= 1
    return start, end


def _top_level_commas(segment):
    """Comma offsets outside quotes and brackets."""
    depth, quoted, found = 0, False, []
    for i, ch in enumerate(segment):
        if ch in '"“”':
            quoted = not quoted
        elif ch in '([{':
            depth += 1
        elif ch in ')]}':
            depth = max(0, depth - 1)
        elif ch == ',' and not quoted and not depth:
            found.append(i)
    return found


def _with(span, role, start, end):
    result = dict(span, role=role, start=start, end=end)
    if role != 'claim':
        result['stance'] = 'unknown'
    return result


def _trim_claim(text, span):
    s, e = span['start'], span['end']
    m = _LEADING_CONNECTIVE.match(text, s, e)
    if m and m.end() < e:
        s = m.end()
    m = _TRAILING_NOISE.search(text[s:e])
    if m and m.start() > 0:
        e = s + m.start()
    s, e = _strip(text, s, e)
    return dict(span, start=s, end=e) if s < e else span


def _trim_condition(text, span):
    s, e = span['start'], span['end']
    m = _CONDITION_TAIL.search(text[s:e])
    if m and m.start() > 0:
        e = s + m.start()
    s, e = _strip(text, s, e)
    return dict(span, start=s, end=e) if s < e else span


def _split_leading(text, span):
    """'If A, (then) B' -> (condition A, claim B) or None."""
    s, e = span['start'], span['end']
    segment = text[s:e]
    if not _LEADING_COND.match(segment):
        return None
    for comma in _top_level_commas(segment):
        rest = s + comma + 1
        m = _THEN.match(text, rest + len(text[rest:e]) - len(text[rest:e].lstrip()))
        claim_start = m.end() if m else rest
        cs, ce = _strip(text, s, s + comma)
        bs, be = _strip(text, claim_start, e)
        if cs < ce and bs < be and len(text[bs:be].split()) >= 2 and not _LEADING_COND.match(text[bs:be]):
            return _with(span, 'condition', cs, ce), _with(span, 'claim', bs, be)
    return None


def _split_trailing(text, span):
    """'B if A' -> (claim B, condition 'if A') or None."""
    s, e = span['start'], span['end']
    m = _TRAILING_COND.search(text, s, e)
    if not m:
        return None
    bs, be = _strip(text, s, m.start())
    cs, ce = _strip(text, m.start(), e)
    if len(text[bs:be].split()) < 2 or cs >= ce:
        return None
    return _with(span, 'claim', bs, be), _with(span, 'condition', cs, ce)


def repair_spans(text, spans):
    """Aligned spans ({role, group, stance, start, end, ...}) -> repaired spans."""
    claims_per_group = {}
    for span in spans:
        if span['role'] == 'claim':
            claims_per_group[span['group']] = claims_per_group.get(span['group'], 0) + 1
    out = []
    for span in spans:
        if span['role'] != 'claim':
            out.append(_trim_condition(text, span) if span['role'] == 'condition' else span)
            continue
        parts = _split_leading(text, span)
        if parts is None and _LEADING_COND.match(text, span['start'], span['end']) \
                and claims_per_group[span['group']] > 1:
            out.append(_trim_condition(text, _with(span, 'condition', span['start'], span['end'])))
            continue
        if parts is None:
            parts = _split_trailing(text, span)
        if parts is None:
            out.append(_trim_claim(text, span))
            continue
        for part in parts:
            out.append(_trim_claim(text, part) if part['role'] == 'claim' else _trim_condition(text, part))
    # Never leave a group without a claim: undo a relabel that removed its last claim.
    rooted = {s['group'] for s in out if s['role'] == 'claim'}
    if all(g in rooted for g in claims_per_group):
        return out
    return [s for s in spans]
