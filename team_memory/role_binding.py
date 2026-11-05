"""Recognize explicit English predicate frames before asking a model to label free text."""
import re

# A frame is used only when all three slots occur in the same construction.
# Technical names and values are captured from the input, never supplied by the rule.
NAME = r"[A-Za-z_][\w.-]*(?:\(\))?"
ENTITY = r'(?:[Tt]he\s+)?(?:["`\']?[\w.-]+["`\']?\s+){0,3}["`\']?[\w.-]+["`\']?'
AUX = r"(?:does\s+not|do\s+not|did\s+not|wasn't|was\s+not|isn't|is\s+not|cannot|can't|would\s+not)"
FRAMES = (
    # A qualified argument followed by the failure predicate. The relative
    # qualifier identifies the affected path, not a second actor.
    rf"(?P<subject>{ENTITY})\s+(?P<condition>(?:passed|sent|given|supplied)\s+to\s+{NAME})\s+"
    rf"(?P<action>{AUX}\s+(?:passed|forwarded|sent|delivered|propagated)\s+(?:forward\s+)?to\s+{NAME})",
    # A main predicate followed by a scope qualifier, before the next clause.
    rf"(?P<subject>{ENTITY})\s+(?P<action>{AUX}\s+[^,.;!?]{{2,90}}?)\s+"
    r"(?P<condition>by\s+default|at\s+startup|at\s+runtime|on\s+startup|in\s+(?:[\w-]+\s+){1,2}mode)\b",
    # An implementation transition followed by the new operation's return
    # behavior. Don't attribute intervening calls or a second sentence to it.
    rf"(?:changing|switching|moving)\s+from\s+{NAME}\s+to\s+(?P<subject>{NAME})\s+"
    r"[^.!?]{0,220}?\b(?P<action>(?:started\s+|began\s+|stopped\s+)?return(?:s|ing|ed)?\s+[\w-]+)"
    r"\s+(?P<condition>for\s+(?:the\s+)?[\w.-]+(?:\(\))?)",
)
PATTERNS = tuple(re.compile(pattern, re.I) for pattern in FRAMES)

def bind(text):
    for pattern in PATTERNS:
        match = pattern.search(text)
        if match is None:
            continue
        return {name: dict(start=match.start(name), end=match.end(name), quote=match.group(name))
                for name in ("subject", "action", "condition")}
    return {}
