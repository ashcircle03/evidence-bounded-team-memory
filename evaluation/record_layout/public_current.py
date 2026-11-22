"""Run the preserved Qwen records builder over public raw documents on Slurm."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json
import os
import subprocess

import httpx
from team_memory.records import grouped, preserving


def main():
    cfg = json.loads(Path("config.json").read_text())
    docs = json.loads(Path(os.environ["RECORD_INPUTS"]).read_text())["documents"]
    out = Path(cfg["project"])/"results"/("records-current-"+os.environ["SLURM_JOB_ID"]+".jsonl")
    def work(doc):
        src = dict(doc, owner="public-corpus", speaker="unknown", observed_at=cfg["snapshot_at"],
                   location=doc["id"])
        calls = []
        def generate(system, prompt):
            body = dict(model="Qwen3-8B", temperature=0, seed=42, max_tokens=2048,
                        chat_template_kwargs=dict(enable_thinking=False),
                        messages=[dict(role="system",content=system),dict(role="user",content=prompt)],
                        **grouped.writer_kwargs(basis_types=True)["extra_body"])
            response = client.post(os.environ["PRACTICAL_MODEL_URL"]+"/chat/completions",json=body)
            response.raise_for_status()
            data = response.json()
            answer = data["choices"][0]["message"]["content"]
            calls.append(dict(output=answer,usage=data["usage"]))
            return answer
        def predict(pairs):
            proc = subprocess.run([cfg["conda_prefix"]+"/bin/python", cfg["role_dir"]+"/role.py"],
                                  input=json.dumps([pairs]),text=True,capture_output=True,check=True,
                                  env={k:v for k,v in os.environ.items() if k!="PYTHONPATH"})
            return json.loads(proc.stdout)[0]
        result = preserving.construct(src, generate, model=cfg["model_revision"],predict=predict,
                                      training_counts={"disjoint":11974})
        return dict(id=doc["id"],graph=result["record_graph"],calls=calls)
    with httpx.Client(trust_env=False,timeout=300) as client, ThreadPoolExecutor(4) as pool, out.open("x") as stream:
        for row in pool.map(work, docs):
            print(json.dumps(row,ensure_ascii=False),file=stream,flush=True)


if __name__=="__main__":
    main()
