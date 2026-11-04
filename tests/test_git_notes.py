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
