"""Render reviewable case evidence and physical API cost without model calls."""
from collections import defaultdict
import json
from .verify import OUT, read


def main():
    cards = read(OUT/'cards.json')
    rating_file = OUT/'ratings.json'
    ratings = read(rating_file)['ratings'] if rating_file.exists() else {}
    lines = ['# Demonstrated QA 사례별 실제 답과 근거', '',
             '이미 본 개발셋. 원문·인용·실패 기록이며 독립 사람 채점이 아니다.', '']
    for identity, card in cards.items():
        result = card['result']; key = card['reference']
        lines.extend(['## '+identity, '', card['question'], '',
                      '기준: '+json.dumps(key.get('A', key.get('expected_sides')), ensure_ascii=False), ''])
        if identity in ratings:
            lines.extend(['판정: '+ratings[identity]['reason'], ''])
        lines.extend(['상태: '+result['status']+'; 경고: '+json.dumps(result.get('warnings', [])), ''])
        for index, claim in enumerate(result['claims']):
            lines.extend([f'### 답 {index+1}', '', claim['text'], ''])
            for evidence in result['answers'][index]['evidence']:
                lines.extend([f"출처: {evidence['location']}; 작성자: {evidence['speaker']}; 시각: {evidence.get('observed_at')}",
                              '', '> '+evidence['quote'].replace('\n', '\n> '), ''])
            lines.extend(['좁은 인용: '+json.dumps(claim['quoted_spans'], ensure_ascii=False), ''])
        if not result['claims']:
            lines.extend(['최종 답 없음.', ''])
        if result.get('selection'):
            lines.extend(['선택 구절:', '```json', json.dumps(result['selection'], ensure_ascii=False, indent=2), '```', ''])
    (OUT/'cases.md').write_text('\n'.join(lines)+'\n')
    costs = defaultdict(lambda:dict(calls=0, prompt_tokens=0, completion_tokens=0))
    for line in (OUT/'calls.jsonl').read_text().splitlines():
        call = json.loads(line); c = call['context']; cost = costs[c['split']+'/'+c['arm']]
        cost['calls'] += 1
        for key in ['prompt_tokens', 'completion_tokens']:
            cost[key] += call['response']['usage'][key]
    (OUT/'costs.json').write_text(json.dumps(dict(physical_call_groups=dict(costs),
        note='Ever select10 is shared by reader_only and combined. Deployment reader_only adds select; combined adds select and retrieve. Do not double count shared selection in physical total.'), indent=2)+'\n')


if __name__=='__main__':
    main()
