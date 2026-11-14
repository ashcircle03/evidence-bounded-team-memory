"""Decode model JSON and recover original offsets for rendered RST prose."""
import json
import re
from pathlib import PurePosixPath
from pydantic import ValidationError

from team_memory.readers.citations import quote_span


_FENCE = re.compile(r'^```(?:json)?\s*|\s*```$')
# Only paired, single-line inline literal markup. Skip escaped delimiters,
# fences, literal blocks, indented code and paragraphs containing directives.
_LITERAL = re.compile(r'(?<![\w\\`])``([^\s`](?:[^`\n]*?[^\s`])?)``(?![\w`])')


def parse_model_json(schema, raw):
    body = _FENCE.sub('', raw.strip())
    try:
        return schema.model_validate_json(body)
    except ValidationError as error:
        if not any(item["type"] == "json_invalid" for item in error.errors()):
            raise
        # A copied tab or line break is permitted inside a model string.
        # Keep the original payload for diagnostics and validate the same schema.
        if re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', body):
            raise
        try:
            value = json.loads(body, strict=False)
        except ValueError:
            raise error from None
        return schema.model_validate(value)


def locate_quote(quote, source):
    """Return original character offsets. Never return a normalized quote."""
    original = source['quote']
    span = quote_span(quote, original)
    if span is not None:
        return span
    if PurePosixPath(source['location'].split('#', 1)[0].split('?', 1)[0]).suffix.lower() != '.rst':
        return None
    if '`' in quote or not quote.strip():
        return None
    pattern = re.compile(r'\s+'.join(re.escape(word) for word in quote.split()))
    candidates = []
    for paragraph in re.finditer(r'[^\n]+(?:\n[^\n]+)*', original):
        text = paragraph.group()
        if any(line.startswith((' ', '\t', '.. ', '>>>', '|', '>')) for line in text.splitlines()):
            continue
        delimiters = set()
        for literal in _LITERAL.finditer(text):
            delimiters.update((literal.start(), literal.start()+1, literal.end()-2, literal.end()-1))
        if not delimiters:
            continue
        offsets = [i for i in range(len(text)) if i not in delimiters]
        rendered = ''.join(text[i] for i in offsets)
        for match in pattern.finditer(rendered):
            start, end = offsets[match.start()], offsets[match.end()-1]+1
            # Include paired markup when the quote starts or ends with the literal.
            while start-1 in delimiters:
                start -= 1
            while end in delimiters:
                end += 1
            candidates.append((paragraph.start()+start, paragraph.start()+end))
    return candidates[0] if len(candidates)==1 else None
