"""One-call direct baseline on the identical answering port and citation schema."""
import json
from typing import Literal

from llama_index.core.llms import ChatMessage
from pydantic import BaseModel

from team_memory.readers.attribution import AttributedQA
from team_memory.readers.scoped import CitedFact, ScopedDraft
from evaluation.answering_port.live_versions import main


class DirectAnswer(BaseModel):
    claims: list[CitedFact]
    outcome: Literal['answered', 'conditional', 'abstained']
    reason: str


class DirectQA(AttributedQA):
    def generate_scoped(self, query, evidence):
        fields = ('id','kind','conditions','quote','speaker','observed_at')
        context = [{key:item[key] for key in fields} for item in evidence]
        prompt = ("Answer the question from the supplied evidence. Give each applicable condition's answer with "
                  "its evidence_id and exact substring_quote. Use answered if the same answer applies, "
                  "conditional if the answer depends on the condition, or abstained with no claims and a reason "
                  "if unsupported. Return JSON matching this schema:\n" + json.dumps(DirectAnswer.model_json_schema()))
        messages = [ChatMessage(role='system',content=prompt),ChatMessage(role='user',content=json.dumps(
                    dict(query=query,evidence=context),ensure_ascii=False))]
        result = DirectAnswer.model_validate_json(self.llm.chat(messages,response_format={'type':'json_object'}).message.content)
        if (result.outcome == 'abstained') != (not result.claims):
            raise ValueError('Inconsistent direct answer')
        return ScopedDraft(claims=result.claims, comparison='', same_answer=result.outcome!='conditional', reason=result.reason)


if __name__=='__main__':
    main({'direct':DirectQA, 'scoped':AttributedQA})
