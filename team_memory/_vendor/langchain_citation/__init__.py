"""Adapted schema from LangChain 0.3.27 citation_fuzzy_match (MIT).

Keep upstream fact/substring_quote schema. The adapter preserves an existing
answer and requires exact quotes instead of the original fuzzy regex matching.
"""
from pydantic import BaseModel, Field


class FactWithEvidence(BaseModel):
    fact: str = Field(..., description="Body of the sentence, as part of a response")
    substring_quote: list[str] = Field(..., description=(
        "Each source should be a direct quote from the context, "
        "as a substring of the original content"))


class QuestionAnswer(BaseModel):
    question: str
    answer: list[FactWithEvidence]
