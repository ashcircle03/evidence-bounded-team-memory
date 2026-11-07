"""AQA conflict-aware demonstration + ALCE post-hoc citation adapters.

AQA: Shaier et al., EMNLP2024, section3.4.1 / appendixA.1 / figure1.
ALCE: Princeton-NLP, MIT, pinned in _vendor/alce. This is a Qwen adaptation,
not a reproduction of either paper's reported model/benchmark performance.
"""
from copy import deepcopy
import re

from llama_index.core.llms import ChatMessage
from nltk.tokenize import PunktTokenizer
from ._vendor.alce.searcher import SearcherWithinDocs
from .reference_checked import ConflictCheckedQA, missing_opposing_sources
from .reference_qa import format_response


# Paraphrase of AQA figure1, disjoint from the evaluated Git/PEP/chat questions.
# It deliberately represents conflicting source records, not current world facts.
AQA_EXAMPLE = '''Example question: Who holds the US presidency?
Document A: The record identifies Barack Obama as the serving president.
Document B: This record identifies Joseph Robinette Biden Jr. as the serving president.
Example answer: Document A identifies Barack Obama; Document B identifies Joseph Robinette Biden Jr.'''


def aqa_messages(question, witnesses):
    context='\n\n'.join(f"Source {i}:\nrecord_author: {w['speaker']}\n{w['quote']}"
                         for i,w in enumerate(witnesses,1))
    return [ChatMessage(role='user',content=f'''Answer the question using the supplied records. They may conflict. When they do, give the source-specific answers, following the example.
{AQA_EXAMPLE}

Question: {question}
Context:
{context}
Answer with the actual Source numbers in [N] citations:''')]


def repair_omitted_answer(question, result, llm):
    """Apply the same source-accounting trigger to every question, never a key."""
    missing=missing_opposing_sources(result)
    if not missing:return deepcopy(result)
    raw=llm.chat(aqa_messages(question,result['citation_sources'])).message.content
    candidate=format_response(question,raw,result['citation_sources'],allow_source_labels=True)
    old_ids={w['source_id'] for a in result['answers'] for w in a['evidence']}
    new_ids={w['source_id'] for a in candidate['answers'] for w in a['evidence']}
    # A source-accounting guard, not a semantic verifier. Never call evidence
    # coverage proof of answer correctness; the fixed20 source review tests that.
    accepted=candidate['status']=='ok' and old_ids.union(missing)<=new_ids
    out=candidate if accepted else deepcopy(result)
    for key in ('draft_raw','document_judgments','revised'):
        out[key]=result[key]
    out.update(aqa_candidate_raw=raw,aqa_candidate_accepted=accepted,
               pre_aqa_raw=result['raw'],missing_opposing_sources_before=missing)
    return out


def add_missing_citations(result, nli=None):
    """ALCE top1 TF-IDF attribution, with additive edits to preserve answer bytes.

    Existing citations are never replaced. This retrieves a candidate support
    passage; it is not an entailment test. Sentence-level source ratings remain
    a separate evaluation, as in ALCE.
    """
    out=deepcopy(result);raw=result['raw'];witnesses=result['citation_sources']
    if not raw or not witnesses:return out
    docs=[dict(title=w['location'],text=w['quote']) for w in witnesses]
    searcher=SearcherWithinDocs(docs,'tfidf',model=None,device='cpu')
    operations=[];reviews=[];unattributed=[]
    for start,end in PunktTokenizer('english').span_tokenize(raw):
        sentence=raw[start:end]
        if re.search(r'\[\d+\]|\bSource\s+\d+\b',sentence,re.IGNORECASE):continue
        if not re.search(r'[A-Za-z0-9]',sentence):continue
        number=int(searcher.search(sentence))+1
        if nli is not None:
            judgments=nli.verify([w['quote'] for w in witnesses],sentence)
            supported=[i for i,j in enumerate(judgments) if j['label']=='entailment']
            reviews.append(dict(start=start,end=end,sentence=sentence,tfidf_number=number,
                judgments=[{k:v for k,v in j.items() if k not in ('passage','claim','input_ids','attention_mask')}
                           for j in judgments]))
            if not supported:
                unattributed.append(dict(start=start,end=end,sentence=sentence))
                continue
            if number-1 not in supported:
                number=max(supported,key=lambda i:judgments[i]['probabilities'][1])+1
        operations.append(dict(start=start,end=end,sentence=sentence,number=number))
    new_raw=raw
    for op in reversed(operations):
        new_raw=new_raw[:op['start']]+f"[{op['number']}] "+new_raw[op['start']:]
    formatted=format_response(result['alce']['question'],new_raw,witnesses,allow_source_labels=True)
    out.update(formatted)
    out.update(pre_citation_raw=raw,posthoc_citations=operations,
        citation_method='ALCE post_hoc_cite top1 TF-IDF; additive, no overwrite',
        citation_entailment_verified=False)
    if nli is not None:
        out.update(citation_method='ALCE TF-IDF candidates with published DeBERTa NLI verification/reranking; additive, no overwrite',
            nli_citation_reviews=reviews,unattributed_sentences=unattributed,
            attribution_status='partial' if unattributed else 'complete',
            nli_prediction_is_not_proof=True)
    if result['status']=='partial':
        out['status']='partial'
        out['warnings']=list(dict.fromkeys(result['warnings']+out['warnings']))
    return out


def attribute_answer(question,result,llm,nli=None):
    return add_missing_citations(repair_omitted_answer(question,result,llm),nli)


class AttributedQA(ConflictCheckedQA):
    """AQA adapter and verified additive attribution; baseline stays selectable."""
    def __init__(self,store,*,nli,**kwargs):
        self.nli=nli
        super().__init__(store,**kwargs)

    def ask(self,question):
        with self.lock:
            result=super().ask(question)
            if not result.get('citation_sources'):return result
            return attribute_answer(question,result,self.llm,self.nli)
