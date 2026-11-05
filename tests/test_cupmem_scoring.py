"""Mechanical failures and unresolved adjudication; no inference or server use."""
from copy import deepcopy
import json
import unittest

from evaluation.cupmem.scoring import FrozenScorer, check_witness, summarize_proposals
from team_memory.store import digest
from team_memory.timeline import witness


class FrozenScoringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scorer = FrozenScorer()
        cls.original_keys = deepcopy(cls.scorer.keys)

    def transfer(self, original, suite="timeline"):
        cid = next(k for k, v in self.scorer.manifest[suite].items() if v["original_id"] == original)
        case = self.scorer.cases[suite][cid]
        docs = {digest(e["source"]): e["source"] for e in case["events"] if e["op"] == "ingest"}
        return cid, case, docs

    def checkpoint(self, original, label):
        cid, case, docs = self.transfer(original)
        entry = self.scorer.manifest["timeline"][cid]
        qid = next(k for k, v in entry["queries"].items() if v["original_label"] == label)
        return cid, qid, docs

    def timeline_answer(self, original, label):
        _, _, docs = self.checkpoint(original, label)
        key = self.scorer.keys["timeline"][original]["qa"][label]
        answers = []
        for gold in key["answers"]:
            env = docs[gold["source_id"]]
            row = dict(witness(env, env["source"]["text"]), answer=gold["aliases"][0], status=gold["status"], condition=None)
            if gold["condition"]:
                row["condition"] = witness(env, gold["condition"])
            answers.append(row)
        return {"kind": key["kind"], "answers": answers}

    def proposal(self, original, *, kind=None, repeat=False):
        cid, case, docs = self.transfer(original)
        key = self.scorer.keys["timeline"][original]
        incoming = key["repeat_source"] if repeat else key["new"]
        eid = next(e["event_id"] for e in case["events"] if e["op"] == "ingest" and digest(e["source"]) == incoming)
        return cid, eid, dict(kind=kind or key["expected_relation"],
                             previous=witness(docs[key["old"]], docs[key["old"]]["source"]["text"]),
                             incoming=witness(docs[incoming], docs[incoming]["source"]["text"]),
                             reason="An ungraded model explanation, not a keyword-based judgment.")

    def rating(self, scored_card, ok=True):
        return {scored_card["card_id"]: {"ok": ok, "reason": "Explicit test adjudication only.",
                                         "reviewer": "test fixture", "reviewer_type": "human"}}

    def test_correct_alias_and_literal_citation_do_not_auto_pass_semantics(self):
        cid, qid, _ = self.checkpoint("final-01", "natural_before")
        answer = self.timeline_answer("final-01", "natural_before")
        row = self.scorer.score_qa("timeline", cid, qid, answer, output_mode="cited")
        self.assertTrue(row["fixed_key"]["correct"])
        self.assertTrue(row["citation_mechanics"]["valid"])
        self.assertIsNone(row["semantic"]["rating"]["ok"])
        self.assertIsNone(row["fixed_reference_joint_correct"])
        scored = self.scorer.score_qa("timeline", cid, qid, answer, output_mode="cited",
                                      ratings=self.rating(row["semantic"]))
        self.assertTrue(scored["fixed_reference_joint_correct"])
        answer["model"] = "MODEL_ID_SHOULD_NOT_ENTER_BLIND_CARD"
        blinded = self.scorer.score_qa("timeline", cid, qid, answer, output_mode="cited")
        self.assertEqual(blinded["semantic"]["card_id"], row["semantic"]["card_id"])
        self.assertNotIn("MODEL_ID_SHOULD_NOT_ENTER_BLIND_CARD", json.dumps(blinded["semantic"]["card"]))

    def test_native_negated_alias_is_only_a_diagnostic_and_has_no_citation_score(self):
        cid, qid, _ = self.checkpoint("final-01", "natural_before")
        row = self.scorer.score_qa("timeline", cid, qid, "It was not 96%.", output_mode="native")
        self.assertTrue(row["alias_diagnostic"]["all_present"])
        self.assertIsNone(row["fixed_key"]["correct"])
        self.assertIsNone(row["citation_mechanics"]["valid"])
        self.assertIsNone(row["native_answer_semantic_correct"])
        self.assertIsNone(row["fixed_reference_joint_correct"])

    def test_span_source_attribution_and_future_visibility_are_checked(self):
        cid, qid, docs = self.checkpoint("final-01", "natural_before")
        answer = self.timeline_answer("final-01", "natural_before")
        answer["answers"][0]["start"] += 1
        row = self.scorer.score_qa("timeline", cid, qid, answer, output_mode="cited")
        self.assertTrue(row["fixed_key"]["correct"])
        self.assertFalse(row["citation_mechanics"]["valid"])
        self.assertFalse(row["fixed_reference_joint_correct"])
        original = self.timeline_answer("final-01", "natural_before")["answers"][0]
        for field in ("speaker", "location"):
            broken = dict(original, **{field: "wrong attribution"})
            self.assertFalse(check_witness(broken, docs)["valid"])
        future = docs[self.scorer.keys["timeline"]["final-01"]["repeat_source"]]
        answer["answers"][0] = dict(witness(future, future["source"]["text"]), answer="96%", status="reported")
        row = self.scorer.score_qa("timeline", cid, qid, answer, output_mode="cited")
        self.assertIn("source_not_visible", row["citation_mechanics"]["citations"][0]["errors"])

    def test_fixed_approved_gold_is_unchanged_when_owner_review_did_not_happen(self):
        cid, qid, _ = self.checkpoint("final-13", "reviewed")
        approved = self.timeline_answer("final-13", "reviewed")
        row = self.scorer.score_qa("timeline", cid, qid, approved, output_mode="cited")
        self.assertTrue(row["fixed_key"]["correct"])
        self.assertTrue(row["workflow"]["unreachable_approved_state"])
        self.assertTrue(row["unearned_approval_claim"])
        self.assertFalse(row["actual_no_review_joint_correct"])
        actual_card = row["actual_no_review_semantic"]["card"]
        self.assertNotIn("reference_sides", actual_card)
        self.assertIn(self.scorer.keys["timeline"]["final-13"]["old"],
                      {source["source_id"] for source in actual_card["visible_sources"]})
        retained = self.timeline_answer("final-13", "changed")
        row = self.scorer.score_qa("timeline", cid, qid, retained, output_mode="cited")
        self.assertFalse(row["fixed_key"]["correct"])
        self.assertTrue(row["workflow"]["unreachable_approved_state"])
        self.assertIsNone(row["actual_no_review_joint_correct"])
        judged = self.scorer.score_qa("timeline", cid, qid, retained, output_mode="cited",
                                      ratings=self.rating(row["actual_no_review_semantic"]))
        self.assertFalse(judged["fixed_key"]["correct"])
        self.assertTrue(judged["actual_no_review_joint_correct"])
        self.assertEqual(self.scorer.keys, self.original_keys)

    def test_approval_requires_a_bound_actual_action_receipt(self):
        cid, qid, _ = self.checkpoint("final-13", "reviewed")
        answer = self.timeline_answer("final-13", "reviewed")
        review = self.scorer.manifest["timeline"][cid]["deferred_reviews"][0]
        receipt = dict(script_sha256=review["script_sha256"], applied=True,
                       actor=review["script"]["actor"], choice="approve", proposal_id="actually-generated-id",
                       evidence_ref="execution-audit:actual-owner-action")
        row = self.scorer.score_qa("timeline", cid, qid, answer, output_mode="cited", applied_reviews=[receipt])
        self.assertTrue(row["workflow"]["desired_workflow_state_reached"])
        self.assertFalse(row["workflow"]["unreachable_approved_state"])
        receipt.pop("evidence_ref")
        with self.assertRaisesRegex(ValueError, "application evidence"):
            self.scorer.score_qa("timeline", cid, qid, answer, output_mode="cited", applied_reviews=[receipt])

    def legacy_answer(self, cid):
        case = self.scorer.legacy_cases[cid]
        docs = self.scorer.legacy["documents"]
        ids = self.scorer.legacy["histories"][case["history_id"]]["historical_source_ids"]
        answers = []
        for side in self.scorer.legacy["evaluation_only"][cid]["expected_sides"]:
            env = next(docs[sid] for sid in ids if docs[sid]["source"]["location"] in side.get("locations", [side.get("location")]))
            answers.append(dict(witness(env, env["source"]["text"]), answer=side["aliases"][0], status="reported", condition=None))
        return dict(kind="conditional" if len(answers) > 1 else "single", answers=answers)

    def test_legacy_requires_every_side_bound_to_its_own_source_and_condition(self):
        cid = "d07/premise"
        answer = self.legacy_answer(cid)
        row = self.scorer.score_qa("legacy", cid, None, answer, output_mode="cited")
        self.assertTrue(row["fixed_key"]["correct"])
        self.assertIsNone(row["fixed_reference_joint_correct"])
        omitted = deepcopy(answer); omitted["answers"].pop()
        row = self.scorer.score_qa("legacy", cid, None, omitted, output_mode="cited")
        self.assertFalse(row["fixed_key"]["correct"])
        swapped = deepcopy(answer)
        swapped["answers"][0]["answer"], swapped["answers"][1]["answer"] = swapped["answers"][1]["answer"], swapped["answers"][0]["answer"]
        row = self.scorer.score_qa("legacy", cid, None, swapped, output_mode="cited")
        self.assertTrue(row["alias_diagnostic"]["all_present"])
        self.assertFalse(row["fixed_key"]["correct"])

    def test_legacy_valid_value_quote_does_not_prove_default_value_answer(self):
        cid = "q04-ordinary/legacy"
        answer = self.legacy_answer(cid)
        env = self.scorer.legacy["documents"][answer["answers"][0]["source_id"]]
        quote = "Valid values are\n\t`full` and `compact`."
        answer["answers"][0] = dict(witness(env, quote), answer="full", status="reported", condition=None)
        row = self.scorer.score_qa("legacy", cid, None, answer, output_mode="cited")
        self.assertTrue(row["fixed_key"]["correct"])
        self.assertTrue(row["citation_mechanics"]["valid"])
        self.assertIsNone(row["fixed_reference_joint_correct"])
        judged = self.scorer.score_qa("legacy", cid, None, answer, output_mode="cited",
                                      ratings=self.rating(row["semantic"], False))
        self.assertFalse(judged["fixed_reference_joint_correct"])

    def test_proposal_reason_is_pending_even_when_target_kind_and_quotes_match(self):
        cid, eid, proposal = self.proposal("final-01")
        row = self.scorer.score_proposals("timeline", cid, eid, [proposal], trigger="prompted")
        self.assertIsNone(row["grounded_review"])
        self.assertTrue(row["proposals"][0]["expected_pair"])
        self.assertTrue(row["proposals"][0]["expected_kind"])
        judged = self.scorer.score_proposals("timeline", cid, eid, [proposal], trigger="prompted",
                                             ratings=self.rating(row["proposals"][0]["semantic"]))
        self.assertTrue(judged["grounded_review"])
        self.assertEqual(judged["trigger"], "prompted")
        bad_rating = {row["proposals"][0]["semantic"]["card_id"]: {"ok": True}}
        with self.assertRaisesRegex(ValueError, "Malformed semantic rating"):
            self.scorer.score_proposals("timeline", cid, eid, [proposal], trigger="prompted", ratings=bad_rating)

    def test_negative_false_alert_wrong_kind_and_repeat_are_separate(self):
        cid, eid, proposal = self.proposal("final-17", kind="reconsider")
        negative = self.scorer.score_proposals("timeline", cid, eid, [proposal], trigger="write")
        self.assertEqual(negative["false_alerts_on_review_negatives"], 1)
        self.assertEqual(negative["wrong_relation_on_review_positives"], 0)
        cid, eid, proposal = self.proposal("final-01", kind="conflict")
        wrong = self.scorer.score_proposals("timeline", cid, eid, [proposal], trigger="write")
        self.assertEqual(wrong["false_alerts_on_review_negatives"], 0)
        self.assertEqual(wrong["wrong_relation_on_review_positives"], 1)
        cid, eid, proposal = self.proposal("final-01", kind="reconsider", repeat=True)
        repeat = self.scorer.score_proposals("timeline", cid, eid, [proposal], trigger="write")
        self.assertEqual(repeat["repeat_arrival_alerts"], 1)
        self.assertEqual(repeat["false_alerts_on_review_negatives"], 0)
        self.assertEqual(repeat["wrong_relation_on_review_positives"], 0)

    def test_prior_events_are_unlabeled_and_native_updates_are_not_proposals(self):
        cid, case, _ = self.transfer("final-01")
        _, _, proposal = self.proposal("final-01")
        eid = case["events"][0]["event_id"]
        row = self.scorer.score_proposals("timeline", cid, eid, [proposal], trigger="write")
        self.assertEqual(row["label_coverage"], "unlabeled")
        self.assertEqual(row["false_alerts_on_review_negatives"], 0)
        self.assertIsNone(row["grounded_review"])
        self.assertNotIn(self.scorer.keys["timeline"]["final-01"]["reason_criterion"],
                         json.dumps(row["proposals"][0]["semantic"]["card"]))
        audit = self.scorer.audit_native_updates("timeline", cid, eid, [{"operation": "WEAKEN"}])
        self.assertIsNone(audit["grounded_review"])
        self.assertIsNone(audit["false_alerts"])
        self.assertIn("unmapped", audit["status"])
        with self.assertRaisesRegex(ValueError, "not native operations"):
            self.scorer.score_proposals("timeline", cid, eid, [{"kind": "WEAKEN"}], trigger="write")

    def test_coexistence_is_not_a_review_alert_and_summary_keeps_pending(self):
        cid, eid, proposal = self.proposal("final-05")
        coexist = self.scorer.score_proposals("timeline", cid, eid, [proposal], trigger="write")
        self.assertTrue(coexist["proposals"][0]["expected_kind"])
        self.assertFalse(coexist["proposals"][0]["alert"])
        cid, eid, proposal = self.proposal("final-01")
        pending = self.scorer.score_proposals("timeline", cid, eid, [proposal], trigger="write")
        summary = summarize_proposals([coexist, pending])[0]
        self.assertEqual(summary["required_reviews"], 1)
        self.assertEqual(summary["grounded_reviews_confirmed"], 0)
        self.assertEqual(summary["grounded_reviews_pending"], 1)

    def test_git_no_match_false_alert_and_supplementary_qa_no_fabricated_gold(self):
        cid, case, docs = self.transfer("patch-search/no-match/raw", "git")
        ingests = [e for e in case["events"] if e["op"] == "ingest"]
        proposal = dict(kind="reconsider", previous=witness(ingests[0]["source"], ingests[0]["source"]["source"]["text"]),
                        incoming=witness(ingests[-1]["source"], ingests[-1]["source"]["source"]["text"]), reason="ungraded")
        row = self.scorer.score_proposals("git", cid, ingests[-1]["event_id"], [proposal], trigger="prompted")
        self.assertEqual(row["false_alerts_on_review_negatives"], 1)
        cid, case, _ = self.transfer("freebsd-cwd/mixed/raw", "git")
        query = next(e for e in case["events"] if e["op"] == "ask")
        row = self.scorer.score_qa("git", cid, query["event_id"], "ERANGE", output_mode="native")
        self.assertEqual(row["fixed_key"]["status"], "not_applicable_native_free_form")
        self.assertIsNone(row["fixed_reference_joint_correct"])
        self.assertIn("no_fixed_qa_key", row["group"])


if __name__ == "__main__":
    unittest.main()
