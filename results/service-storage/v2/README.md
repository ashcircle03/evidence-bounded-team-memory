# 비용 분해 첫 실행의 준비 실패

Slurm122923는9초 후FAILED/1:0으로 종료됐다. 평가 디렉터리의 `profile.py`가 Python 표준 `profile`을 가려 Transformers의 cProfile import가 실패했다. 임베딩 비교·QA 측정은 시작하지 않았다. GPU0.15분을 실패 비용에 포함한다.

[실패 로그](slurm.log), [자원 기록](accounting.txt), [당시 평가 코드](failed-source/profile.py), [당시 진입점](failed-source/run.py), [동결](freeze.json), [장부](dispatch.json)를 보존했다. 평가 파일명을 instrumentation.py로 바꾸고 `python -m evaluation.storage_cost.run`으로 실행한 별도버전은 [v2b](../v2b/README.md)다. 모델·데이터·비교 기준·자원은 확대하지 않았다.
