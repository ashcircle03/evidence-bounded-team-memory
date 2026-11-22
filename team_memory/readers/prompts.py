"""Task adaptation of ConflictScore Table14 + upstream LlamaIndex citation prompts.

Reference: Liu et al., ConflictScore, arXiv:2606.26437v1, Appendix E Table14.
https://arxiv.org/html/2606.26437v1 (CC BY4.0).
The five balanced-generation instructions below are from Table14; the report
format is adapted to source QA. This is NOT ConflictScore's evaluator or R-RAG.
The separate record contract follows the caller's source-history requirements.
"""
from llama_index.core import PromptTemplate
from llama_index.core.query_engine.citation_query_engine import (
    CITATION_QA_TEMPLATE, CITATION_REFINE_TEMPLATE,
)

BALANCED_INSTRUCTIONS = '''Your goal is to synthesize the information from the documents while minimizing factual conflicts. To do this:
- Hedge appropriately when the evidence is partial, uncertain, or varies across documents. Use phrases like “some sources suggest,” “it is possible that,” “there is limited evidence,” or “while one document indicates…”.
- Avoid making definitive claims unless they are clearly and consistently supported across multiple documents.
- Do not speculate or infer beyond what is stated in the documents.
- Attribute information to the documents when relevant (e.g., “According to one article…” or “Document A notes that…”).
- Acknowledge conflicting viewpoints if they appear in the documents.
'''

RECORD_QA_CONTRACT = '''Answer the question about the supplied records, including their source metadata.
The record_author field identifies who wrote a record; an @mention in its text is not its author.
If records give incompatible answers under the same conditions, state that the records conflict and give each answer with its own source citation. Do not pick a winner using prior knowledge, a document's title, or recording time alone.
When conditions differ, state each answer with its condition; do not call different conditions a contradiction.
If the relevant records agree, answer directly. Unrelated disagreements do not prevent answering the question. Keep the answer concise and do not add an explanation beyond the evidence.
'''

TEAM_QA_TEMPLATE = PromptTemplate(BALANCED_INSTRUCTIONS + RECORD_QA_CONTRACT + '\n' +
                                 CITATION_QA_TEMPLATE.template)
TEAM_REFINE_TEMPLATE = PromptTemplate(BALANCED_INSTRUCTIONS + RECORD_QA_CONTRACT + '\n' +
                                     CITATION_REFINE_TEMPLATE.template)
