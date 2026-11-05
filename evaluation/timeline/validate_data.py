"""Check evaluation fixtures/temporal visibility; never report this as model accuracy."""
from hashlib import sha256
import json
import re
from .build import HERE, ROOT, write
from .runner import stream
from .score import grade_qa
from team_memory import timeline as t
from team_memory.store import digest


def validate():
    frozen=json.loads((HERE/'data-freeze.json').read_text())
    for name,h in frozen['files'].items():assert sha256((HERE/name).read_bytes()).hexdigest()==h,name
    keys=json.loads((HERE/'final-key.json').read_text());rows=json.loads((HERE/'final.json').read_text())
    results={}
    for row in rows:
        key=keys[row['id']]
        sources={digest(s['source']):s['source'] for s in row['steps'] if s['op']=='ingest'}
        assert len(sources)==5
        for mode in ('direct','indexed'):
            qa=iter(s['id'] for s in row['steps'] if s['op']=='ask')
            seen=set();visibility=[]
            def generator(system,content):
                generator.last_usage=dict(input_tokens=1,output_tokens=1)
                d=json.loads(content)
                if system==t.INDEX:return '{"decisions":[]}'
                if system==t.COMPARE:
                    present={s['id'] for s in d['earlier']};incoming=d['incoming']['id']
                    assert incoming not in present
                    # The first source has no comparison; later ones appear in arrival order.
                    assert present==seen,(row['id'],present,seen)
                    seen.add(incoming);visibility.append(sorted(present))
                    if incoming!=key['new'] or not key['expected_relation']:return '{"relations":[]}'
                    old=key['old_text'].rsplit(' The evidence archive is ',1)[0] if key['kind']=='correction' else key['old_text']
                    return json.dumps(dict(relations=[dict(kind=key['kind'],target=key['old'],old_quote=old,
                        new_quote=key['new_text'],reason=key['reason_criterion'])]))
                assert system==t.QA
                present={s['id'] for s in d['sources']}
                if not seen:seen.update(present)
                assert present==seen
                k=key['qa'][next(qa)];answers=[]
                for a in k['answers']:
                    assert a['source_id'] in present
                    text=sources[a['source_id']]['source']['text']
                    match=re.search(re.escape(a['aliases'][0]),text,re.IGNORECASE)
                    assert match,(row['id'],a)
                    assert a['condition'] in text
                    answers.append(dict(source=a['source_id'],quote=text,answer=match.group(0),condition=a['condition']))
                return json.dumps(dict(kind=k['kind'],answers=answers))
            r=stream(row,mode,generator)
            grades={s['id']:grade_qa(s['result'],key['qa'][s['id']]) for s in r['steps'] if s['op']=='ask'}
            assert all(x['correct'] for x in grades.values()),(row['id'],grades)
            assert not any(s['result']['errors'] for s in r['steps'] if s['op']=='ingest')
            results[row['id']+'/'+mode]=dict(fixture_checks=grades,visible_source_ids_before_arrivals=visibility,
                                            calls=len(r['calls']),source_count=len(r['objects']['sources']))
    write(ROOT/'results/timeline/data-integrity.json',dict(status='passed',streams=len(rows),arms=2,
          qa_fixture_checks=sum(len(r['fixture_checks']) for r in results.values()),
          scope='Scripted gold responses validate fixtures, source visibility, status transitions and scorer agreement. Not model performance.',results=results))
    print('data integrity passed:',len(results),'stream-arms, 280 scripted QA checks; not model performance')


if __name__=='__main__':validate()
