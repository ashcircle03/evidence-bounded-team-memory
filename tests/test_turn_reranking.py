"""Regression checks for predecessor selection, stable ties and the frozen top five."""
from types import SimpleNamespace
from unittest import TestCase, skipUnless
from unittest.mock import MagicMock, patch
from importlib.util import find_spec

from team_memory.readers.turn_reranking import previous_turn_order


class TurnRankingTests(TestCase):
    @skipUnless(find_spec('torch'), 'optional reference dependencies')
    def test_previous_turn_only_and_original_nodes(self):
        import torch
        locations = ['a#turn=2', 'a#turn=1', 'b#turn=2', 'a#turn=4', 'a#turn=5', 'b#turn=4']
        sources = {str(i): {'source': dict(text=str(i), speaker='s', location=loc)}
                   for i, loc in enumerate(locations)}
        # Two original chunk nodes from turn 2, equal scores must preserve their order.
        nodes = [SimpleNamespace(node=SimpleNamespace(metadata={'source_id': sid}))
                 for sid in ('0', '0', '2', '3', '4', '5')]
        tok = MagicMock(sep_token_id=99)
        tok.num_special_tokens_to_add.return_value = 3
        tok.encode.side_effect = lambda text, **kw: [int(text.split()[-1])] if text != 'query' else [10]
        tok.prepare_for_model.side_effect = lambda q, body, **kw: body
        tok.pad.return_value = {}
        model = MagicMock(return_value=SimpleNamespace(logits=torch.tensor([[2.],[2.],[1.],[5.],[0.]])))
        with patch('team_memory.readers.turn_reranking.encoder', return_value=(tok, model)):
            ordered = previous_turn_order('query', nodes, sources)
        self.assertEqual(tok.pad.call_args.args[0], [[1,99,0], [1,99,0], [2], [3], [3,99,4]])
        self.assertEqual([id(n) for n in ordered], [id(nodes[i]) for i in (3,0,1,2,4,5)])

    def test_plain_sources_need_no_encoder(self):
        hit = SimpleNamespace(node=SimpleNamespace(metadata={'source_id':'s'}))
        nodes = [hit, hit]
        with patch('team_memory.readers.turn_reranking.encoder') as load:
            self.assertIs(previous_turn_order('q', nodes, {'s':{'source':{'location':'report.md'}}}), nodes)
            load.assert_not_called()
