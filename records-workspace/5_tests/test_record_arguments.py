from copy import deepcopy

import pytest

from team_memory.records.arguments import validate_arguments, visible_arguments, with_arguments


def test_native_roles_and_invalid_predicate_are_isolated():
    source = {"text": "Petr will send questions. Petr agreed."}
    rows = [{"predicate": [-1, 8], "qas": []},
            {"predicate": [10, 14], "qas": [
                {"question": "who will send something ?", "answers": ["Petr"]},
                {"question": "what will someone send ?", "answers": ["questions"]}]}]
    result = with_arguments(source, rows, "test")
    links = result["record_arguments"]["links"]
    assert len(links) == 1
    assert links[0]["predicate"]["quote"] == "send"
    assert links[0]["argument"]["quote"] == "questions"
    assert links[0]["role_question"] == "what will someone send ?"
    assert visible_arguments(result, 26, 38)["record_arguments"]["links"] == []
    corrupt = deepcopy(result)
    corrupt["record_arguments"]["links"][0]["argument"]["start"] += 1
    with pytest.raises(ValueError):
        validate_arguments(corrupt)


def test_native_template_never_overrides_question_or_approval():
    row = dict(predicate=[5, 13], qas=[dict(question="who approved something ?",answers=["Petr"])],
               raw="<pad> who _ _ approved something _ _ ?<extra_id_7> Petr</s>")
    source = with_arguments({"text":"Petr approved it."}, [row], "fixture")
    link = source["record_arguments"]["links"][0]
    assert link["role_template"] == "who _ _ approved something _ _ ?"
    assert not visible_arguments(source, 5, 13)["record_arguments"]["links"]
    changed = deepcopy(source)
    changed["record_arguments"]["qualification"] = "approved"
    with pytest.raises(ValueError):
        validate_arguments(changed)
    changed = deepcopy(source)
    changed["record_arguments"]["links"][0]["role_template"] = "when _ _ approved something _ _ ?"
    with pytest.raises(ValueError):
        validate_arguments(changed)
    with pytest.raises(ValueError):
        with_arguments(source, [row], "other")


def test_public_example_restarts_and_preserves_actor_and_object(tmp_path):
    from examples.records_argument_roundtrip import demo
    assert demo(tmp_path) == [
        ("send","who will send something ?","Petr","minutes.md#L4"),
        ("send","what will someone send ?","questions","minutes.md#L4"),
    ]
