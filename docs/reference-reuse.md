# 공개 구현을 직접 사용하는 원문 QA 경로

이 문서는 먼저 측정한 `standard` 구성과 v2 결과(15/20)를 설명한다. 후속 구성은 작성자 전달·혼합 검색·상충 검토를 추가한다. [새 구성의 근거와 사용법](reference-team-profile.md)을 따른다. CLI 기본값은 기존 `standard`로 유지하고 후속 구성은 명시적으로 선택한다.

이 경로는 기존 실패의 입력·인용·의존성 문제를 고치는 **선택 가능한 원문 QA**다. 기존 CUPMem 평가와 구현은 고정한 채 보존한다. 자동 재검토, 승인 상태를 반영한 현재 지식, 전체 팀 메모리의 대체 구현으로 채택한 상태가 아니다.

## 무엇을 가져왔는가

| 확인한 실패 | 실제 사용하는 공개 구현 | 적용 범위 |
|---|---|---|
| 줄바꿈에서 `ValueError`와 발생 조건이 다른 근거 ID로 갈라짐 | LlamaIndex `SentenceSplitter` | Qwen 토크나이저로 512토큰·64토큰 겹침. 문장/문단 우선 분할이며, 상한보다 긴 문장은 더 작게 나뉠 수 있다. |
| 작은 구절을 검색한 뒤 문서 전체와 반복 메타데이터를 넣어 32K 초과 | `VectorStoreIndex.as_retriever`, `PromptHelper`, `CompactAndRefine` | 상위 4개 청크를 사용하고 전체 문서로 확장하지 않는다. 실제 모델 토크나이저·출력 예약량으로 문맥을 구성한다. 필요한 경우 upstream refine가 여러 번 호출될 수 있다. |
| 기억 작성의 실패로 원문 QA까지 `needs_rebuild` | `StorageContext.persist`, `load_index_from_storage` | 원문을 먼저 저장하고 별도의 검색 색인을 사용한다. LLM 기억 작성이 QA의 선행 조건이 아니다. |
| 작은 ID 목록 생성과 출처 복원을 직접 구현 | `CitationQueryEngine`과 **공식 QA/refine 템플릿 그대로** | `[1]` 방식의 답과 citation source node를 받는다. 우리 연결 코드는 원문 ID·문자 위치를 복원한다. |

[분할기 공식 문서](https://developers.llamaindex.ai/python/framework/module_guides/loading/node_parsers/modules/) · [CitationQueryEngine 공식 예제](https://developers.llamaindex.ai/python/examples/query_engine/citation_query_engine/) · [문맥 예산 구현](https://github.com/run-llama/llama_index/blob/main/llama-index-core/llama_index/core/indices/prompt_helper.py) · [저장/불러오기](https://developers.llamaindex.ai/python/framework/module_guides/storing/save_load/)

직접 작성한 부분은 기존 원문 저장 형식 연결, 원문 위치 검증, 정확한 Qwen chat-template 길이를 확인하는 전송 전 검사, JSONL 입출력이다. 검색 점수·청킹 알고리즘·문맥 압축·QA 프롬프트를 다시 구현하지 않는다. 사용 패키지는 `requirements-reference.txt`에 고정한다. 라이브러리 원문 해시는 `results/reference-qa/upstream-reuse.json`에 남긴다.

## 논문이 해결한 부분과 남은 부분

**ALCE**는 내용 정답과 인용의 지지를 분리해 평가한다. 공식 `compute_autoais`는 답의 문장과 해당 문장의 인용 문서를 NLI 모델로 대조하고, 인용 precision/recall을 계산한다. 원문에 있는 문자열을 선택했다는 것만으로 맞는 인용이라고 하지 않는다. 이 경로는 실제 답과 번호가 맞는 `output`/`docs`를 ALCE 입력 형태로 내보낸다. **ALCE 채점 모델을 실행한 상태는 아니며**, `verification` 필드도 문자 위치 일치만 확인했다고 표시한다. [논문](https://aclanthology.org/2023.emnlp-main.398/) · [공식 평가 코드](https://github.com/princeton-nlp/ALCE/blob/main/eval.py)

**LongCite**는 문장별 인용 데이터로 학습한 모델과 추론 코드를 공개했다. 따라서 인용 형식을 추가한 일반 Qwen이 같은 능력을 갖는다고 볼 수 없다. 이번 변경은 LlamaIndex를 실제로 가져다 쓰는 입력/출처 경로이며, LongCite 모델을 사용했다거나 인용 추론 자체를 해결했다고 주장하지 않는다. [논문](https://arxiv.org/abs/2409.02897) · [공식 모델·코드](https://github.com/THUDM/LongCite)

**CUPMem**의 원래 대상은 시간이 지나 유효하지 않게 된 기억을 판별·갱신하는 STALE 설정이다. 기존에 가져온 native 구현은 유지한다. 그 구현이 조건이 다른 실험의 공존, 결정의 전제 변화, 작성자 승인까지 해결했다고 확대 해석하지 않는다. 이번에 해제한 “native 작성 성공 후에만 QA”라는 의존성은 우리 연결 코드의 선택이었다. [STALE/CUPMem 논문](https://arxiv.org/abs/2605.06527) · [공식 구현](https://github.com/icedreamc/STALE)

특히 threeway의 실제 실패 동작을 반대로 설명한 오류나 해결 방법을 바뀐 조건으로 해석한 오류는 **의미 추론 문제로 남는다**. 이번 라이브러리 연결만으로 해결됐다고 표시하지 않는다. 새 재검토 알고리즘이나 병합 규칙은 추가하지 않았다.

## 사용

Python 3.10 이상 격리 환경에 `requirements-reference.txt`를 설치한다. 모델·임베딩 가중치는 기존 로컬 경로를 사용한다. 외부 유료 API로 자동 대체하지 않는다.

Aurora에서는 GPU를 포함한 계산 노드 할당과 conda 활성화 후 실행한다. 그룹 쓰기가 가능한 공유 패키지 경로의 NLTK 데이터는 거절될 수 있다. 계산 노드의 새 개인 디렉터리를 `NLTK_DATA`로 지정하고 공식 데이터를 내려받아야 한다. 첫 실행119844의 오류와 이를 고친119845를 모두 보존했다. 예를 들어 새 작업 안에서:

```bash
umask 077
export NLTK_DATA=/local_datasets/pjw031003/capstone-shared-knowledge/reference-nltk/$SLURM_JOB_ID
mkdir -p "$NLTK_DATA"
python -m nltk.downloader -d "$NLTK_DATA" stopwords punkt_tab
```

```bash
python -m team_memory.reference_qa \
  --store /path/to/reference-records \
  --model-path /local_datasets/.../Qwen3-8B/... \
  --embedding-path /path/to/existing/local/embedding \
  --api-base http://127.0.0.1:PORT/v1
```

표준입력은 한 줄당 JSON이다. `import_history`에 `records`를 전달한 뒤 `ask`에 `question`을 전달한다. `records`는 기존과 같은 `owner`, `observed_at`, `source: {speaker, location, text}`다. 원문 저장에는 LLM 호출이 없다. 임베딩 색인은 첫 질문 시 만들고 원문 집합·설정별로 저장한다. 운영 CLI에는 가짜 모델/임베딩 대체가 없다.

출력의 `answers`, `citation_sources`, `raw`를 사용한다. `status=ok`는 처리와 인용 번호 연결의 성공이며 **내용 정답/인용 entailment 인증이 아니다**. 인용 번호가 없거나 범위를 벗어나면 `partial`이다. 출처 메타데이터는 원문 추적용으로 보존하며 모델 입력에 반복해서 넣지 않는다. 원문 자체에 없는 작성 시간·검토 승인 상태를 판단하는 질문은 이 경로의 지원 범위가 아니다.

기존 owner-review 저장소와 자동으로 합치지 않는다. 승인된 현재 상태에 관한 질문은 기존 상태 처리 경로의 검토가 필요하다. 이 파일은 기존 서비스 전체의 대체를 권하는 안내가 아니다.

## 확인한 범위

- 기존 QA 원문 786개 → 실제 `SentenceSplitter` 청크 832개. 원문 위치 불일치 0개, 가장 긴 청크 506 Qwen 토큰.
- 기존 PEP의 `ValueError`와 발생 조건이 같은 청크에 들어가는 것을 확인했다.
- 실제 라이브러리와 가짜 디코더를 사용한 연결 검사 5개: 줄바꿈 인용/재시작, 긴 문서 입력 제한, 잘못된 인용 번호, 파생 색인 실패 후 복구, 과대 질문의 전송 전 거절. 이는 실제 Qwen 정확도 검사가 아니다.
- [구조 검사 결과](../results/reference-qa/structural-audit.json), [연결 검사](../results/reference-qa/integration-tests.log), [기존 검사](../results/reference-qa/legacy-tests.log).

실제 Qwen용 `evaluation.reference_qa.run`은 기존 전체 기록과 20개 질문을 사용하며 정답 키는 받지 않는다. 모델 호출·실제 입력·원출력·토큰 길이를 남긴다. 이미 본 사례의 개발 진단이며 새로운 holdout 성과가 아니다. 기존 단순 경로의 7/20과 비교할 수 있지만 여러 입력 구성이 함께 바뀌므로 개선 원인을 단일 요소로 단정하지 않는다. 실행 상태는 [progress.json](../results/reference-qa/progress.json)을 따른다.

실제 실행 결과는 **답·인용15/20**, PEP8/8, 공개 Git5/5, 조건별 공존1/1, 상충 기록0/3, 자연 EverMemBench1/3이다. 기존 성공7개 중5개만 보존했다. 작성자 정보를 모델에 숨긴 선택은 사람을 묻는 QA에서 문제가 드러났고, 벡터 검색과 일반 인용 QA만으로는 상충 기록 보존을 해결하지 못했다. 입력 반복을 줄이는 것과 필요한 출처 속성을 없애는 것을 구분해야 한다. [문항별 근거](../results/reference-qa/cases.md)
