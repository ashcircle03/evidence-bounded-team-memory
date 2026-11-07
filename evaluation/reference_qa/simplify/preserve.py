"""Replay the actual17 enrichment calls; check current code preserves20 outputs."""
from pathlib import Path
from types import SimpleNamespace
from hashlib import sha256
import json
from team_memory.reference_attributed import repair_omitted_answer
from team_memory.reference_quotes import add_quote_citations


def main():
    repo=Path(__file__).resolve().parents[3]
    previous=json.loads((repo/'results/reference-qa/parse-v1/cards.json').read_text())
    selected=json.loads((repo/'results/reference-qa/quote-normalized-v1/cards.json').read_text())
    calls=[json.loads(l) for l in (repo/'results/reference-qa/quote-normalized-v1/calls.jsonl').read_text().splitlines()]
    verified=[];used=[]
    for cid,card in previous.items():
        context=dict(case_id=card['case_id'],label=card['label'])
        class Replay:
            def chat(self,messages):
                actual=[dict(role=m.role.value,content=m.content) for m in messages]
                matches=[c for c in calls if c['context']==context and c['request']['messages']==actual]
                assert len(matches)==1,(cid,len(matches))
                c=matches[0];used.append(c['id'])
                return SimpleNamespace(message=SimpleNamespace(content=c['response']['choices'][0]['message']['content']))
        question=card['result']['alce']['question']
        current=add_quote_citations(question,repair_omitted_answer(question,card['result'],Replay()),Replay())
        expected=selected[cid]['result']
        assert current['raw']==expected['raw'] and current['answers']==expected['answers'],cid
        verified.append(cid)
    assert len(verified)==20 and len(used)==17
    out=repo/'results/reference-qa/simplify-v1';out.mkdir(exist_ok=True)
    (out/'preservation.json').write_text(json.dumps(dict(current_outputs_equal_selected=20,actual_prompt_matches=17,model_calls=0,gpu_minutes=0,cases=verified,call_ids=used,source_sha256={str(p.relative_to(repo)):sha256(p.read_bytes()).hexdigest() for p in [repo/'team_memory/reference_fallback.py',repo/'team_memory/reference_quotes.py',repo/'team_memory/reference_attributed.py']}),indent=2)+'\n')


if __name__=='__main__':main()
