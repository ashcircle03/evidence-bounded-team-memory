import copy
import unittest

from team_memory.role_review import core_passage, evidence_link, locate, unsupported_details, valid_ledger


class RoleReviewTest(unittest.TestCase):
    def setUp(self):
        self.text = "On a cold boot, the scheduler does not run checks."
        self.parent = dict(source_id="src0", location="worklog", speaker="Lee",
                           quote=self.text, start=90, end=90+len(self.text))

    def test_offsets_resolve_multiline_and_ambiguous_text_is_rejected(self):
        self.assertEqual(locate("A cold\nboot failed", "cold boot"),
                         {"start": 2, "end": 11, "quote": "cold\nboot"})
        self.assertIsNone(locate("one one", "one"))
        self.assertIsNone(locate("returns non-NULL", "NULL"))
        self.assertIsNone(locate("run checks", "run new checks"))

    def test_short_evidence_keeps_context(self):
        text = self.text+" Otherwise it runs."
        w = dict(self.parent, quote=text, end=90+len(text))
        self.assertEqual(core_passage(w, {}, None), w)

    def test_unsupported_nesting_and_flag_are_identified(self):
        passage = {"quote": "tick() calls advance(); poll() performs a separate check."}
        self.assertFalse(unsupported_details("advance() in tick()", [passage]))
        self.assertEqual(unsupported_details("tick() in advance() with --drain", [passage]),
                         ["option absent from evidence: --drain", "unsupported nesting: tick() in advance()"])

    def test_tampered_ledger_fails(self):
        row = dict(previous=self.parent, incoming=dict(self.parent, source_id="src1"), rationale=self.text)
        role_quotes = dict(subject="the scheduler", action="does not run checks", condition="On a cold boot")
        row["role_evidence"] = {}
        for role, quote in role_quotes.items():
            assertion=locate(self.text, quote)
            row["role_evidence"][role] = dict(assertion=assertion, evidence=evidence_link(self.parent, assertion))
        self.assertTrue(valid_ledger(row))
        for field, value in (("speaker","Kim"),("end",90),("quote","always runs")):
            bad=copy.deepcopy(row)
            bad["role_evidence"]["action"]["evidence"][field]=value
            self.assertFalse(valid_ledger(bad))
        del row["role_evidence"]["condition"]
        self.assertFalse(valid_ledger(row))

    def test_slots_keep_receiver_scope_and_polarity(self):
        from team_memory.role_binding import bind
        for sentence, expected in [
                ("The token supplied to prepare() was not forwarded to publish().",
                 ("The token", "was not forwarded to publish()", "supplied to prepare()")),
                ("Parser does not accept escapes by default.",
                 ("Parser", "does not accept escapes", "by default")),
                ("Switching from v0() to v1() started returning false for empty().",
                 ("v1()", "started returning false", "for empty()"))]:
            got=bind(sentence)
            self.assertEqual(tuple(got[k]["quote"] for k in ("subject","action","condition")), expected)
        self.assertFalse(bind("The cache can store requests. The transport did not exit."))

    def test_citation_prefix_with_nested_function_arguments(self):
        from team_memory.role_review import citation_prefix_end
        prefix="Fix a regression in deadbeef (use reader(), 2019-04-05), "
        self.assertEqual(citation_prefix_end(prefix+"under load it fails."), len(prefix))
        self.assertEqual(citation_prefix_end("Keep reader(), even if it fails."), 0)
