"""Small external syntax controls, run in the pinned parser environment."""
from team_memory.records.policy_scope import restriction
import spacy


def main():
    parse = spacy.load('en_core_web_sm', disable=['ner'])
    # The first sentence is RFC 5049 section 3. All other controls are constructed.
    cases = [
        ('Any SigComp implementation that is used for the compression of SIP messages',
         ' MUST conform to this document, as well as to [RFC3320].', '', True),
        ('All parcels tagged as `FRAGILE`', ' must be inspected.', '', True),
        ('All parcels', ' must be inspected.', '', False),
        ('All parcels tagged as fragile', ' were inspected.', '', False),
        ('all parcels tagged as fragile', '.', 'Every employee must inspect ', False),
        ('All parcels tagged', ' as fragile must be inspected.', '', False),
        ('All parcels, which have labels,', ' must be inspected.', '', False),
    ]
    for span, suffix, prefix, expected in cases:
        claim = prefix + span + suffix
        p = dict(old_role='subject', target=dict(start=0, end=len(claim), text=claim),
                 context=dict(start=len(prefix), end=len(prefix+span), text=span))
        assert bool(restriction(p, parse)) == expected, claim
    print(f'{len(cases)} scope controls passed')


if __name__ == '__main__':
    main()
