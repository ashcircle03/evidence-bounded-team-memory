import json
import sys
from base_run import PROJECT,ENCODER,LABELS,RelationModel,AutoTokenizer,record_input,torch

def main():
    torch.set_num_threads(2)
    ck=PROJECT/'checkpoints/record-discourse-124235'
    cal=json.loads((ck/'calibration.json').read_text())
    model=RelationModel()
    model.load_state_dict(torch.load(ck/'weights.pt',map_location='cpu',weights_only=True))
    model.eval()
    tok=AutoTokenizer.from_pretrained(ENCODER,local_files_only=True)
    batches=json.load(sys.stdin);out=[]
    with torch.inference_mode():
        for batch in batches:
            roles=[]
            for i in range(0,len(batch),32):
                a,b=zip(*(record_input(p) for p in batch[i:i+32]))
                inputs=tok(list(a)+list(b),padding=True,truncation=True,max_length=128,return_tensors='pt')
                for probs in model(inputs).softmax(1).tolist():
                    label=LABELS[max(range(len(probs)),key=probs.__getitem__)]
                    t=cal.get(label,{}).get('threshold')
                    roles.append(label if t is not None and max(probs)>=t else 'keep')
            out.append(roles)
    print(json.dumps(out))
if __name__=='__main__':main()
