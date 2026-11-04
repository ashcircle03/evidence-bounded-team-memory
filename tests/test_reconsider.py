import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from team_memory.merge import review, submit
from team_memory.qa import answer
from team_memory.reconsider import prepare, proposal_inbox, reconsider, review_proposal, source_snapshot
from team_memory.store import Store, capture
from team_memory.writer import ingest


def source(who, text, day):
    return {"owner": who, "source": {"location": f"notes/{who}/{day}", "speaker": who, "text": text},
            "observed_at": f"2025-01-{day:02}T10:00:00Z"}


class Choices:
    identity = "contract-test"

    def __init__(self, *letters):
        self.letters = iter(letters)
        self.payloads = []

    def __call__(self, instruction, payload):
        self.payloads.append(json.loads(payload))
        return next(self.letters)


class DecisionReview(unittest.TestCase):
    old_text = "We deferred the queue for the small configuration because the old trial timed out."
    new_text = "In the large configuration, we measured the queue against the baseline. Latency dropped from 80 to 30 ms."

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.store = Store(Path(tmp.name))
        self.old = source("author", self.old_text, 1)
        self.new = source("member", self.new_text, 2)
        self.goal = "Select a queue for the release."

    def run_pair(self, letters=("A", "B")):
        capture(self.store, self.old)
        return reconsider(self.store, self.new, self.goal, Choices(*letters), limit=1)["assessments"][0]

    def test_masking_scope_and_immutable_evidence(self):
        capture(self.store, self.old)
        reader = Choices("A", "B")
        result = reconsider(self.store, self.new, self.goal, reader)
        before, after = reader.payloads
        self.assertIsNone(before["new_report"])
        self.assertEqual(after.pop("new_report"), self.new_text)
        before.pop("new_report")
        self.assertEqual(before, after)
        self.assertNotIn("80 to 30", json.dumps(before))
        row, = result["assessments"]
        self.assertEqual(row["action"], "request_comparison")
        self.assertEqual(row["comparison_scope"]["previous"]["quote"], self.old_text)
        self.assertIn("80 to 30", row["new_excerpt"]["quote"])
        self.assertEqual(proposal_inbox(self.store)[0]["status"], "pending")
        again = reconsider(self.store, self.new, self.goal, Choices())
        self.assertEqual(result, again)

    def test_constraint_and_already_running_have_distinct_actions(self):
        self.old["source"]["text"] += " The queue comparison is already underway."
        row = self.run_pair(("D", "D"))
        self.assertEqual(row["action"], "attach_to_existing")
        self.assertIn("underway", row["ongoing_work"]["quote"])
        self.assertFalse(proposal_inbox(self.store))

    def test_model_cannot_invent_ongoing_comparison(self):
        self.assertEqual(self.run_pair(("A", "D"))["action"], "needs_context")

    def test_independent_constraint(self):
        self.old["source"]["text"] += " The release policy requires a certified queue."
        self.assertEqual(self.run_pair(("C", "C"))["action"], "retain_constraint")
        self.assertFalse(proposal_inbox(self.store))

    def test_old_evidence_already_sufficient(self):
        self.assertEqual(self.run_pair(("B", "B"))["action"], "already_supported")
        self.assertFalse(proposal_inbox(self.store))

    def test_question_with_date_is_not_measurement(self):
        self.new["source"]["text"] = "2025-01-02: Should we try this queue configuration?"
        self.assertEqual(self.run_pair()["action"], "needs_context")

    def test_explicit_same_configuration_with_better_score(self):
        self.new["source"]["text"] = self.new_text.replace("large configuration", "small configuration")
        self.assertEqual(self.run_pair()["action"], "needs_context")
        self.assertFalse(proposal_inbox(self.store))

    def test_projected_numeric_gain_is_not_a_witness(self):
        self.new["source"]["text"] = "In the large configuration, we expect improved latency from 80 to 30 ms."
        self.assertEqual(self.run_pair()["action"], "needs_context")

    def test_inactive_comparison_cannot_receive_evidence(self):
        self.old["source"]["text"] += " The new queue comparison is not yet underway."
        self.assertEqual(self.run_pair(("A", "D"))["action"], "needs_context")

    def test_constraint_requires_a_witness(self):
        self.assertEqual(self.run_pair(("A", "C"))["action"], "needs_context")

    def test_no_reason_and_delegated_authorship(self):
        self.old["source"]["text"] = "We deferred the small queue configuration."
        self.assertEqual(self.run_pair()["action"], "needs_context")
        other = Store(self.store.root/"foreign")
        capture(other, {**self.old, "owner": "collector", "source": {**self.old["source"], "text": self.old_text}})
        self.assertEqual(reconsider(other, self.new, self.goal, Choices("A", "B"))["assessments"][0]["action"], "needs_context")

    def test_legacy_rejected_decision_still_found(self):
        legacy = {**self.old, "issue": "queue", "scope": {"setting": "small"}, "quote": self.old_text, "value": "defer"}
        self.store.put("records", legacy)
        self.assertEqual(reconsider(self.store, self.new, self.goal, Choices("A", "B"))["assessments"][0]["action"], "request_comparison")
        row = submit(self.store, legacy)
        review(self.store, row["id"], row["proposal"], "author", "reject")
        self.assertEqual(reconsider(self.store, self.new, self.goal, Choices("A", "B"))["assessments"][0]["reason"]["quote"], self.old_text)

    def test_duplicate_and_unrelated_skip_reader(self):
        capture(self.store, self.old)
        self.assertEqual(reconsider(self.store, source("copy", self.old_text, 2), self.goal, Choices())["status"], "duplicate")
        self.assertEqual(reconsider(self.store, source("member", "Violin pizzicato.", 3), self.goal, Choices())["status"], "no_target")

    def test_exact_reviewer_and_strict_basis_and_stale(self):
        self.run_pair()
        proposal, = proposal_inbox(self.store)
        pid = proposal["id"]
        for basis, who in ((pid, "member"), ("other-hash", "author")):
            with self.assertRaises(ValueError):
                review_proposal(self.store, pid, basis, who, "approve")
        capture(self.store, source("third", "A further report arrived.", 3))
        self.assertEqual(proposal_inbox(self.store)[0]["status"], "stale")
        with self.assertRaises(ValueError):
            review_proposal(self.store, pid, pid, "author", "approve")

    def test_hash_valid_but_spliced_and_self_approved_record(self):
        row = self.run_pair()
        altered = copy.deepcopy(row)
        altered["reason"]["quote"] = "Invented explanation."
        altered["status"] = "approved_comparison"
        key = self.store.put("decision_assessments", altered)
        self.assertEqual(next(p["status"] for p in proposal_inbox(self.store) if p["id"] == key), "invalid_evidence")
        with self.assertRaises(ValueError):
            review_proposal(self.store, key, key, "author", "approve")

    def test_default_qa_and_idempotent_review_via_cli(self):
        capture(self.store, self.old)
        capture(self.store, self.new)
        before = answer(self.store, self.goal)
        self.run_pair()
        def cli(*args):
            return json.loads(subprocess.check_output([sys.executable, "-m", "team_memory", "--store", str(self.store.root), *args]))
        pid, = [r["id"] for r in cli("inbox") if r["kind"] == "decision_reconsideration"]
        self.assertEqual(answer(self.store, self.goal), before)
        for _ in range(2):
            self.assertEqual(cli("review", pid, pid, "author", "approve")["status"], "approved_comparison")
        self.assertEqual(cli("ask", self.goal), before)
        self.assertFalse(self.store.load("reviews"))
        capture(self.store, source("third", "A new violin note.", 3))
        self.assertEqual(reconsider(self.store, self.new, self.goal, Choices(), 1)["assessments"][0]["status"], "approved_comparison")
        self.assertEqual(len(self.store.load("decision_votes")), 1)

    def test_parallel_approval_and_rejection_remain_visible_after_git_merge(self):
        self.run_pair()
        pid = proposal_inbox(self.store)[0]["id"]
        def git(*args):
            return subprocess.run(["git", "-c", "user.name=test", "-c", "user.email=test@example.test", *args],
                                  cwd=self.store.root, check=True, capture_output=True)
        git("init", "-b", "main")
        git("add", ".")
        git("commit", "-m", "pending")
        git("switch", "-c", "other")
        review_proposal(self.store, pid, pid, "author", "reject")
        git("add", ".")
        git("commit", "-m", "reject")
        git("switch", "main")
        review_proposal(self.store, pid, pid, "author", "approve")
        git("add", ".")
        git("commit", "-m", "approve")
        git("merge", "--no-edit", "other")
        self.assertEqual(proposal_inbox(self.store)[0]["status"], "review_conflict")
        self.assertEqual(len(self.store.load("decision_votes")), 2)

    def test_intake_shadow_survives_invalid_draft_and_invalid_choice_retries(self):
        capture(self.store, self.old)
        default = ingest(self.store, self.new, lambda *_: "null")
        self.assertNotIn("decision_review", default)
        with self.assertRaises(ValueError):
            reconsider(self.store, self.new, self.goal, Choices("?", "B"))
        self.assertFalse(self.store.load("decision_assessments"))
        result = ingest(self.store, self.new, lambda *_: "not-json", reconsider_goal=self.goal, choose=Choices("A", "B"))
        self.assertEqual(result["outcome"], "invalid_draft")
        self.assertEqual(result["decision_review"]["assessments"][0]["action"], "request_comparison")
        sources, _ = source_snapshot(self.store)
        self.assertEqual(len(prepare(sources, result["source_id"], self.goal, 1)["cases"]), 1)
