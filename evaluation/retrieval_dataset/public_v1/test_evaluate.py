"""Deterministic metric examples. Run: python3 -m unittest discover -s ."""
import unittest
from evaluate import metrics


class MetricTests(unittest.TestCase):
    def test_late_first_hit(self):
        m=metrics("F02",[{"a"}],["x","y","a"],[],False)
        self.assertEqual(m["MRR@1"],0)
        self.assertAlmostEqual(m["MRR@5"],1/3)
        self.assertEqual(m["Recall@5"],1)

    def test_early_hit_incomplete_bundle(self):
        m=metrics("F05",[{"a","b"},{"c"}],["a","b","a"],["a"],False)
        self.assertEqual(m["MRR@5"],1)
        self.assertEqual(m["Recall@5"],0.5)
        self.assertAlmostEqual(m["turn_recall@5"],2/3)
        self.assertEqual(m["final_all_ranges"],0)

    def test_bundle_after_expansion(self):
        m=metrics("F05",[{"a"},{"b"}],["a"],["a","b"],False)
        self.assertEqual(m["all_ranges@5"],0)
        self.assertEqual(m["final_all_ranges"],1)

    def test_error_is_not_normal_empty(self):
        m=metrics("F02",[{"a"}],[],[],True)
        self.assertEqual(m["error_rate"],1)
        self.assertEqual(m["positive_empty_rate"],0)
        self.assertEqual(m["MRR@5"],0)
