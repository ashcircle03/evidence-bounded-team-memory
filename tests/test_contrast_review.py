import json
import unittest
from tempfile import TemporaryDirectory
from pathlib import Path

from team_memory import contrast_review
from team_memory.evidence import FOLLOWUP
from team_memory.store import Store
from team_memory.sync import followups


class ContrastTest(unittest.TestCase):
    def test_label_bias_cancels_and_tie_abstains(self):
        class Model:
            def option_scores(self,s,x,count):
                choices=list(json.loads(x)["choices"].values())
                return [90*(i==0)+3*(v=="right") for i,v in enumerate(choices)]
        for items in (["other","right","none"],["right","other","none"]):
            i=contrast_review.choose(Model(),"prompt",{},items)
            self.assertEqual(items[i],"right")
        self.assertEqual(contrast_review.choose(Model(),"prompt",{},["left","middle","none"]),2)

    def test_full_record_vote_cannot_override_disagreeing_witnesses(self):
        def env(id,body):
            return {"source":{"location":id,"text":body,"speaker":"Sam"},"owner":"Sam"}
        class Reader:
            def option_scores(self,s,x,count):
                o=json.loads(x);choices=list(o["choices"].values())
                if s==contrast_review.MATCH:
                    wanted="Codec" if "\n\n" in o["incoming"] else contrast_review.NONE
                else:wanted="Codec"
                return [3*int(wanted in c) for c in choices]
            def __call__(self,*args):raise AssertionError("No explanation after conflicting votes")
        r=contrast_review.assess({"p":(env("p","Codec choice."),"accepted")},"q",env("q","Report.\n\nCodec results."),"goal",Reader())
        self.assertEqual(r["action"],"keep")

    def test_alternative_must_resolve_to_its_own_source(self):
        with TemporaryDirectory() as tmp:
            store=Store(Path(tmp));w=[]
            for i in range(3):
                txt=f"decision {i}";src=dict(text=txt,location=str(i),speaker="Lee")
                key=store.put("sources",dict(source=src,owner="Lee",observed_at=f"2020-01-0{1+i}T00:00:00Z"))
                w.append(dict(source_id=key,location=str(i),speaker="Lee",quote=txt,start=0,end=len(txt)))
            p=dict(previous=w[0],incoming=w[2],alternative=w[1],action="reassess",reviewer="Lee",next_step=FOLLOWUP["REASSESS"])
            store.put("followups",p)
            store.put("followups",dict(p,alternative=dict(w[1],quote="false")))
            self.assertEqual(len(followups(store)),1)
