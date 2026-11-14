"""Call the released CoMRAT commit analyzer unchanged, replacing only its UI.

No service import, new classifier, threshold tuning, model training or paid API.
Upstream: Dhaouadi/Oakes/Famelis, Zenodo 14176549, CC-BY-4.0.
"""
import asyncio
from contextlib import nullcontext
from hashlib import sha256
import importlib.util
import json
import os
from pathlib import Path
import sys
import time
from unittest.mock import patch


def main():
    packet = Path(sys.argv[1]).resolve()
    root = Path(sys.argv[2]).resolve()
    config = json.loads((packet / 'config.json').read_text())
    for name, digest in config['sha256'].items():
        assert sha256((packet / name).read_bytes()).hexdigest() == digest, name
    os.chdir(root)
    sys.path.insert(0, str(root))
    import pandas as pd
    import streamlit as st
    import tensorflow as tf
    tf.config.threading.set_intra_op_parallelism_threads(8)
    tf.config.threading.set_inter_op_parallelism_threads(2)
    for gpu in tf.config.list_physical_devices('GPU'):
        tf.config.experimental.set_memory_growth(gpu, True)
    spec = importlib.util.spec_from_file_location('upstream_commit', root / 'pages/commit.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # Cache unmodified released weights between documents, not predictions.
    models = module.load_models()
    documents = json.loads((packet / 'inputs.json').read_text())
    results = []
    started = time.monotonic()
    for document in documents:
        frames, messages, predictions = [], [], []

        def write(value):
            if isinstance(value, pd.DataFrame):
                frames.append(value.to_dict(orient='records'))
            else:
                messages.append(str(value))

        originals = [model.predict for model in models]

        def recorder(original, label):
            def predict(*args, **kwargs):
                value = original(*args, **kwargs)
                predictions.append({'label': label, 'probabilities': value.flatten().tolist(),
                                    'token_ids': args[0].tolist()})
                return value
            return predict

        with patch.object(st, 'header'), patch.object(st, 'text_area', return_value=document['text']), \
             patch.object(st, 'button', return_value=True), \
             patch.object(st, 'spinner', side_effect=lambda *a, **k: nullcontext()), \
             patch.object(st, 'write', side_effect=write), patch.object(st, 'error'), \
             patch.object(st, 'success'), patch.object(module, 'load_models', return_value=models), \
             patch.object(models[0], 'predict', side_effect=recorder(originals[0], 'Rationale')), \
             patch.object(models[1], 'predict', side_effect=recorder(originals[1], 'Decision')):
            asyncio.run(module.user_commit_page())
        assert len(frames) == 1 and len(predictions) == 2
        results.append(dict(id=document['id'], group=document['group'], input_text=document['text'],
                            rows=frames[0], raw_predictions=predictions, messages=messages))
        print('document_complete', document['id'], flush=True)
    result = dict(status='complete', job_id=os.environ['SLURM_JOB_ID'],
                  source_version=config['source_version'], input_sha256=config['sha256']['inputs.json'],
                  config_sha256=sha256((packet / 'config.json').read_bytes()).hexdigest(),
                  tensorflow=tf.__version__, devices=[str(x) for x in tf.config.list_physical_devices()],
                  inference_seconds=time.monotonic()-started, documents=results,
                  upstream_sha256={str(p.relative_to(root)):sha256(p.read_bytes()).hexdigest()
                                   for p in [root/'helpers.py', root/'pages/commit.py',
                                             root/'models/bi_lstm_model_decision.h5',
                                             root/'models/bi_lstm_model_rationale.h5',
                                             root/'data/dataset_3_labels_merged.csv']})
    destination = Path(config['project'])/'results'/('sm-'+os.environ['SLURM_JOB_ID']+'.json')
    temporary = destination.with_suffix('.tmp')
    temporary.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    temporary.replace(destination)


if __name__ == '__main__':
    main()
