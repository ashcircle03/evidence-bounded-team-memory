"""Extract a post-hoc source audit from immutable pilot artifacts; no inference.

This is a case-specific evidence report, not a new score or an evaluator fitted
to the pilot. Assertions bind the report to the actual requests and snapshots.
Run from the repository root: python -m evaluation.cupmem.source_audit
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FOLDER = ROOT / "results/cupmem/pilot-v5"
UID = "a5aa884f-29d6-40dc-a72c-e155fcbc7c79"


def canonical_hash(value):
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def build():
    trace_path = FOLDER / f"{UID}.cupmem.json"
    answers_path = FOLDER / f"{UID}.answers.json"
    judgments_path = FOLDER / f"{UID}.judgments.json"
    result_path = ROOT.parent / "campaigns/speakermem-dev/results/sm-119626.json"
    transitions_path = ROOT.parent / "campaigns/cupmem-stale/upstream/cup_mem/store_layer/transitions.py"
    trace, answers, judgments, result = map(read, [trace_path, answers_path, judgments_path, result_path])
    assert result["status"] == "budget_stopped"
    assert len(result["completed"]) == 1
    assert trace["completed_session_count"] == 50
    assert trace["completed_query_count"] == 3
    rows = [json.loads(line) for line in (FOLDER / "http.jsonl").read_text().splitlines()]
    events = {(row["event"], row["request_id"]): (line, row)
              for line, row in enumerate(rows, 1)}

    def request(rid):
        return events[("request", rid)][1]

    def payload(rid):
        return json.loads(request(rid)["body"]["messages"][-1]["content"])

    def response(rid):
        return json.loads(events[("response", rid)][1]["body"]["choices"][0]["message"]["content"])

    def evidence(rid, fields=()):
        req_line, req = events[("request", rid)]
        res_line, res = events[("response", rid)]
        assert canonical_hash(req["body"]) == req["body_sha256"]
        out = dict(request_id=rid, request_line=req_line, response_line=res_line,
                   context=req["context"], request_body_sha256=req["body_sha256"],
                   response_body_sha256=canonical_hash(res["body"]),
                   response=response(rid))
        if fields:
            data = payload(rid)
            out["input_excerpt"] = {key: data[key] for key in fields}
        return out

    profile = {item["item_id"]: item for items in trace["final_profile_snapshot"]["active_profile"].values()
               for item in items}
    chunks = {item["chunk_id"]: item for item in trace["chunk_bank"]}
    deltas = {item["delta_id"]: item for item in trace["delta_store"]}
    old = profile["p_00001"]
    current = profile["p_00075"]
    assert old["active_strength"] == "WEAK"
    assert len(old["revision_history"]) == 1
    assert old["revision_history"][0]["source_session_id"] == "s_001"
    assert old["revision_history"][0]["source_proposal_id"] == "lip_00006"
    assert response(22)["decision"] == "WEAK_CHALLENGE"
    assert payload(22)["latent_invalidation_proposal"]["trigger_delta_ids"] == ["d_00002", "d_00003"]
    assert response(676)["decision"] == "WEAK_CHALLENGE"
    later = next(row for row in trace["session_logs"][38]["invalidation_logs"]
                 if row["proposal"]["proposal_id"] == "lip_00265")
    assert later["apply_result"]["applied_action"] == "WEAK_CHALLENGE_IDEMPOTENT"
    assert later["apply_result"]["before"] == later["apply_result"]["after"]
    unknown = next(row for row in trace["final_profile_snapshot"]["unknown_current"]
                   if row["bucket"] == "stable_preferences" and row["local_track"] == "value_or_priority_tendency")
    assert unknown["created_session_index"] == 0
    assert unknown["invalidated_by_delta_id"] == "lip_00002"
    initial = next(row for row in trace["session_logs"][0]["invalidation_logs"]
                   if row["proposal"]["proposal_id"] == "lip_00002")
    assert initial["candidate_pool_summary"]["candidate_pool_size_before_topk"] == 0
    assert response(10)["decision"] == "SET_UNKNOWN_CURRENT"

    for rid, index in [(12, 1), (667, 38)]:
        assert payload(rid)["user_turns"] == trace["session_logs"][index]["user_turns"]
    new_turns = {turn["turn_id"]: turn["content"] for turn in payload(667)["user_turns"]}
    assert "pay it forward" in new_turns["t_2"]
    assert "insists on paying you back" in new_turns["t_4"]
    assert "gracefully accept a payback" in new_turns["t_6"]
    assert current["source_delta_ids"] == ["d_00076"]
    assert current["evidence_chunk_ids"] == ["c_00075"]
    assert chunks["c_00075"]["source_turn_ids"] == ["t_2", "t_4", "t_6"]
    assert deltas["d_00076"]["proposed_value"] == current["value"]
    assert response(668)["deltas"][0]["proposed_value"] == current["value"]
    assert len(response(668)["deltas"]) == 1
    assert response(669)["decision"] == "ADD"
    assert "hard_positive_constraints" in response(923)
    assert "answer" in response(924)
    for rid in [923, 924]:
        assert payload(rid)["canonical_answer_grounding"]["decisive_basis"][0]["hit_ref"]["id"] == "p_00075"
    for rid, arm in [(928, "cupmem"), (929, "direct")]:
        assert response(rid) == judgments[arm]["ratings"]
        judge_text = request(rid)["body"]["messages"][-1]["content"]
        assert new_turns["t_4"] not in judge_text and new_turns["t_6"] not in judge_text
        assert "[Ground Truth Context]" in judge_text
    scores = {arm: {label: judgments[arm]["ratings"][f"dim{i}_eval"]["pass"]
                    for i, label in enumerate(["SR_explicit", "PR_false_premise", "IPA_action"], 1)}
              for arm in ["cupmem", "direct"]}
    assert list(scores["cupmem"].values()) == [True, True, False]
    assert list(scores["direct"].values()) == [False, False, True]
    assert response(911)["answer"] == answers["cupmem"]["dim1_response"]
    assert response(918)["answer"] == answers["cupmem"]["dim2_response"]
    assert response(924)["answer"] == answers["cupmem"]["dim3_response"]

    files = [FOLDER / "http.jsonl", trace_path, answers_path, judgments_path, result_path, transitions_path]
    file_hashes = {str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else "../" + str(path.relative_to(ROOT.parent)):
                   hashlib.sha256(path.read_bytes()).hexdigest() for path in files}
    report = dict(
        status="post_hoc_source_audit_verified", uid=UID, job_id="119626",
        scope="One completed alternate-model T1 case from a budget-stopped two-case pilot; not a benchmark score or new primary adjudication",
        inference_calls_added=0, source_file_sha256=file_hashes,
        official_scores_unchanged=scores,
        official_judge_evidence=[evidence(928), evidence(929)],
        unknown_without_observed_prior=dict(
            initial_request=evidence(10, ["latent_invalidation_proposal", "candidate_existing_items"]),
            candidate_pool_summary=initial["candidate_pool_summary"],
            persisted_unknown=unknown,
            interpretation="The proposal supplies a supposed prior non-tracking preference without an existing candidate. The unknown track dates to session0, before the new preference arrives."),
        unrelated_early_weakening=dict(
            source=evidence(12, ["session_id", "user_turns"]),
            proposer_requests=[evidence(17, ["lane"]), evidence(21, ["lane"])],
            decision=evidence(22, ["latent_invalidation_proposal"]),
            chunks=[chunks[key] for key in ["c_00001", "c_00002", "c_00003"]],
            deltas=[deltas[key] for key in ["d_00001", "d_00002", "d_00003"]],
            final_old_item=old,
            interpretation="Meditation, Pomodoro and journaling do not entail a change in gift reciprocity. The trace explicitly acknowledges no direct contradiction, yet weakens the old item."),
        later_valid_review_and_provenance=dict(
            decision=evidence(676, ["latent_invalidation_proposal"]),
            applied_action=later["apply_result"]["applied_action"],
            before_after_identical=True,
            code_location="../campaigns/cupmem-stale/upstream/cup_mem/store_layer/transitions.py:241",
            interpretation="The actual changed preference did trigger a correctly targeted later proposal. Because the item was already weak, the transition was idempotent: this newer reason remains in the session trace but does not refresh the persisted item revision history. Do not describe this as wholly missing the later change."),
        conditional_exception=dict(
            source=evidence(667, ["session_id", "user_turns"]),
            delta_extractor=evidence(668), update=evidence(669, ["delta"]),
            chunk=chunks["c_00075"], delta=deltas["d_00076"], final_item=current,
            constraints=evidence(923, ["query", "canonical_answer_grounding"]),
            composer=evidence(924, ["query", "canonical_answer_grounding", "constraint_set"]),
            interpretation="The original conversation supports both default pay-it-forward and an exception for insistent repayment. The single extracted delta and final composer emphasize the exception; the final answer omits the default and ends with a broader accept-if-they-try instruction. It is not wholly unsupported, but this audit does not relabel it a pass."),
        query_path=dict(
            SR=[evidence(906), evidence(907), evidence(909), evidence(910), evidence(911, ["canonical_answer_grounding"])],
            PR=[evidence(913), evidence(914), evidence(916), evidence(917), evidence(918, ["canonical_answer_grounding"])],
            interpretation="The displayed SR/PR reasoning depends on the weak old item and unknown track. It does not reconstruct the new pay-it-forward preference. Traces support this mechanism description; a counterfactual causal effect of removing the early errors has not been measured."),
        answers=answers,
        judge_scope_caveat="The official judge sees M_old/M_new/Hidden Logic and answers, not the full source turns4/6. Direct IPA begins by declining repayment but later also permits acceptance; CUP chiefly recommends acceptance. Different labels may partly reflect default behavior emphasis, not necessarily judge inconsistency. A full-source condition-aware adjudication is needed separately; preserve the official scores.",
        implications=[
            "Outcome scores and update provenance need separate checks: a correct refusal can coexist with an unsupported earlier memory update.",
            "Track whether a later warranted review refreshes evidence even if its status is already weak.",
            "Evaluate default and exception conditions separately, including whether compression preserves both.",
            "These are observed failures/limitations of this single alternate-model run, not proof about the original GPT-4o-mini configuration or all CUPMem cases. No semantic modification is justified by this audit alone.",
        ],
    )
    return report


def markdown(report):
    return """# STALE T1 파일럿 원문 감사

대상은 `a5aa884f-29d6-40dc-a72c-e155fcbc7c79` 한 사례다. 50개 세션과 세 질문을 완료했지만 전체 작업119626은 요청 상한에서 멈췄다. 모델은 BAZE의 gpt-5.4-mini / gemini-3.1-flash-lite이며 원 논문의 모델 그대로 재현한 결과가 아니다. 추가 모델 호출 없이 실제 HTTP 입력·원출력과 저장 상태를 대조했다. 파일 해시, JSON 경로에 대응하는 추출값, HTTP 줄 번호는 `source-audit.json`에 있다. 기존 공식 판단은 수정하지 않았다.

## 공식 점수와 근거 검증은 다른 결론을 준다

| 질문 | CUPMem 공식 채점 | 직접 읽기 공식 채점 | 원문 감사 |
|---|---|---|---|
| SR: 아직 선물 가격을 기억해 나중에 맞추는가? | 통과 | 실패 | CUPMem은 새 관행을 설명하지 않고 과거 항목이 약하고 현재 상태가 불명확하다고 답했다. |
| PR: 계속 같은 가격으로 답례하도록 기록 시스템을 제안하라 | 통과 | 실패 | CUPMem은 전제를 확정할 수 없다며 거절했다. 잘못 생성된 초기 UNKNOWN_CURRENT와 무관한 초기 약화가 판단 근거에 남아 있다. |
| IPA: 친구가 나중에 비용을 정산하려 하면 어떻게 할까? | 실패 | 통과 | CUPMem의 상환 수락에는 실제 원문 근거가 있으나, 기본값인 pay-it-forward를 빠뜨리고 예외를 넓게 적용했다. |

따라서 **2/3 대 1/3을 근거 있는 기억 갱신의 성공으로 해석하면 안 된다.** 단, 실제 변경을 전혀 감지하지 못했다고 해도 틀리다.

## 1. 실제 변경보다 먼저 생긴 두 상태 오류

세션0의 원문은 선물 비용을 추적한다는 현재 행동과 그 습관을 놓아야 하는지에 대한 질문이다. 그런데 request10의 `lip_00002`는 기존 후보가 0개인데도 과거에 ‘선물 가격을 비교하지 않는 성향’이 있었다고 가정하고 `SET_UNKNOWN_CURRENT`를 만든다. 이 UNKNOWN_CURRENT는 세션0 시각으로 마지막까지 남는다. 이후 SR/PR의 판단은 이 상태를 인용한다.

세션1의 실제 입력(request12)은 명상 앱, Pomodoro, 아침 일기 얘기다. request17/21의 제안자는 이 정보가 선물 답례 성향과 직접 충돌하지 않는다고 명시하면서도 기존 성향을 재검토하자고 제안한다. request22는 `WEAK_CHALLENGE`를 선택한다. `p_00001`의 최종 revision_history에는 이때의 이유만 하나 남아 있다.

이는 명상이나 생산성 습관에서 선물 답례 방식의 변화가 도출되지 않는다는 **원문 근거 판단**이다. 두 초기 상태를 제거했을 때 답이 어떻게 바뀔지에 대한 반사실 실험은 하지 않았으므로, 정답 두 개를 오직 이 오류 때문이라고 단정하지 않는다. 다만 SR(request907/910/911)과 PR(request914/917/918)의 명시된 이유가 해당 weak/unknown 상태에 의존한다는 점은 실제 출력으로 확인했다.

## 2. 실제 변경은 감지했지만 최신 근거가 항목 이력에 반영되지 않았다

세션38에서 request676은 올바른 `p_00001`을 지목하고 새 pay-it-forward 관행을 근거로 다시 `WEAK_CHALLENGE`를 제안한다. 원문에 기반한 재검토 자체는 발생했다.

그러나 적용 결과는 `WEAK_CHALLENGE_IDEMPOTENT`이고 적용 전후 스냅숏이 같다. 공식 코드 `cup_mem/store_layer/transitions.py:241`은 이미 WEAK인 항목이면 새 이력·시각을 추가하기 전에 반환한다. 그 결과 새 이유는 **세션 실행 기록에는 남지만 최종 항목 revision_history에는 들어가지 않는다.** 질문에 전달된 항목 이력에는 명상/Pomodoro를 근거로 약화한 과거 설명이 남는다.

이 사례의 정확한 문제는 ‘변경을 한 번도 감지하지 못함’이 아니라 **초기의 무관한 약화와 이후 정당한 재검토를 지속되는 근거 이력에서 구분하지 못함**이다. 동결 코드나 프롬프트를 고치지 않았고, 이 관찰을 전체 사례의 발생률로 확대하지 않는다.

## 3. 새 원문에는 기본값과 예외가 함께 있다

실제 입력 request667의 세션38에는 아래 세 발화가 함께 들어 있다.

- t_2: 커피·주차 비용을 조용히 내고, Venmo로 돌려주려 하면 다른 사람에게 선행을 전하라고 한다.
- t_4: 상대가 정산하지 않으면 불편해하며 계속 갚겠다고 할 때는 그 뜻을 존중하고 싶다고 한다.
- t_6: 어색하지 않게 상환을 받아들이는 구체적 표현을 요청한다.

추출 청크 `c_00075`에는 세 발화가 모두 들어 있지만, request668의 delta는 ‘상대가 고집하면 상환을 자연스럽게 받고 싶다’ 하나다. `d_00076 → p_00075`가 되고, 최종 질문의 decisive basis로 전달된다. request923은 제약 생성이고 request924는 최종 답 생성이며, 재시도 두 번이 아니다.

CUPMem의 답은 상환을 받아들이라는 부분에서 실제 근거가 있다. 하지만 기본값인 거절/pay-it-forward를 누락하고 마지막에는 상대가 정산을 시도하면 받으라고 넓게 표현했다. 따라서 원문에 없는 환각으로만 분류하기도, 완전히 올바른 답이라고 재채점하기도 어렵다. **기본값과 예외의 조건 보존 실패**를 별도로 봐야 한다.

## 4. 공식 judge가 보는 정보의 범위

request928/929의 공식 judge는 M_old, M_new 요약, Hidden Logic, 질문·답을 받는다. t_4/t_6 전체 발화는 주어지지 않는다. CUPMem의 IPA 실패 이유는 상환 수락이 M_new와 충돌한다는 것이다. 직접 읽기 답도 후반에는 수락을 허용하지만 앞에서는 먼저 거절하고 자유롭게 베푸는 방식을 설명한다. 따라서 두 판정의 차이가 단순한 judge 모순인지, 기본 행동을 얼마나 강조했는지의 차이인지는 현재 자료만으로 확정하지 않는다.

원 채점 2/3 대 1/3은 그대로 보존한다. 원문 조건까지 보는 별도 근거 감사에서는 **CUPMem도 직접 읽기도 default/exception을 얼마나 정확히 구분했는지**를 확인해야 한다. 이 한 사례를 이유로 STALE 전체를 부적절한 데이터셋이라고 결론내리지 않는다.

## 설계 판단에 주는 제한적인 근거

정답 여부와 별개로 (1) 재검토를 유발한 원문 관계, (2) 이전 관측 보존, (3) 새로운 타당한 근거가 이력에 남는지, (4) 기본값과 예외 조건이 압축에서 함께 살아남는지를 평가해야 한다. 이는 기존 팀 문제와 직접 연결된다. 아직 팀 사례 적용·기존 QA 보존 결과는 없으며 CUPMem 채택/기각이나 의미 규칙 수정의 결론을 내릴 단계는 아니다.

재생성: 저장소 루트에서 `python -m evaluation.cupmem.source_audit`. 이 명령은 저장된 파일만 읽고 새 감사 산출물 두 개만 쓴다. API·서버 실행·기존 채점 변경은 없다.
"""


if __name__ == "__main__":
    output = build()
    (FOLDER / "source-audit.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    (FOLDER / "source-audit.md").write_text(markdown(output))
    print(json.dumps({"status": output["status"], "uid": UID, "official_scores": output["official_scores_unchanged"],
                      "inference_calls_added": 0}, ensure_ascii=False))
