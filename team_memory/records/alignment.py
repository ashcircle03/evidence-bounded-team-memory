"""Opt-in source alignment: a quote is linked only when its position is unique.

The default LangExtract aligner matches whole whitespace tokens, ignores case
and silently takes the first match. That loses Korean nouns written without
their attached particle (초안 in 초안을) and binds a repeated sentence to its
first occurrence. This module keeps the exact-copy rule but searches the
original characters, preferring case-sensitive matches, and reports a repeat
instead of choosing one. Offsets are Python Unicode code points, [start, end).
"""
import re

MODE_TOKEN = 'token'    # historical LangExtract alignment (default)
MODE_SOURCE = 'source'  # this module
MODES = (MODE_TOKEN, MODE_SOURCE)
_TOKEN = re.compile(r"\w+(?:['’]\w+)*|[^\w\s]")


class Ambiguous(ValueError):
    """The quote occurs more than once; candidates are kept for later narrowing."""

    def __init__(self, message, candidates):
        super().__init__(message)
        self.candidates = candidates


def _ascii_word(c):
    return c.isascii() and c.isalnum()


def _inside_word(text, start, end):
    # v1 must not match inside v10, QA not inside QAT. Hangul may continue
    # (attached particles), so only ASCII letters and digits form a word here.
    before = start > 0 and _ascii_word(text[start - 1]) and _ascii_word(text[start])
    after = end < len(text) and _ascii_word(text[end - 1]) and _ascii_word(text[end])
    return before or after


def _matches(text, pattern, flags=0):
    return [(m.start(), m.end()) for m in re.finditer(pattern, text, flags)
            if m.end() > m.start() and not _inside_word(text, m.start(), m.end())]


def occurrences(text, quote):
    """Positions of quote in text, from the strictest search that finds any.

    1. exact characters, case-sensitive
    2. whitespace differences allowed (line breaks inside a sentence), case-sensitive
    3. whitespace differences allowed, case-insensitive (sentence-initial capitals)
    """
    words = quote.split()
    if not words:
        return []
    loose = r'\s+'.join(map(re.escape, words))
    # Tokenized sources put spaces around punctuation ("Success , then"); a model
    # copies "Success, then". Allow any spacing between word and punctuation tokens.
    tokens = _TOKEN.findall(quote)
    spaced = re.escape(tokens[0]) if tokens else ''
    for prev, tok in zip(tokens, tokens[1:]):
        # Two words still need whitespace between them; punctuation may attach.
        gap = r'\s+' if prev[-1].isalnum() and tok[0].isalnum() else r'\s*'
        spaced += gap + re.escape(tok)
    for pattern, flags in ((re.escape(quote), 0), (loose, 0), (spaced, 0),
                           (loose, re.IGNORECASE), (spaced, re.IGNORECASE)):
        found = _matches(text, pattern, flags)
        if found:
            return found
    return []


def locate(text, quote):
    """Return the unique (start, end) of quote, or raise.

    ValueError('Ungrounded extraction') when absent; Ambiguous when repeated.
    """
    found = occurrences(text, quote)
    if not found:
        raise ValueError('Ungrounded extraction')
    if len(found) > 1:
        raise Ambiguous('Ambiguous repeated span', found)
    return found[0]


def sentence_bounds(text):
    from nltk.tokenize import PunktTokenizer
    return list(PunktTokenizer('english').span_tokenize(text)) or [(0, len(text))]


def narrow(text, candidates, anchors, bounds=None):
    """Keep the one candidate inside the sentences its claim spans touch.

    anchors: (start, end) of the claim spans of the same group. Returns the
    single remaining candidate, or raises Ambiguous when zero or several remain.
    """
    bounds = sentence_bounds(text) if bounds is None else bounds
    touched = [(a, b) for a, b in bounds if any(max(a, s) < min(b, e) for s, e in anchors)]
    inside = [c for c in candidates if any(a <= c[0] and c[1] <= b for a, b in touched)]
    if len(inside) != 1:
        raise Ambiguous('Ambiguous repeated context span', candidates)
    return inside[0]
