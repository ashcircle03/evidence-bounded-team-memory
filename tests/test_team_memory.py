import tempfile
import unittest
from pathlib import Path

from team_memory.demo import sample, vote
from team_memory.merge import overlap_action, replay, review, submit
from team_memory.qa import answer
from team_memory.store import Store
from team_memory.writer import draft, prepare


class Sharing(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.store = Store(Path(tmp.name))

    def test_late_pending_record_does_not_undo_approved_correction(self):
        a = submit(self.store, sample(1, "a", "low", "x"))
        vote(self.store, a, "a")
        c = submit(self.store, sample(3, "a", "high", "x", corrects=a["id"]))
        vote(self.store, c, "a")
        self.assertEqual(replay(self.store)[a["id"]]["status"], "superseded")
        submit(self.store, sample(2, "b", "unknown", "x"))
        view = replay(self.store)
        self.assertEqual(view[a["id"]]["status"], "superseded")
        self.assertEqual(view[c["id"]]["status"], "accepted")
        self.assertTrue(answer(self.store, "다중 클래스 성능")["next_actions"])

    def test_rejected_correction_leaves_team_state_intact(self):
        a = submit(self.store, sample(1, "a", "old", "x"))
        vote(self.store, a, "a")
        b = submit(self.store, sample(2, "b", "new", "x", corrects=a["id"]))
        with self.assertRaises(ValueError):
            vote(self.store, b, "observer")
        vote(self.store, b, "b")
        review(self.store, b["id"], b["proposal"], "a", "reject")
        result = answer(self.store, "", issue=b["record"]["issue"])
        self.assertEqual([x["value"] for x in result["accepted"]], ["old"])
        self.assertFalse(result["pending"])

    def test_idempotence_and_unseen_quote(self):
        inp = sample(1, "a", "old", "x")
        a = submit(self.store, inp)
        self.assertEqual(a, submit(self.store, inp))
        self.assertEqual(len(self.store.load("records")), 1)
        self.assertEqual(answer(self.store, "completely unrelated potassium")["status"], "insufficient")
        with self.assertRaises(ValueError):
            submit(self.store, dict(inp, quote="fabricated"))

    def test_crossed_and_unknown_conditions_are_not_disjoint(self):
        def action(a, b):
            return overlap_action("old", {"scope": a, "value": "old"}, {"scope": b, "value": "new"})
        self.assertEqual(action({"x": "a", "y": "*"}, {"x": "*", "y": "b"}), "unresolved")
        self.assertEqual(action({}, {"x": "b"}), "unresolved")
        self.assertEqual(action({"x": "*"}, {"x": "b"}), "keep_by_condition")
        self.assertEqual(action({"x": "a"}, {"x": "b"}), "keep_by_condition")

    def test_conflicting_review_and_duplicate_do_not_overwrite_first_record(self):
        a = submit(self.store, sample(1, "a", "old", "x"))
        vote(self.store, a, "a")
        b = submit(self.store, sample(2, "b", "old", "x"))
        self.assertEqual(b["targets"][0]["action"], "duplicate")
        vote(self.store, b, "b")
        conflicting = {"proposal": b["proposal"], "actor": "b", "record": b["id"], "decision": "reject"}
        self.store.put("reviews", conflicting)  # Two opposite reviews merged from concurrent branches.
        view = replay(self.store)
        self.assertEqual(view[b["id"]]["status"], "review_conflict")
        self.assertEqual(view[a["id"]]["status"], "accepted")

    def test_writer_cannot_set_owner_and_approval(self):
        import json
        env = sample(1, "a", "val", "x")
        output = {**env, "owner": "b", "status": "accepted"}
        self.assertEqual(draft(self.store, env, lambda *_: json.dumps(output))["owner"], "a")
        self.assertNotIn("status", draft(self.store, env, lambda *_: json.dumps(output)))
        self.assertEqual(prepare(self.store, env)["input"]["source"], env["source"])

    def test_reader_cannot_promote_or_use_a_missing_quote(self):
        import json
        from team_memory.qa import read_answer
        item = submit(self.store, sample(1, "a", "미관측", "x"))
        base = answer(self.store, "다중 클래스 성능")
        def pick(span):
            return lambda *_: json.dumps({"id": item["id"], "field": "quote", "span": span, "status": "accepted"})
        self.assertEqual(read_answer(base, "결과?", pick("미관측"))["reader"]["status"], "pending")
        self.assertEqual(read_answer(base, "결과?", pick("invented"))["reader"]["status"], "invalid_citation")

    def test_writer_sees_existing_evidence_but_must_name_valid_correction_target(self):
        import json
        first = sample(1, "a", "old", "x")
        old = submit(self.store, first)
        later = sample(2, "a", "new", "x", corrects=old["id"])
        self.assertEqual(prepare(self.store, later)["earlier_records"][0]["id"], old["id"])
        self.assertEqual(draft(self.store, later, lambda *_: json.dumps(later))["corrects"], old["id"])
        with self.assertRaises(ValueError):
            draft(self.store, later, lambda *_: json.dumps(dict(later, corrects="unknown")))

    def test_pending_vote_cannot_apply_to_a_changed_proposal(self):
        first = submit(self.store, sample(1, "original", "negative", "x"))
        vote(self.store, first, "original")
        new = submit(self.store, sample(3, "other", "positive", "y"))
        vote(self.store, new, "other")
        # Simulate a separately published branch that forked from the first approved record.
        other = dict(sample(2, "third", "unclear", "z"), parents=[first["id"]])
        from team_memory.store import record
        self.store.put("records", dict(record(other), parents=other["parents"]))
        updated = replay(self.store)[new["id"]]
        self.assertNotEqual(updated["proposal"], new["proposal"])
        self.assertEqual(updated["approved_by"], [])
        with self.assertRaises(ValueError):
            vote(self.store, new, "original")

    def test_unparsed_source_survives_and_can_be_cited_without_approval(self):
        from team_memory.writer import ingest
        from team_memory.qa import read_answer
        import json
        data = sample(1, "member", "개선 없음", "기간 A")
        first = ingest(self.store, data, lambda *_: "null")
        retry = ingest(self.store, data, lambda *_: "not valid JSON")
        self.assertEqual(first["source_id"], retry["source_id"])
        self.assertFalse(self.store.load("records"))
        result = answer(self.store, "다중 클래스 성능")
        self.assertEqual(result["status"], "source_only")
        pick = json.dumps({"id": first["source_id"], "field": "quote", "span": "개선 없음"})
        self.assertEqual(read_answer(result, "결과?", lambda *_: pick)["reader"]["status"], "source_only")

    def test_approved_concurrent_corrections_remain_in_conflict_after_pull(self):
        import shutil
        from team_memory.store import Store
        origin = submit(self.store, sample(1, "owner", "initial", "x"))
        vote(self.store, origin, "owner")
        with tempfile.TemporaryDirectory() as tmp:
            branch = Store(Path(tmp) / "fork")
            shutil.copytree(self.store.root, branch.root)
            versions = []
            for st, day, value in ((self.store, 2, "left",), (branch, 3, "right",)):
                change = submit(st, sample(day, "owner", value, "x", corrects=origin["id"]))
                vote(st, change, "owner")
                versions.append(change["id"])
            shutil.copytree(branch.root, self.store.root, dirs_exist_ok=True)
        combined = answer(self.store, "다중 클래스 성능")
        self.assertEqual({r["id"] for r in combined["accepted"]}, set(versions))
        self.assertEqual(len(combined["unresolved"]), 1)
