"""Published DeBERTa NLI classifier; optional verification of ALCE candidates.

Uses the model card's AutoModelForSequenceClassification/argmax inference.
This smaller trained classifier substitutes for ALCE's T5-XXL AutoAIS model;
its predictions are not reported as AutoAIS scores or logical guarantees.
"""
class LocalNLIVerifier:
    def __init__(self, path, *, device='cuda', observe=None):
        import torch
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        self.torch=torch;self.device=device;self.observe=observe
        self.tokenizer=AutoTokenizer.from_pretrained(path,local_files_only=True,trust_remote_code=False)
        self.model=AutoModelForSequenceClassification.from_pretrained(path,local_files_only=True,
            trust_remote_code=False,use_safetensors=True).to(device).eval()
        assert self.model.config.id2label=={0:'contradiction',1:'entailment',2:'neutral'}

    def verify(self, passages, claim):
        answers=[]
        for start in range(0,len(passages),4):
            docs=passages[start:start+4]
            full=self.tokenizer(docs,[claim]*len(docs),truncation=False)
            batch=self.tokenizer(docs,[claim]*len(docs),padding=True,truncation='only_first',
                max_length=512,return_tensors='pt')
            with self.torch.inference_mode():
                probabilities=self.model(**batch.to(self.device)).logits.softmax(-1).cpu().tolist()
            for i,probs in enumerate(probabilities):
                ids=batch['input_ids'][i].cpu().tolist();mask=batch['attention_mask'][i].cpu().tolist()
                result=dict(passage=docs[i],claim=claim,probabilities=probs,
                    label=self.model.config.id2label[max(range(3),key=lambda k:probs[k])],
                    full_tokens=len(full['input_ids'][i]),input_ids=ids,attention_mask=mask,
                    truncated=len(full['input_ids'][i])>512)
                answers.append(result)
                if self.observe:self.observe(result)
        return answers
