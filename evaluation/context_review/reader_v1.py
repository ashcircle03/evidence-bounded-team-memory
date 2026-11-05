"""Fixed questions and extraction format across all context interventions."""
import json
from team_memory.evidence import QA, Passage, prompt_rows, resolve_answer
from team_memory.referenced_review import REASON

QUESTIONS = {
    'failure': 'What concrete failure did the reported operation exhibit: the actual error, output, return value, or inability to complete? Quote the observed failure, not a statement that a regression is fixed or a proposed repair.',
    'condition': 'Under what input or execution condition does that reported failure occur? Include the limiting conditions given in the report.',
}

def read_context(base, witnesses, generate):
    index = {f'E{i}': Passage(w['source_id'],w['location'],w['speaker'],w['start'],w['quote'],w['status'])
             for i,w in enumerate(witnesses,1)}
    result = {}
    for field, question in QUESTIONS.items():
        content = json.dumps(dict(question=question, report=base['incoming']['location'],
            focus=base['incoming']['quote'], evidence=prompt_rows(index)),ensure_ascii=False)
        raw = generate(QA, content)
        result[field] = dict(raw=raw, parsed=resolve_answer(raw,index))
    context = dict(earlier=base['previous']['quote'], incoming=prompt_rows(index),
                   report=base['incoming']['location'],focus=base['incoming']['quote'])
    result['rationale'] = generate(REASON,json.dumps(context,ensure_ascii=False))
    return result
