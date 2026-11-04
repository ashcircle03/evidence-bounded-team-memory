"""Conservative comparison of evidence, independent of the writer's topic name."""
from difflib import SequenceMatcher
from functools import lru_cache
import re

TOKEN = re.compile(r"[^\W_]+", re.UNICODE)
# These cues can make a single event's different values mutually exclusive.
SINGLE = re.compile(r'\b(only|sole|exactly|exclusive|minimum required|final (?:decision|disposition)|single)\b', re.I)
BOUND = re.compile(r'\b(at least|at most|or more|or less|up to|roughly|approximately)\b', re.I)
NONASSERT = re.compile(r"\b(maybe|perhaps|might|possibly|if|could|should we)\b|\?", re.I)

@lru_cache(maxsize=8192)
def tokens(s):
    return tuple(TOKEN.findall(s.casefold()))

def frame(item):
    s = item["quote"].casefold()
    # Remove the claim value and recorded condition *values*, not new keywords invented by a model.
    val = item["value"].casefold()
    if not re.search(r'(?<!\w)' + re.escape(val) + r'(?!\w)', s):
        return ()
    s = re.sub(r'(?<!\w)' + re.escape(val) + r'(?!\w)', ' SLOT ', s)
    for v in sorted(item["scope"].values(), key=len, reverse=True):
        s = s.replace(v.casefold(), ' CONDITION ')
    return tokens(s)

def comparable(old, new):
    if old["quote"] == new["quote"] and old["value"].casefold() == new["value"].casefold():
        return True
    a,b = frame(old),frame(new)
    return bool(a and a == b and len(set(a)-{"slot","condition"}) >= 3)

def exclusive_difference(a, b):
    """Minimal contrasting spans in two otherwise identical single-value assertions.
    Return None on missing exclusivity, changed conditions, bounds, or speculative reports."""
    if not (SINGLE.search(a) and SINGLE.search(b)) or NONASSERT.search(a) or NONASSERT.search(b) or BOUND.search(a) or BOUND.search(b):
        return None
    ma,mb = list(TOKEN.finditer(a)),list(TOKEN.finditer(b))
    ta,tb = tokens(a),tokens(b)
    if min(len(ta),len(tb)) < 6: return None
    edits = [op for op in SequenceMatcher(None,ta,tb,autojunk=False).get_opcodes() if op[0] != 'equal']
    if len(edits) != 1: return None
    tag,i,j,k,l = edits[0]
    if tag != 'replace' or max(j-i,l-k)>6 or len(ta)-(j-i)<5: return None
    # A difference preceding the predicate often changes the subject or the scope.
    # Accept differences in the value slot only, following a predication.
    prefix = a[:ma[i].start()]
    if not re.search(r'\b(?:is|was|were|are|requires?|remains?|took|spent|lists?|names?)\s*(?:exactly\s*)?$', prefix, re.I):
        return None
    return [a[ma[i].start():ma[j-1].end()], b[mb[k].start():mb[l-1].end()]]

def merge_action(key, old, new, conditioned_action):
    explicit = new.get("corrects") == key
    aligned = comparable(old,new)
    diff = exclusive_difference(old["quote"],new["quote"])
    if not (explicit or aligned or diff):
        return None
    action = conditioned_action(key, old, new)
    if diff and action=='duplicate':
        return 'unresolved'  # A lossy identical writer summary cannot erase an explicit clash in the quotes.
    if action != "unresolved" or explicit:
        return action
    if BOUND.search(old['quote']) or BOUND.search(new['quote']):
        return 'needs_comparison'
    # Scoped, identically worded results can disagree; two repeated observations are not
    # proof either is false. No old record is overwritten. Weak comparisons never block QA.
    if aligned and any(re.search(r'\d',item['value']) for item in (old,new)) and not diff:
        return 'needs_comparison'  # Same configuration can produce different measured observations.
    if (aligned and old['scope'] and old['scope']==new['scope']) or diff:
        return 'unresolved'
    return 'needs_comparison'
