"""Load the optional experimental checkpoint in the Aurora model environment."""
import json
from pathlib import Path

import torch
from transformers import AutoTokenizer

from evaluation.record_binding.discourse.run import ENCODER, LABELS, RelationModel, record_input


def load_predictor(checkpoint):
    checkpoint=Path(checkpoint)
    model=RelationModel()
    model.load_state_dict(torch.load(checkpoint/'weights.pt',map_location='cpu',weights_only=True))
    device='cuda' if torch.cuda.is_available() else 'cpu'
    model.to(device).eval()
    tokenizer=AutoTokenizer.from_pretrained(ENCODER,local_files_only=True)
    calibration=json.loads((checkpoint/'calibration.json').read_text())

    @torch.inference_mode()
    def predict(pairs):
        decisions=[]
        for start in range(0,len(pairs),32):
            body,context=zip(*(record_input(p) for p in pairs[start:start+32]))
            tokens=tokenizer(list(body)+list(context),max_length=128,padding=True,truncation=True,return_tensors='pt').to(device)
            for probs in model(tokens).softmax(1).tolist():
                label=LABELS[max(range(len(probs)),key=probs.__getitem__)]
                threshold=calibration.get(label,{}).get('threshold')
                decisions.append(label if threshold is not None and max(probs)>=threshold else 'keep')
        return decisions
    return predict
