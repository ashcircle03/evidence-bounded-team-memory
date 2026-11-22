"""Optional source-local, unverified predicate arguments; offsets are Unicode characters."""
from copy import deepcopy
import re

TOKEN = re.compile(r"\w+(?:['’]\w+)*|[^\w\s]")
VERSION = "records.arguments/v1"


def _span(text, start, end):
    if type(start) is not int or type(end) is not int or not 0 <= start < end <= len(text):
        raise ValueError("Argument span outside source")
    return dict(start=start, end=end, quote=text[start:end])


def validate_arguments(source):
    text = source["text"]
    layer = source["record_arguments"]
    if layer["version"] != VERSION or not layer["producer"].strip():
        raise ValueError("Invalid argument producer or version")
    if layer["qualification"] != "model_extracted_unverified":
        raise ValueError("Argument was promoted to a fact")
    for link in layer["links"]:
        if not link["role_question"].strip():
            raise ValueError("Missing semantic role question")
        if "role_template" in link:
            surface = " ".join(w for w in link["role_template"].split() if w != "_")
            if surface != " ".join(link["role_question"].split()):
                raise ValueError("Template differs from role question")
        for key in ("predicate", "argument"):
            span = link[key]
            if span != _span(text, span["start"], span["end"]):
                raise ValueError("Argument quote differs from source")


def with_arguments(source, predicates, producer):
    """Keep the native role question. Only uniquely alignable answers get a link."""
    if "record_arguments" in source:
        raise ValueError("Source already has an argument layer")
    text = source["text"]
    tokens = list(TOKEN.finditer(text))
    words = [token.group() for token in tokens]
    links = []
    skipped = 0
    for row in predicates:
        if not isinstance(row, dict) or not isinstance(row.get("qas"), list):
            skipped += 1
            continue
        templates = {}
        raw = row.get("raw", "")
        for pair in (raw if isinstance(raw, str) else "").removeprefix("<pad>").removesuffix("</s>").split("<extra_id_9>"):
            template, sep, _ = pair.partition("<extra_id_7>")
            if sep:
                expanded = " ".join(word for word in template.split() if word != "_")
                templates.setdefault(expanded, set()).add(template.strip())
        try:
            predicate = _span(text, *row["predicate"])
        except (KeyError, TypeError, ValueError):
            skipped += 1
            continue
        for qa in row["qas"]:
            if not isinstance(qa, dict) or not isinstance(qa.get("question"), str) or not isinstance(qa.get("answers"), list):
                skipped += 1
                continue
            question = qa["question"].strip()
            for answer in qa["answers"]:
                phrase = TOKEN.findall(answer) if isinstance(answer, str) else []
                starts = [i for i in range(len(words)) if phrase and words[i:i+len(phrase)] == phrase]
                if len(starts) != 1 or not question:
                    skipped += 1
                    continue
                i = starts[0]
                argument = _span(text, tokens[i].start(), tokens[i+len(phrase)-1].end())
                link = dict(predicate=predicate, role_question=question, argument=argument)
                matches = templates.get(" ".join(question.split()), set())
                if len(matches) == 1:
                    link["role_template"] = next(iter(matches))
                if link not in links:
                    links.append(link)
    result = dict(source, record_arguments=dict(version=VERSION, producer=producer, links=links,
                  qualification="model_extracted_unverified", skipped=skipped))
    validate_arguments(result)
    return result


def visible_arguments(source, start, end):
    layer = source.get("record_arguments")
    if layer is None:
        return {}
    links = [link for link in layer["links"]
             if all(start <= link[key]["start"] and link[key]["end"] <= end
                    for key in ("predicate", "argument"))]
    return {"record_arguments": dict(layer, links=deepcopy(links))}
