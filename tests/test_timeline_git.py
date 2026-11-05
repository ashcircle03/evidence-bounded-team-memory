"""Transport/approval integration with fixtures, not model-performance evidence."""
import json
from pathlib import Path
import unittest
from team_memory import timeline as t
from team_memory.store import digest
from evaluation.timeline.runner import stream
from evaluation.timeline.git_replay import replay


class TimelineGitTests(unittest.TestCase):
    def test_exact_prompt_replay_and_two_clone_convergence(self):
        root=Path(__file__).resolve().parents[1]
        row=json.loads((root/'evaluation/timeline/development.json').read_text())[3]
        key=json.loads((root/'evaluation/timeline/development-key.json').read_text())[row['id']]
        sources={digest(s['source']):s['source'] for s in row['steps'] if s['op']=='ingest'}
        for mode in ('direct','indexed'):
            qa=iter(s['id'] for s in row['steps'] if s['op']=='ask')
            def generator(system,content):
                generator.last_usage=dict(input_tokens=1,output_tokens=1)
                data=json.loads(content)
                if system==t.INDEX:return '{"decisions":[]}'
                if system==t.COMPARE:
                    if data['incoming']['id']!=key['new']:return '{"relations":[]}'
                    old=sources[key['old']]['source']['text'].split('.')[0]+'.'
                    return json.dumps(dict(relations=[dict(kind='correction',target=key['old'],old_quote=old,
                        new_quote=sources[key['new']]['source']['text'],reason='The original author explicitly corrects the same R7 limit.')]))
                gold=key['qa'][next(qa)]
                answers=[]
                for a in gold['answers']:
                    answers.append(dict(source=a['source_id'],quote=sources[a['source_id']]['source']['text'],
                                        answer=a['aliases'][0],condition=a['condition']))
                return json.dumps(dict(kind=gold['kind'],answers=answers))
            recorded=stream(row,mode,generator)
            result=replay(row,recorded)
            self.assertTrue(result['clones_converged']);self.assertTrue(result['raw_sources_unchanged'])
            self.assertEqual(result['calls_replayed'],len(recorded['calls']))
            final=next(s['result'] for s in recorded['steps'] if s['id']=='other_preserved')
            self.assertEqual(final['answers'][0]['status'],'reported')


if __name__=='__main__':unittest.main()
