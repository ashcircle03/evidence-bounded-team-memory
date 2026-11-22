"""Reorder the first five RRF hits using the previous and central transcript turns."""
from collections import defaultdict
from functools import lru_cache
import os
import re


MODEL = 'cross-encoder/ms-marco-MiniLM-L-6-v2'
REVISION = '233902d25c440f23af6f7d6e94d2946bac0bee0a'


def turn_key(location):
    # Explicit transcript anchors and the existing QMSum meeting/turn locations.
    match = re.fullmatch(r'(.+)#turn=(\d+)', location) or re.fullmatch(r'(meeting-\d+)-(\d+)', location)
    if match:
        return match[1], int(match[2])


@lru_cache(maxsize=1)
def encoder(path):
    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    options = dict(local_files_only=True, revision=REVISION)
    return (AutoTokenizer.from_pretrained(path, **options),
            AutoModelForSequenceClassification.from_pretrained(path, **options).eval())


def previous_turn_order(question, nodes, sources):
    head = nodes[:5]
    if len(head) < 2:
        return nodes
    central = [sources[item.node.metadata['source_id']]['source'] for item in head]
    keys = [turn_key(s['location']) for s in central]
    if not any(keys):
        return nodes

    turns = defaultdict(list)
    for envelope in sources.values():
        source = envelope['source']
        key = turn_key(source['location'])
        if key:
            turns[key].append(source)

    tokenizer, model = encoder(os.environ.get('TEAM_MEMORY_RERANKER_PATH') or MODEL)
    import torch

    def tokens(source):
        text = source['text']
        if '#turn=' in source['location']:
            text = source['speaker'] + ' — ' + text
        return tokenizer.encode(text, add_special_tokens=False, verbose=False)

    limit = 512 - tokenizer.num_special_tokens_to_add(pair=True)
    query = tokenizer.encode(question, add_special_tokens=False, truncation=True, max_length=limit-1)
    budget = limit - len(query)
    batch = []
    for source, key in zip(central, keys):
        body = tokens(source)[:budget]
        space = budget - len(body)
        if key and space >= 2:
            previous = turns.get((key[0], key[1]-1), [])
            if len(previous) == 1:
                tail = tokens(previous[0])[-(space-1):]
                if tail:
                    body = tail + [tokenizer.sep_token_id] + body
        batch.append(tokenizer.prepare_for_model(query, body, add_special_tokens=True, return_attention_mask=True))
    with torch.inference_mode():
        scores = model(**tokenizer.pad(batch, return_tensors='pt')).logits[:, 0]
        if not torch.isfinite(scores).all():
            raise ValueError('Non-finite transcript reranking score')
    return [node for _, node in sorted(zip(scores.tolist(), head), key=lambda pair: pair[0], reverse=True)] + nodes[5:]
