"""Offline regression checks for packet alignment and scoring integrity."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('qa20_evaluate',ROOT/'evaluate.py')
ev=importlib.util.module_from_spec(spec);spec.loader.exec_module(ev)


class PacketTests(unittest.TestCase):
    def run_cli(self,*args,ok=True):
        p=subprocess.run([sys.executable,str(ROOT/'evaluate.py'),*map(str,args)],capture_output=True,text=True)
        self.assertEqual(p.returncode==0,ok,p.stderr)
        return p.stdout

    def test_packet_and_baseline(self):
        self.assertEqual(json.loads(self.run_cli('verify'))['questions'],20)
        score=json.loads(self.run_cli('score','--predictions',ROOT/'reference/checked-v1-predictions.jsonl',
                                     '--ratings',ROOT/'reference/checked-v1-ratings.json'))
        self.assertEqual(score['answer_and_required_citation'],19)
        self.assertEqual(score['invalid_original_citations'],[])
        self.assertEqual(len(score['known_extra_sentence_citation_gaps']),2)

    def test_requests_and_collection_preserve_pairing(self):
        inputs,questions=ev.verify()
        known={x['id']:x for x in ev.lines(ROOT/'reference/checked-v1-predictions.jsonl')}
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);requests=folder/'requests';responses=folder/'responses';responses.mkdir()
            self.run_cli('requests','--out',requests)
            for c in inputs['cases']:
                actual=ev.lines(requests/(c['id']+'.jsonl'))
                self.assertEqual(actual,[{k:v for k,v in e.items() if k!='label'} for e in c['events']])
                rows=[]
                for e in c['events']:
                    if e['operation']=='import_history':rows.append(dict(status='ok'));continue
                    x=known[c['id']+'/'+e['label']]
                    rows.append(dict(status=x['status'],raw=x['answer'],answers=[dict(text=x['answer'],evidence=x['citations'])]))
                (responses/(c['id']+'.jsonl')).write_text(''.join(json.dumps(x)+'\n' for x in rows))
            collected=[json.loads(x) for x in self.run_cli('collect','--responses',responses).splitlines()]
            self.assertEqual(collected,list(known.values()))
            self.run_cli('requests','--out',requests,ok=False)
            one=next(responses.glob('*.jsonl'));one.write_text('{}\n')
            self.run_cli('collect','--responses',responses,ok=False)

    def test_missing_duplicate_and_unrated_predictions_rejected(self):
        _,qs=ev.verify();pred=ev.lines(ROOT/'reference/checked-v1-predictions.jsonl')
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'pred.jsonl'
            for bad in [pred[:-1],pred[:-1]+pred[:1]]:
                path.write_text(''.join(json.dumps(x)+'\n' for x in bad))
                with self.assertRaises(ValueError):ev.predictions(path,qs)
            path.write_bytes((ROOT/'reference/checked-v1-predictions.jsonl').read_bytes())
            rating=Path(tmp)/'ratings.json';rating.write_text(self.run_cli('ratings','--predictions',path))
            self.run_cli('score','--predictions',path,'--ratings',rating,ok=False)

    def test_corrupted_quote_cannot_keep_passing_with_old_rating(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);pred=ev.lines(ROOT/'reference/checked-v1-predictions.jsonl')
            pred[0]['citations'][0]['quote']='not in this original'
            path=folder/'predictions.jsonl';path.write_text(''.join(json.dumps(x)+'\n' for x in pred))
            old=ROOT/'reference/checked-v1-ratings.json'
            self.run_cli('score','--predictions',path,'--ratings',old,ok=False)
            ratings=ev.read(old);ratings['predictions_sha256']=ev.sha256(path.read_bytes()).hexdigest()
            r=folder/'ratings.json';r.write_text(json.dumps(ratings))
            score=json.loads(self.run_cli('score','--predictions',path,'--ratings',r))
            self.assertEqual(score['answer_and_required_citation'],18)
            self.assertEqual(score['invalid_original_citations'][0]['id'],pred[0]['id'])


if __name__=='__main__':unittest.main()
