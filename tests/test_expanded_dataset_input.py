import unittest
from evaluation.reference_qa.expanded.run import iter_dialogue_messages


class NativeMessageInput(unittest.TestCase):
    def test_missing_group_does_not_drop_neighbors_or_renumber_messages(self):
        a={'dialogue':'verbatim A'};b={'dialogue':'verbatim B'}
        days=[dict(date='2025-01-01',dialogues={'Group 1':None,'Group 2':[a,b],'Group 3':[]})]
        rows=list(iter_dialogue_messages(days))
        self.assertEqual(rows,[('2025-01-01','Group 2',1,a),('2025-01-01','Group 2',2,b)])
        self.assertIs(rows[0][3],a)

    def test_nonempty_malformed_group_is_not_silently_dropped(self):
        with self.assertRaises(TypeError):list(iter_dialogue_messages([dict(date='d',dialogues={'G':'bad'})]))
