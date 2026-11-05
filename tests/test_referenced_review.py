import unittest

from team_memory.referenced_review import assess, handles

A="deadbeef"*5
B="cafebabe"*5


def env(oid, text):
    return {"source":{"location":"https://git.example/repo/commit/"+oid,"text":text,"speaker":"Lee"},"owner":"Lee"}


class RefTest(unittest.TestCase):
    def test_direction_and_absent_target(self):
        self.assertEqual(handles("An index from deadbeef was cached."),set())
        self.assertEqual(handles("There was no regression in deadbeef."),set())
        text="Fix a regression introduced by deadbeef. On an empty request, the parser exits."
        self.assertEqual(handles(text),{"deadbeef"})
        self.assertEqual(assess({"x":(env(B,"A topic."),"accepted")},"r",env("c",text),"goal",None)["action"],"keep")

    def test_ambiguous_prefix_stays_open_for_manual_work(self):
        hist={"a":(env(A,"First"),"accepted"),"b":(env(A[:8]+"0"*32,"Second"),"accepted")}
        self.assertEqual(assess(hist,"r",env("c","A regression in deadbeef wiped the empty table."),"goal",None)["action"],"keep")

    def test_review_has_three_distinct_exact_witnesses_and_attribution(self):
        hist={"a":(env(A,"Cache decision\n\nCache parsed requests."),"rejected"),
              "b":(env(B,"Cache logs\n\nRotate logs every week."),"accepted")}
        new=env("c","Requests fail\n\nA regression in deadbeef (cache requests).\n\nEmpty requests trigger a parser exception.")
        class Reader:
            def __call__(self,*args):return "Empty requests fail during parsing."
            def option_scores(self,s,x,n):return list(range(n))
        r=assess(hist,"r",new,"goal",Reader())
        self.assertEqual(r["action"],"reassess")
        for key,source,doc in (("previous","a",hist["a"][0]),("incoming","r",new),("attribution","r",new),("alternative","b",hist["b"][0])):
            w=r[key];self.assertEqual(w["source_id"],source)
            self.assertEqual(w["quote"],doc["source"]["text"][w["start"]:w["end"]])
