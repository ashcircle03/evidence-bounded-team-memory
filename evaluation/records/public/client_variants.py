"""The teammate's public-document records client (Slurm 124911), with selectable variants.

'default' is the original submission/client.py unchanged: preserving.construct with
the role predictor. The others change only the builder call:
  default    preserving.construct(..., predict=role predictor)            (as 124911)
  source     same, plus alignment='source'
  nopredict  preserving.construct(...) without the role predictor
  staged     staged.construct(...) two-stage builder (no role predictor support)
  repair         default + repair_conditions=True
  repair-source  default + repair_conditions=True + alignment='source'
  staged-repair  staged + repair_conditions=True
Select with RECORDS_VARIANT. Output rows keep the 124911 format, so the teammate's
score.sh scores them unchanged: {id, graph, calls: [{output, usage}]}.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json
import os
import subprocess

import httpx
from team_memory.records import grouped, preserving

VARIANTS = ('default', 'source', 'nopredict', 'staged', 'repair', 'repair-source', 'staged-repair')


def main():
    variant = os.environ.get('RECORDS_VARIANT', 'default')
    if variant not in VARIANTS:
        raise SystemExit(f'Unknown RECORDS_VARIANT {variant}; choose from {VARIANTS}')
    cfg = json.loads(Path("config.json").read_text())
    docs = json.loads(Path(os.environ["RECORD_INPUTS"]).read_text())["documents"]
    out = Path(cfg["project"])/"results"/("records-current-"+os.environ["SLURM_JOB_ID"]+".jsonl")
    (Path(cfg["project"])/"variant.json").write_text(json.dumps(dict(
        variant=variant, team_memory=str(Path(preserving.__file__).resolve()))))

    def work(doc):
        src = dict(doc, owner="public-corpus", speaker="unknown", observed_at=cfg["snapshot_at"],
                   location=doc["id"])
        calls = []

        def generator(extra_body):
            def generate(system, prompt):
                body = dict(model="Qwen3-8B", temperature=0, seed=42, max_tokens=2048,
                            chat_template_kwargs=dict(enable_thinking=False),
                            messages=[dict(role="system",content=system),dict(role="user",content=prompt)],
                            **extra_body)
                response = client.post(os.environ["PRACTICAL_MODEL_URL"]+"/chat/completions",json=body)
                response.raise_for_status()
                data = response.json()
                choice = data["choices"][0]
                answer = choice["message"]["content"]
                calls.append(dict(output=answer,usage=data["usage"],finish_reason=choice.get("finish_reason")))
                return answer
            return generate

        def predict(pairs):
            proc = subprocess.run([cfg["conda_prefix"]+"/bin/python", cfg["role_dir"]+"/role.py"],
                                  input=json.dumps([pairs]),text=True,capture_output=True,check=True,
                                  env={k:v for k,v in os.environ.items() if k!="PYTHONPATH"})
            return json.loads(proc.stdout)[0]

        generate = generator(grouped.writer_kwargs(basis_types=True)["extra_body"])
        extra = dict(source=dict(alignment='source'), repair=dict(repair_conditions=True),
                     **{'repair-source': dict(alignment='source', repair_conditions=True)})
        if variant in ('default', 'source', 'repair', 'repair-source'):
            result = preserving.construct(src, generate, model=cfg["model_revision"], predict=predict,
                                          training_counts={"disjoint":11974}, **extra.get(variant, {}))
        elif variant == 'nopredict':
            result = preserving.construct(src, generate, model=cfg["model_revision"])
        else:
            from team_memory.records import staged
            result = staged.construct(src, model=cfg["model_revision"], repair_conditions=variant == 'staged-repair',
                                      generate_claims=generator(staged.claims_writer_kwargs()["extra_body"]),
                                      generate_roles=generator(staged.roles_writer_kwargs()["extra_body"]))
        return dict(id=doc["id"],graph=result["record_graph"],calls=calls)

    with httpx.Client(trust_env=False,timeout=300) as client, ThreadPoolExecutor(4) as pool, out.open("x") as stream:
        for row in pool.map(work, docs):
            print(json.dumps(row,ensure_ascii=False),file=stream,flush=True)


if __name__=="__main__":
    main()
