"""Adapted from LongMemEval DenseRetrievalMaster's flat-contriever branch.

Copyright (c) 2024 Di Wu. MIT; see LICENSE and NOTICE.md.
Same masked mean pooling, unnormalized inner product and descending ranking.
Cache corpus embeddings once; explicit local snapshot and configurable batch.
"""
import torch
from transformers import AutoModel, AutoTokenizer


def mean_pooling(token_embeddings, mask):
    token_embeddings = token_embeddings.masked_fill(~mask[..., None].bool(), 0.)
    return token_embeddings.sum(dim=1) / mask.sum(dim=1)[..., None]


class Contriever:
    def __init__(self, model_path, *, device='cuda', batch_size=16):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
        self.model = AutoModel.from_pretrained(model_path, local_files_only=True).to(device).eval()
        self.batch_size = batch_size
        self.truncated = 0

    def encode(self, texts):
        vectors = []
        with torch.no_grad():
            for start in range(0, len(texts), self.batch_size):
                batch = texts[start:start+self.batch_size]
                lengths = self.tokenizer(batch, truncation=False, return_length=True)['length']
                self.truncated += sum(n > self.tokenizer.model_max_length for n in lengths)
                inputs = self.tokenizer(batch, padding=True, truncation=True, return_tensors='pt')
                inputs = {k:v.to(self.model.device) for k,v in inputs.items()}
                outputs = self.model(**inputs)
                vectors.append(mean_pooling(outputs[0], inputs['attention_mask']).detach().cpu())
        return torch.cat(vectors)

    def index(self, witnesses):
        self.witnesses = witnesses
        self.vectors = self.encode([w['quote'] for w in witnesses])

    def retrieve(self, query, top_k=8):
        scores = (self.encode([query]) @ self.vectors.T).squeeze(0)
        indices = scores.argsort(descending=True)[:top_k].tolist()
        return [self.witnesses[i] for i in indices]
