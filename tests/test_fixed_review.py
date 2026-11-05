import json
import unittest

from team_memory.evidence import Passage
from team_memory.fixed_review import CHANGE, SEPARATE, adjudicate
from team_memory.pair_selection import Comparison


class FixedReviewTest(unittest.TestCase):
    def test_one_document_order_can_vote_against_review(self):
        old=Passage("a","r/old","Lee",0,"Skip updates during branch creation.","rejected")
        new=Passage("b","r/new","Kim",0,"The initial checkout still needs updates. Other checks cost less.","source_only")
        pair=Comparison(old,new,-9.0,2.0)
        calls=[]
        def reader(prompt,content):
            self.assertEqual(json.loads(content)["selected_report_sentence"],"The initial checkout still needs updates.")
            return "During the initial checkout the prior optimization must update the tree."
        def margin(prompt,content):
            doc=json.loads(content)
            if prompt in (CHANGE,SEPARATE):
                calls.append((prompt,list(doc)[1]))
                if prompt==SEPARATE:return 0
                return 4 if list(doc)[1]=="EARLIER" else -1
            return int("initial checkout" in doc["REPORT"])
        reader.evidence_margin=margin
        history={"a":({"owner":"Lee"},"rejected")}
        normal=adjudicate(pair,history,"review",reader)
        self.assertEqual(normal,adjudicate(pair,history,"review",reader,report_first=True))
        self.assertEqual(len(calls),8)
        self.assertEqual(normal["previous"],old.cite())
        self.assertEqual(normal["reviewer"],"Lee")
        self.assertEqual(normal["incoming"],new.cite())

    def test_ambiguous_relation_skips_the_explainer(self):
        past=Passage("a","a","Lee",0,"An old report.","accepted")
        new=Passage("b","b","Kim",0,"A new report.","source_only")
        def reader(*args):self.fail("no review should be drafted")
        reader.evidence_margin=lambda *args:2
        self.assertEqual(adjudicate(Comparison(past,new,9,9),{},"goal",reader)["action"],"keep")
