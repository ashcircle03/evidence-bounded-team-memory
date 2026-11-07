# 저자 구현의 연결을 복구한 QA 후보

논문 성능 재현이 아닌 Qwen3-8B 어댑터다. 기본 선택 경로는 아직 attributed다.

- Attribute First pinned `cc7b995dfb288da7982ae388994f182bef030b75`의
  `few_shot_experiments/prompts/LFQA.json` 원문을 Apache-2.0 조건으로 보존했다.
  첫 두 예시의 전체 문서, 선택 구절, 구절 번호와 출력 문장을 JSON 대화 예시로 변환한다.
  원 구현의 무작위 2개 선택은 재현 가능하게 첫 두 개 고정으로 변경했다.
- 원 구현의 선택 → 문장별 근거 연결을 유지한다. 자유로운 purpose 해석과
  답변 뒤에 인용 구절을 다시 쓰는 단계를 제거했다. 생성 결과는 답과 highlight_ids이며,
  코드가 해당 구절의 원 출처로 복원한다. 문자열 검증은 의미 검증이 아니다.
- 저자 예시에 중복 구절이 있으므로 번호가 변하지 않게 그대로 보존한다.
  반면 원 구현의 잘못된 출처를 다른 문서로 자동 이동하는 처리는 쓰지 않는다.
- AQA pinned `f72bdb3e5d1f4bf83a3dd84596039b67ddd145e8`의 few_shot.py는
  3개 완성 예시와 출처별 답을 사용한다. datasets 디렉터리에는 실제 JSON이 없고,
  README의 Drive 폴더는 이 연결에서404여서 원 3-shot을 재현하지 못했다.
  기존 논문 Figure1의 대통령 충돌 예시를 구조화한 paraphrase 1개만 추가한다.
  저자의 3-shot 데이터나 finetuning을 가져왔다고 주장하지 않는다.
- 검색은 기존 LlamaIndex BM25를 사용한다. IRCoT의 누적·재독해 연결을 참고해
  새 문서가 들어오면 선택을 다시 수행한다. 최대2회, 질의2개/회, 결과4개/질의,
  최초8개를 버리지 않고 최대24개. 질의 없음/중복 질의/새 문서 없음에서 멈춘다.
  이는 원 IRCoT의 마지막 생성 문장 검색과 다르며 완전 재현이 아니다.
- 원문은 계속 생성기에 전달하지만 인용은 선택 구절로 제한된다. 따라서 선택 누락이
  답을 막는지, 동일 예시를 받은 direct 독해와 비교한다. 실패를 숨기는 fallback은 없다.

## 호출

`team_memory.reference_demonstrated.DemonstratedQA`는 기존 import_history/ask를
그대로 지원한다. 고정 원문 입력은 `answer_from_sources(question, sources, llm)`으로
호출한다. UI/MCP와 상태 저장 구조는 추가하지 않았다. 평가 전 기본 경로 변경 없음.

## 원 출처

- https://github.com/lovodkin93/attribute-first-then-generate/tree/cc7b995dfb288da7982ae388994f182bef030b75/few_shot_experiments
- https://github.com/Shaier/Adaptive_QA/blob/f72bdb3e5d1f4bf83a3dd84596039b67ddd145e8/experiments/few_shot.py
- https://github.com/StonyBrookNLP/ircot/blob/main/base_configs/ircot_flan_t5_xl_hotpotqa.jsonnet

## 실제 평가 결과

기존20은19/20, Ever10은 direct/reader_only/combined 모두2/10으로 채택하지 않았다.
Ever10 모두 검색 요청이 비어 추가 검색이 실행되지 않았다. [원출력과 한계](../results/reference-qa/demonstrated-v1/README.md).
