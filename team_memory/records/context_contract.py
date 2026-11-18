"""Typed context edges must have a distinct source and target assertion.

This is a structural contract over source intervals, not a semantic validator.
No second model call, keyword rules, label lookup, or claim rewriting.
"""
import json
from . import anchored_binding, preserving


def bind(source, original_raw, reply, *, model):
    roots = {}
    try:
        for row in json.loads(original_raw)['extractions']:
            if 'claim' in row:
                group = row['claim_attributes']['claim_group']
                # Existing preserving v3 contract: first assertion is the root.
                if group not in roots:
                    roots[group] = preserving._aligned_span(source, row)
        parsed = json.loads(reply)
        import jsonschema
        jsonschema.validate(parsed, anchored_binding.schema(roots))
    except Exception:
        return anchored_binding.bind(source, original_raw, reply, model=model)
    keep = []; rejected = []
    for index, link in enumerate(parsed['links']):
        try:
            span = preserving._aligned_span(source, anchored_binding._row(link['role'], link['quote'], link['target']))
            root = roots[link['target']]
            if span['start'] <= root['start'] and root['end'] <= span['end']:
                rejected.append(dict(index=index, reason='Context contains its complete target root assertion',
                                     link=link, context_span=span, root_span=root))
                continue
        except Exception:
            pass  # The existing grounding/schema validator records this error.
        keep.append(link)
    graph, trace = anchored_binding.bind(source, original_raw, json.dumps(dict(links=keep), ensure_ascii=False), model=model)
    trace.update(endpoint_rejections=rejected, original_reply=reply,
                 endpoint_policy='context_cannot_contain_complete_target_root')
    return graph, trace
