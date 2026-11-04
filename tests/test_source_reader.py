import unittest

from team_memory.demo import run_followup
from team_memory.evidence import Passage, resolve_answer


class SourceReader(unittest.TestCase):
    def test_preserves_offsets_and_refuses_unsupported_second_answer(self):
        p = Passage("abc", "source/a", "writer", 10, "At least\n  ten days.", "pending")
        index = {"E1": p, "E2": p}
        (row,) = resolve_answer("E1 | at least ten days", index)["answers"]
        self.assertEqual(row["answer"], "At least\n  ten days")
        for bad in ["E1 | eleven", "E0 | ten", "E1 | ten\nE2 | days"]:
            self.assertEqual(resolve_answer(bad, index)["status"], "invalid_citation")

    def test_real_git_arrival_is_provisional_until_the_original_owner_reviews(self):
        run = run_followup()
        self.assertEqual(run["before_owner_review"]["status"], "pending")
        self.assertEqual(run["after_owner_review"]["status"], "approved_review")
        self.assertEqual(run["retained_source_count"], 2)
