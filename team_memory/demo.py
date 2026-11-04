"""Offline functional replay in two disposable clones. All identities and work records are simulated."""
import os
import subprocess
import tempfile
from pathlib import Path

from .merge import replay, review, submit
from .qa import answer
from .store import Store


def git(cwd, *args):
    env = dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")
    subprocess.run(["git", "-c", "user.name=Demo", "-c", "user.email=demo@localhost",
                    "-c", "commit.gpgsign=false", *args], cwd=cwd, env=env, check=True,
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def publish(clone):
    git(clone, "add", "records")
    git(clone, "commit", "-m", "Publish work record or review")
    git(clone, "push", "origin", "HEAD:main")


def sample(day, owner, value, setting, **extra):
    quote = f"{setting} 조건에서 다중 클래스 실험 결과는 {value}."
    return {"observed_at": f"2025-01-{day:02}T10:00:00Z", "owner": owner, "issue": "다중 클래스 성능",
            "value": value, "scope": {"분할": setting}, "quote": quote,
            "source": {"location": f"synthetic://demo/{day}", "text": quote, "speaker": owner}, **extra}


def vote(store, row, reviewer):
    return review(store, row["id"], row["proposal"], reviewer, "approve")


def run():
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        git(base, "init", "--bare", "--initial-branch=main", "origin.git")
        for member in ("a", "b"):
            git(base, "clone", "origin.git", member)
        a, b = base/"a", base/"b"
        local_a, local_b = Store(a/"records"), Store(b/"records")
        first = submit(local_a, sample(1, "writer-a", "개선 미관측", "시간 분할"))
        vote(local_a, first, "writer-a")
        publish(a)
        git(b, "pull", "--ff-only", "origin", "main")
        second = submit(local_b, sample(2, "writer-b", "개선 관측", "그룹 분할"))
        vote(local_b, second, "writer-b")
        publish(b)
        git(a, "pull", "--ff-only", "origin", "main")
        before = answer(local_a, "다중 클래스 성능")
        assert len(before["accepted"]) == len(before["pending"]) == 1
        assert before["next_actions"][0]["action"] == "keep_by_condition"
        assert before["next_actions"][0]["changed_conditions"]["분할"]["incoming"] == "그룹 분할"
        vote(local_a, second, "writer-a")
        publish(a)
        git(b, "pull", "--ff-only", "origin", "main")
        after = answer(local_b, "다중 클래스 성능")
        assert len(after["accepted"]) == 2 and not after["pending"]
        third = submit(local_b, sample(3, "writer-b", "개선 미관측", "그룹 분할"))
        vote(local_b, third, "writer-b")
        publish(b)
        git(a, "pull", "--ff-only", "origin", "main")
        vote(local_a, third, "writer-a")
        publish(a)
        git(b, "pull", "--ff-only", "origin", "main")
        conflict = answer(local_b, "다중 클래스 성능")
        assert len(conflict["unresolved"]) == 1 and len(conflict["accepted"]) == 3
        correction = submit(local_b, sample(4, "writer-b", "측정 오류로 재측정 필요", "그룹 분할", corrects=third["id"]))
        vote(local_b, correction, "writer-b")
        assert replay(local_b)[third["id"]]["status"] == "accepted"
        publish(b)
        git(a, "pull", "--ff-only", "origin", "main")
        vote(local_a, correction, "writer-a")
        publish(a)
        git(b, "pull", "--ff-only", "origin", "main")
        view = replay(local_b)
        assert view[third["id"]]["status"] == "superseded" and view[first["id"]]["status"] == "accepted"
        return {"data": "simulated, including reviewer identities and decisions", "transport": "local Git bare remote and two clones",
                "after_pull_before_review": before, "after_both_reviews_and_pull": after,
                "unresolved_pair": conflict["unresolved"], "after_explicit_correction":
                {k: r["status"] for k, r in view.items()}}
