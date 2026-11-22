"""Build frozen Retrieval v1 inputs. Run with the official SQuAD dev-v2.0 JSON."""
import argparse
import hashlib
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SQUAD_SHA = "80a5225e94905956a6446d296ca1093975c4d3b3260f1d6c8f68bc2ab77182d8"


def key(s):
    return hashlib.sha256(s.encode()).hexdigest()[:16]


def save(folder, name, rows):
    (folder / (name + ".jsonl")).write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf8")


def span(doc, excerpt, start=None):
    start = doc["text"].index(excerpt) if start is None else start
    assert doc["text"][start:start + len(excerpt)] == excerpt
    return dict(source_id=doc["id"], start=start, end=start + len(excerpt), quote=excerpt)


def public(path):
    assert hashlib.sha256(path.read_bytes()).hexdigest() == SQUAD_SHA
    articles = json.loads(path.read_bytes())["data"]
    corpora, cases, gold = [], [], []
    for article in sorted(articles, key=lambda a: key(a["title"])):
        idx = len(corpora)
        group = "sq-" + key(article["title"])
        docs, chosen = [], []
        for i, para in enumerate(article["paragraphs"]):
            doc = dict(id=f"{group}-{i}", text=para["context"])
            docs.append(doc)
            for q in sorted(para["qas"], key=lambda q: key(q["id"])):
                if q["is_impossible"]:
                    continue
                anchors = sorted({(a["answer_start"], a["text"]) for a in q["answers"]})
                if anchors and all(doc["text"][s:s + len(t)] == t and t for s, t in anchors):
                    chosen.append((q, [span(doc, t, s) for s, t in anchors]))
                    break
        if len(chosen) < 10:
            continue
        split = "dev" if idx < 10 else "evaluation"
        corpora.append(dict(id=group, split=split, title=article["title"], documents=docs))
        for q, anchors in sorted(chosen, key=lambda v: key(v[0]["id"]))[:10]:
            cid = "squad-" + q["id"]
            cases.append(dict(id=cid, corpus=group, task="F05", query=q["question"]))
            gold.append(dict(id=cid, required=[anchors]))
        if len(corpora) == 20:
            break
    return corpora, cases, gold


# Four record formulations for each field type. Values for a field are sampled without replacement.
FIELDS = [
    ("초안 승인자", ["지수", "민아", "은호", "서진", "태영", "수빈"], "누가 초안을 승인했어?"),
    ("회귀 시험 횟수", ["2회", "3회", "4회", "5회", "6회", "8회"], "회귀 시험을 몇 번 돌리기로 했지?"),
    ("보관 기간", ["7일", "14일", "21일", "30일", "45일", "60일"], "자료를 며칠 동안 보관해?"),
    ("검수 장소", ["동관", "별관", "본관", "서관", "신관", "남관"], "어디에서 검수해?"),
    ("배포 요일", ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일"], "무슨 요일에 배포해?"),
]
PROJECTS = ["새봄", "누리", "마루", "다온", "하람", "가람", "소담", "아람", "해솔", "늘봄"]
TEAMS = ["수집", "정제", "분석", "검수", "배포", "운영", "설계", "품질", "지원", "기록"]
RECORDS = ["{scope} 기준 {field}: {value}.", "{field} 항목에는 {value}(으)로 기재했다. 적용 범위는 {scope}이다.",
           "적용 범위 | {field}\n{scope} | {value}", "회의 결정 ({scope}) — {field} = {value}."]
UPDATES = ["정정", "상충 보고", "재검토 요청", "조건 추가", "첫 등록"]
SCOPES = [("v1", "v10"), ("시험 환경", "운영 환경"), ("1차 배치", "10차 배치"), ("내부 공개", "외부 공개")]


def synthetic():
    corpora, cases, gold = [], [], []
    for i in range(100):
        rng = random.Random(34000 + i)
        group = "sim-" + key(str(i))
        project = PROJECTS[i // 10] + " " + TEAMS[i % 10] + "팀"
        field, values, question = FIELDS[(i // 5 + i % 5) % len(FIELDS)]
        old, other, updated, unused = rng.sample(values, 4)
        scope, near = SCOPES[(i // 5) % len(SCOPES)]
        mode = i % 5
        split = "dev" if i // 10 < 5 else "evaluation"
        def record(sc, f, v, topic=project):
            body = rng.choice(RECORDS).format(scope=sc, field=f, value=v)
            return dict(id="s-" + key(str(i) + body + topic), text=topic + " 업무 기록\n" + body)
        previous = record(scope, field, old)
        distractor = record(near, field, other)
        orthogonal = record(scope, "기록 양식", "공통 양식")
        foreign = record(scope, field, unused, PROJECTS[i // 10] + " 협력팀")
        history = [previous, distractor, orthogonal, foreign] if mode != 4 else []
        if mode == 4 and (i // 5) % 2:
            history = [orthogonal, foreign]
        if history:
            for region in ("북부", "남부", "중부"):
                sibling = PROJECTS[i // 10] + " " + TEAMS[i % 10] + " 협력사 " + region + " 지원반"
                for f, pool, _ in rng.sample(FIELDS, 4):
                    history.append(record(rng.choice((scope, near)), f, rng.choice(pool), sibling))
        rng.shuffle(history)
        # Incoming scope addition explicitly refers to its predecessor's scope.
        fact = [f"{scope}의 {field} 기재를 {updated}(으)로 정정합니다.",
                f"{scope}에서 확인한 {field} 값은 {updated}입니다. 기존 기록과 달라 확인이 필요합니다.",
                f"{scope}의 {field} 항목을 다시 검토해 주세요. 아직 변경 결정은 없습니다.",
                f"{scope}의 {field} 지침에 예외를 추가합니다. 야간에는 {updated}입니다.",
                f"{scope}의 {field} 항목을 {updated}(으)로 처음 등록합니다."][mode]
        incoming = dict(id="s-" + key(group + fact), text=project + " 후속 기록\n" + fact)
        docs = history + [incoming]
        corpora.append(dict(id=group, split=split, documents=docs))
        fid = group + "-ingest"
        cases.append(dict(id=fid, corpus=group, task="F02", incoming=incoming["id"], history=[d["id"] for d in history]))
        def body(doc):
            return span(doc, doc["text"].split("\n", 1)[1])
        gold.append(dict(id=fid, category=UPDATES[mode], required=[[body(previous)]] if mode != 4 else []))
        qid = group + "-ask"
        # Reviews here are supplied snapshot inputs for retrieval-only evaluation.
        states, needed_states = [], []
        selected = i // 5 % 4
        status = ["pending", "approved", "rejected", "pending"][selected]
        if mode in (0, 1, 2):
            kind = ["correction", "conflict", "reconsider"][mode]
            pid = "p-" + key(group)
            states = [dict(id=pid, kind=kind, status=status, previous=body(previous), incoming=body(incoming))]
            needed_states = [pid]
        query = f"{project} {scope}에서 {question}"
        needed = [previous, incoming] if mode < 4 else [incoming]
        if mode == 3:
            query = f"{project} {scope}에서 평소와 야간의 {field} 지침을 각각 찾아줘."
        # In one quarter of histories the question targets the near-miss condition alone.
        if selected == 3 and mode != 4:
            query, needed, needed_states = f"{project} {near}에서 {question}", [distractor], []
        if mode == 4 and (i // 5) % 2:
            query, needed = f"{project} {near}에서 {question}", []
        cases.append(dict(id=qid, corpus=group, task="F05", query=query, reviews=states))
        gold.append(dict(id=qid, category="근거 없음" if not needed else ("인접 조건" if needed == [distractor] else UPDATES[mode]),
                         required=[[body(d)] for d in needed], required_review_ids=needed_states))
    return corpora, cases, gold


def build(path, output):
    a = json.loads((ROOT / "aimers.json").read_text())
    parts = [public(path), synthetic(), (a["corpora"], a["cases"], a["gold"])]
    output.mkdir(parents=True, exist_ok=True)
    for name, groups in zip(["corpora", "cases", "gold"], zip(*parts)):
        save(output, name, [row for group in groups for row in group])


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("squad", type=Path)
    p.add_argument("--output", type=Path, default=ROOT / "v1")
    args = p.parse_args()
    build(args.squad, args.output)
