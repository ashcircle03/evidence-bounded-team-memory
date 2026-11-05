import copy
import json
from pathlib import Path
import tempfile
import unittest

from evaluation.cupmem import transfer_inputs as t
from team_memory.timeline import witness


class TransferFixtures(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.actors, cls.manifest = t.build()
        cls.original_git = json.loads((t.ROOT / t.GIT_INPUT).read_text())
        cls.original_timeline = json.loads((t.ROOT / t.TIMELINE_INPUT).read_text())

    def test_every_original_source_and_question_is_preserved(self):
        self.assertEqual(self.manifest["counts"], {
            "git_cases": 60, "timeline_streams": 20, "git_source_arrivals": 180,
            "git_qa_checkpoints": 6, "timeline_source_arrivals": 100,
            "timeline_qa_checkpoints": 140, "deferred_owner_reviews": 12,
        })
        for original, case in zip(self.original_git, self.actors["git"]):
            events = case["events"]
            self.assertEqual([e["source"] for e in events if e["op"] == "ingest"],
                             [*original["prior"], original["incoming"]])
            self.assertEqual([e["question"] for e in events if e["op"] == "ask"],
                             [original["qa"]] if "qa" in original else [])
        for original, case in zip(self.original_timeline, self.actors["timeline"]):
            expected = [s for s in original["steps"] if s["op"] != "review"]
            for step, event in zip(expected, case["events"]):
                self.assertEqual(event["op"], step["op"])
                field = "source" if step["op"] == "ingest" else "question"
                self.assertEqual(event[field], step[field])

    def test_only_source_projections_reach_writer_and_no_future_leaks(self):
        for case in self.actors["timeline"] + self.actors["git"]:
            seen = []
            for index, event in enumerate(case["events"]):
                if event["op"] == "ingest":
                    seen.append(event["source"])
                record = t.native_record_at(case, index)
                self.assertEqual(set(record), {"uid", "haystack_session", "timestamps", "probing_queries"})
                restored = [json.loads(session[0]["content"]) for session in record["haystack_session"]]
                self.assertEqual(restored, seen)
                self.assertEqual(record["timestamps"], [s["observed_at"] for s in seen])
                self.assertTrue(all(len(s) == 1 and s[0]["role"] == "user" for s in record["haystack_session"]))
                self.assertEqual(list(record["probing_queries"].values()),
                                 [event["question"]] if event["op"] == "ask" else [])

    def test_labels_gold_and_review_scripts_live_only_in_evaluator_manifest(self):
        self.assertEqual(self.manifest["audience"], "evaluator_only_never_model_input")
        serialized = t.encoded(self.actors).decode()
        for row in self.original_git:
            self.assertNotIn(row["id"], serialized)
        for group in ("git", "timeline"):
            for case in self.actors[group]:
                self.assertEqual(set(case), {"case_id", "events"})
                self.assertRegex(case["case_id"], "^[0-9a-f]{24}$")
                for event in case["events"]:
                    self.assertIn(event["op"], ("ingest", "ask"))
                    self.assertEqual(set(event), {"op", "event_id", "source" if event["op"] == "ingest" else "question"})
        for original, case in zip(self.original_timeline, self.actors["timeline"]):
            entry = self.manifest["timeline"][case["case_id"]]
            self.assertEqual([r["script"] for r in entry["deferred_reviews"]],
                             [s for s in original["steps"] if s["op"] == "review"])
            for review in entry["deferred_reviews"]:
                index = review["original_step_index"]
                self.assertEqual(review["after_event_id"], t.opaque_id(case["case_id"], index - 1))

    def test_frozen_source_modification_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in [t.FREEZE, *self.manifest["source_files"]]:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes((t.ROOT / name).read_bytes())
            modified = root / t.TIMELINE_INPUT
            modified.write_bytes(modified.read_bytes() + b" ")
            with self.assertRaisesRegex(ValueError, "Frozen transfer source changed"):
                t.build(root)

    def test_extra_semantic_fields_cannot_enter_source_projection(self):
        env = copy.deepcopy(self.original_git[0]["prior"][0])
        env["expected_relation"] = "review"
        with self.assertRaisesRegex(ValueError, "Unexpected source-envelope fields"):
            t.attributed_session(env)
        env.pop("expected_relation")
        env["source"]["selected_because"] = "correct target"
        with self.assertRaisesRegex(ValueError, "Unexpected source fields"):
            t.attributed_session(env)

    def test_export_matches_checked_in_bytes(self):
        folder = t.ROOT / "evaluation/cupmem"
        self.assertEqual((folder / "transfer-inputs.json").read_bytes(), t.encoded(self.actors))
        self.assertEqual((folder / "transfer-inputs.manifest.json").read_bytes(), t.encoded(self.manifest))
        self.assertEqual(t.sha256(t.encoded(self.actors)), self.manifest["actor_sha256"])


class OwnerReviewGate(unittest.TestCase):
    def setUp(self):
        row = json.loads((t.ROOT / t.TIMELINE_INPUT).read_text())[0]
        self.script = next(s for s in row["steps"] if s["op"] == "review")
        self.sources = {t.source_id(s["source"]): s["source"] for s in row["steps"] if s["op"] == "ingest"}
        old, new = (self.sources[self.script[name]] for name in ("previous", "incoming"))
        self.proposal = {
            "id": "actual-output-proposal", "kind": self.script["kind"],
            "previous": witness(old, old["source"]["text"]),
            "incoming": witness(new, new["source"]["text"]),
            "history": [self.script["previous"]], "reviewer": old["owner"], "status": "pending",
        }

    def test_native_never_earns_an_approval_from_script(self):
        before = copy.deepcopy(self.sources)
        result = t.review_gate(self.script, [self.proposal], self.sources)
        self.assertEqual(result, {"status": "unsupported_native_owner_review", "proposal_ids": []})
        self.assertEqual(self.sources, before)
        result = t.review_gate(self.script, [], self.sources, approval_adapter=True)
        self.assertEqual(result["status"], "deferred_no_matching_proposal")

    def test_eligible_proposal_is_selected_but_not_applied(self):
        proposal = copy.deepcopy(self.proposal)
        result = t.review_gate(self.script, [proposal], self.sources, approval_adapter=True)
        self.assertEqual(result, {"status": "eligible_existing_proposal", "proposal_ids": [proposal["id"]]})
        self.assertEqual(proposal["status"], "pending")

    def test_wrong_pair_fabricated_quote_wrong_owner_and_closed_status_are_rejected(self):
        bad = []
        p = copy.deepcopy(self.proposal); p["previous"]["source_id"] = self.script["incoming"]; bad.append(p)
        p = copy.deepcopy(self.proposal); p["incoming"]["quote"] = "invented finding"; bad.append(p)
        p = copy.deepcopy(self.proposal); p["reviewer"] = "someone else"; bad.append(p)
        p = copy.deepcopy(self.proposal); p["status"] = "approved"; bad.append(p)
        p = copy.deepcopy(self.proposal); p["kind"] = "correction"; bad.append(p)
        p = copy.deepcopy(self.proposal); p["history"] = [self.script["previous"], self.script["incoming"]]; bad.append(p)
        for proposal in bad:
            with self.subTest(proposal=proposal):
                result = t.review_gate(self.script, [proposal], self.sources, approval_adapter=True)
                self.assertEqual(result["proposal_ids"], [])


if __name__ == "__main__":
    unittest.main()
