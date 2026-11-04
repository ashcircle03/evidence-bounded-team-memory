from pathlib import Path
import tempfile
import unittest

from team_memory.demo import git
from team_memory.store import Store
from team_memory.sync import followups, pull, vote


class RawNotes(unittest.TestCase):
    def test_pull_detects_new_plain_note_and_owner_can_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            git(root, "init", "--bare", "--initial-branch=main", "origin.git")
            git(root, "clone", "origin.git", "writer")
            writer, reader = root / "writer", root / "reader"
            notes = writer / "notes"
            notes.mkdir()
            (notes / "decision.md").write_text("We rejected the cache because it gave no gain in the initial configuration.")
            git(writer, "add", "notes")
            git(writer, "-c", "user.name=Ana", "commit", "-m", "initial measurement")
            git(writer, "push", "origin", "HEAD:main")
            git(root, "clone", "origin.git", "reader")
            (notes / "report.md").write_text("In a sparse configuration we measured the cache. Hits improved from 20 to 70.")
            git(writer, "add", "notes")
            git(writer, "-c", "user.name=Ben", "commit", "-m", "share a result")
            git(writer, "push", "origin", "HEAD:main")
            store = Store(reader / "state")
            run = lambda: pull(store, "Improve hits", lambda *_: "RETEST | P1 | N1 | The sparse workload changes the earlier comparison.", "premise", "notes")
            result = run()
            row, = result["proposals"]
            self.assertEqual(row["reviewer"], "Ana")
            self.assertEqual(row["incoming"]["speaker"], "Ben")
            self.assertIn("no gain", row["prior_rationale"]["quote"])
            self.assertEqual(row["status"], "pending")
            with self.assertRaises(ValueError):
                vote(store, row["id"], row["id"], "Ben", "approve")
            self.assertFalse(run()["arrivals"])
            vote(store, row["id"], row["id"], "Ana", "approve")
            self.assertEqual(followups(store)[0]["status"], "approved_review")
            self.assertEqual(len(store.load("sources")), 2)

    def test_retired_claim_is_historical_review_evidence_only(self):
        import json
        from team_memory.demo import sample
        from team_memory.evidence import active_sources
        from team_memory.merge import replay, review, submit
        from team_memory.store import capture
        from team_memory.sync import assess_arrivals

        for status in ("rejected", "superseded"):
            with self.subTest(status=status), tempfile.TemporaryDirectory() as tmp:
                store = Store(Path(tmp))
                old = submit(store, sample(1,"Ada","low","standard"))
                review(store,old["id"],old["proposal"],"Ada","reject" if status=="rejected" else "approve")
                if status=="superseded":
                    updated = submit(store,sample(2,"Ada","revised","standard",corrects=old["id"]))
                    review(store,updated["id"],updated["proposal"],"Ada","approve")
                old_loc = old["record"]["source"]["location"]
                src = active_sources(store,include_retired=True)
                old_id = next(k for k,(e,_) in src.items() if e["source"]["location"]==old_loc)
                # Reproduce a legacy checkout retaining only the structured original.
                (store.root/"sources"/(old_id+".json")).unlink()
                env = sample(3,"Ben","improved","sparse")
                env["source"]["text"] = "다중 클래스 sparse 조건의 측정 결과가 개선됐다. In the sparse configuration we measured accuracy increasing from 30 to 45."
                new = capture(store,env)
                def reader(_,content):
                    payload=json.loads(content)
                    source=next(s for s in payload["previous"] if s["source"]==old_loc)
                    self.assertEqual(source["historical_status"],status)
                    return "RETEST | "+next(iter(source["excerpts"]))+" | N1 | The sparse observation warrants comparison."
                proposal,=assess_arrivals(store,[new],"Try comparisons",reader,"premise")
                self.assertEqual(proposal["result"]["action"],"retest")
                self.assertEqual(followups(store)[0]["previous"]["status"],status)
                self.assertEqual(replay(store)[old["id"]]["status"],status)
                self.assertNotIn(old_id,active_sources(store))
