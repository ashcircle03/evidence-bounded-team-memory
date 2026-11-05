import unittest

from team_memory.pair_selection import assess, select, SUPPORT


def envelope(location,text):
    return {"owner":"member","observed_at":"2026-01-01T00:00:00Z",
            "source":{"speaker":"member","location":location,"text":text}}


class PairSelectionTest(unittest.TestCase):
    def test_reversal_returns_identical_decision_and_source_offsets(self):
        prior=envelope("notes/compression","Codec choice\n\nTiny payloads grew after compression.")
        other=envelope("notes/power","Power usage\n\nThe monitor was switched off.")
        incoming=envelope("notes/report","Trial results\n\nLarge payloads shrank in our comparison.")
        history={"a":(prior,"rejected"),"b":(other,"source_only")}
        def margin(instruction,content):
            self.assertFalse("Tiny payloads" in content and "monitor" in content)
            return 2 if "Tiny payloads" in content and "shrank" in content else -1
        def generate(s,c):return "Large payloads now warrant a separate comparison."
        generate.evidence_margin=margin
        r=assess(history,"c",incoming,"reduce bytes",generate)
        self.assertEqual(r,assess(dict(reversed(list(history.items()))),"c",incoming,"reduce bytes",generate))
        self.assertEqual(r["action"],"reassess")
        for key,doc in (("previous",prior),("incoming",incoming)):
            hit=r[key]
            self.assertEqual(doc["source"]["text"][hit["start"]:hit["end"]],hit["quote"])
        self.assertEqual(r["previous"]["status"],"rejected")

    def test_document_similarity_alone_does_not_request_review(self):
        past=envelope("notes/earlier","The existing measurements supported release.")
        new=envelope("notes/now","An engineer corrected the spelling in a release note.")
        def generate(s,c):
            raise AssertionError("should not compose a proposal")
        generate.evidence_margin=lambda s,c:-1 if s==SUPPORT else 2
        self.assertEqual(assess({"a":(past,"accepted")},"b",new,"quality",generate)["action"],"keep")

    def test_equal_scores_use_stable_source_and_offsets(self):
        a=envelope("A","A fact."); b=envelope("B","Another fact."); n=envelope("N","Report.")
        old={"z":(a,"accepted"),"b":(b,"accepted")}
        for hist in [old,dict(reversed(list(old.items())))]:
            self.assertEqual(select(hist,"n",n,"goal",lambda *_:1).old.sid,"b")
